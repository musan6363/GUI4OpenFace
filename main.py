# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
import subprocess
import glob
from pathlib import Path
import shutil
import os
import sys
import plot_glaph

if len(sys.argv) == 2:
    CMD = sys.argv[1]
else:
    CMD = r"/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti"  # 実行するコマンドのパス
    # 【注意】環境に応じて適切なパスを選択する！！
    # CMD = r"/Users/username/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti"  # Macの例
    # CMD = r"C:\Users\username\OpenFace\OpenFace_2.2.0_win_x64\OpenFace_2.2.0_win_x64/FaceLandmarkVidMulti.exe"  # Windowsの例

Window.size = (1000, 600)

resource_add_path('./Fonts')  # 日本語対応
LabelBase.register(DEFAULT_FONT, 'GenEiGothicM-SemiLight.ttf')  # 日本語対応

suffixs = ['.mp4', '.MP4', '.avi', '.AVI', '.mov', '.MOV']

IS_VIDEO_FILE = 0
IS_DIR = 1

# 既知の無視するエラー
ignore_error = [
    '[ WARN:1] global /tmp/opencv-20210523-95168-eavm03/opencv-4.5.2/modules/core/src/matrix_expressions.cpp (1334) assign OpenCV/MatExpr: processing of multi-channel arrays might be changed in the future: https://github.com/opencv/opencv/issues/16739\n']


class RunWidget(Widget):
    label_text = StringProperty()
    button_text = StringProperty()

    def __init__(self, **kwargs):
        super(RunWidget, self).__init__(**kwargs)
        self.label_text = '動画ファイルもしくはフォルダをここにドロップ'
        self.button_text = ''
        self._filepath = None
        self.flag_error = False
        self._file = Window.bind(on_dropfile=self._get_file_path)

    def _get_file_path(self, window, file_path):
        self._filepath = Path(file_path.decode('utf-8'))
        self.label_text = '\
ファイルを受け取りました．\n\
\"RUN\"ボタンをクリックして\n\
\"実行完了\"と表示されるまでしばらくお待ち下さい．'
        self.button_text = 'RUN'

    def _is_file_exist(self):
        if self._filepath is None:
            print("NONE")
            return -1
        elif self._filepath.is_file():
            # ファイルは動画か判定する
            ext = self._filepath.suffix
            if ext in suffixs:
                return IS_VIDEO_FILE
            else:
                self.label_text = self._filepath.name + " is not Video"
                return -1
        elif self._filepath.is_dir():
            return IS_DIR
        else:
            print("ERROR")
            return -1

    def begin(self):
        self.label_text = '\
実行中です．\n\
\"実行完了\"と表示されるまでしばらくお待ち下さい．'
        self.button_text = ''

    def run_openface(self):
        flag = self._is_file_exist()

        videos = []
        if flag == IS_VIDEO_FILE:
            videos.append(str(self._filepath))
        elif flag == IS_DIR:
            for filetype in suffixs:
                # 動画だけを対象に追加
                videos.extend(glob.glob(str(self._filepath) + "/*" + filetype))
        else:
            self.label_text = "ファイルが見つかりません"
            return

        # 出力ディレクトリの作成
        lastpath = os.path.splitext(os.path.basename(str(self._filepath)))[0]
        outdir = str(self._filepath.parent) + f"/{lastpath}_output/"
        csvdir = Path(outdir + "csv/")
        try:
            os.makedirs(csvdir)
        except FileExistsError:
            pass
        glaphdir = Path(outdir + "glaph/")
        try:
            os.makedirs(glaphdir)
        except FileExistsError:
            pass

        _runcount = 1
        for inputvideo in videos:
            target_path = Path(inputvideo)
            name = target_path.stem
            print(f"[{_runcount}/{len(videos)}]" + name + " is Running")
            _runcount += 1
            # 実行中のファイルを記録．異常終了時に確認する用．正常終了すればこのファイルは消える．
            with open(outdir + "current_run.txt", mode='a') as run_f:
                run_f.write(name + '\n')

            try:
                # 【メイン】OpenFaceの実行
                result = subprocess.run([CMD, "-f", target_path, "-out_dir", outdir + name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # OpenFace実行結果の確認
                with open(outdir + name + "/" + name + "_stdout.txt", mode='w') as stdout_f:
                    stdout_f.write(result.stdout)
                if result.stderr and result.stderr not in ignore_error:
                    # エラー出力があれば各ディレクトリにログを残す．
                    # 出力ディレクトリにエラーが出たファイル名をまとめて追記する．
                    self.flag_error = True
                    with open(outdir + name + "/" + name + "_stderr.txt", mode='w') as stderr_f:
                        stderr_f.write(result.stderr + '\n')
                    with open(outdir + "stderr_all.txt", mode='a') as allerr_f:
                        allerr_f.write(name + '\n')

                if result.returncode == 0:
                    ori_csv = Path(outdir + name + "/" + name + ".csv")
                    shutil.copy(ori_csv, csvdir)
                    plot_glaph.PlotGlaph(str(ori_csv), str(glaphdir), name)
                    print("DONE " + name)
                else:
                    print("error " + name)
            except plot_glaph.NoSuccessValue:
                self.flag_error = True
                with open(outdir + name + "/" + name + "_stderr.txt", mode='a') as stderr_f:
                    stderr_f.write("NoSuccessValue: CSVに成功データ(success=1)がないかもしれません．\n")
                with open(outdir + "stderr_all.txt", mode='a') as allerr_f:
                    allerr_f.write(name + ": NoSuccessValue: CSVに成功データ(success=1)がないかもしれません．" + '\n')
            except:
                self.flag_error = True
                with open(outdir + name + "/" + name + "_stderr.txt", mode='a') as stderr_f:
                    stderr_f.write("Unexpected Error\n")
                with open(outdir + "stderr_all.txt", mode='a') as allerr_f:
                    allerr_f.write(name + ": Unexpected Error" + '\n')

        self._filepath = None
        self.button_text = ''
        if self.flag_error:
            self.label_text = f"\
実行完了\n\n\
入力ファイルと同じディレクトリ\n\
({outdir})\n\
に出力しました．\n\n\
一部のファイルにエラーがあります．\n\
詳しくは出力先のstderr_all.txtに書かれたディレクトリを参照してください．"
        else:
            self.label_text = f"\
実行完了\n\n\
入力ファイルと同じディレクトリ\n\
({outdir})\n\
に出力しました．\n\n\
続けて実行するには動画ファイルもしくはフォルダをドロップしてください．\n\
終了するには右上のバツを押してください．"  # win
        os.remove(outdir + "current_run.txt")


class RunOpenFaceApp(App):
    def __init__(self, **kwargs):
        super(RunOpenFaceApp, self).__init__(**kwargs)
        self.title = 'OpenFace GUI'

    def build(self):
        return RunWidget()


if __name__ == '__main__':
    RunOpenFaceApp().run()
