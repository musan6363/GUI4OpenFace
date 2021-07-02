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

Window.size = (1000, 300)

resource_add_path('/Users/mrkm-cmc/Library/Fonts')  # 日本語対応
LabelBase.register(DEFAULT_FONT, 'GenEiGothicM-SemiLight.ttf')  # 日本語対応

CMD = "/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti"  # 実行するコマンドのパス

suffixs = ['.mp4', '.MP4', '.avi', '.AVI', '.mov', '.MOV']

IS_VIDEO_FILE = 0
IS_DIR = 1


class RunWidget(Widget):
    # 【要改善】実行中であることがわかりにくい．ポップアップの追加等を検討
    label_text = StringProperty()    # プロパティの追加

    def __init__(self, **kwargs):
        super(RunWidget, self).__init__(**kwargs)
        self.label_text = '動画ファイルもしくはフォルダをここにドロップ\n\n\"実行完了\"と表示されるまで待ってください．'
        self._filepath = None
        self._file = Window.bind(on_dropfile=self._get_file_path)

    def _get_file_path(self, window, file_path):
        self._filepath = Path(file_path.decode('utf-8'))
        # self._make_outdir()
        self.run_openface()

    def _make_outdir(self):
        # 選択されたパスの1つ上に出力ディレクトリを作る．
        pass

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
            return

        outdir = str(self._filepath.parent) + "/output/"

        _i = 0
        for inputvideo in videos:
            target_path = Path(inputvideo)
            name = target_path.stem
            result = subprocess.run([CMD, "-f", target_path, "-out_dir", outdir + name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.returncode)
            print(result.stdout)
            if result.returncode == 0:
                print("DONE" + str(_i))
            else:
                print("error" + str(_i))
            _i += 1

        self._filepath = None
        self.label_text = f"実行完了\n\n入力ファイルと同じディレクトリ\n({outdir})\nに出力しました．"


class RunOpenFaceApp(App):
    def __init__(self, **kwargs):
        super(RunOpenFaceApp, self).__init__(**kwargs)
        self.title = 'OpenFace GUI'

    def build(self):
        return RunWidget()


if __name__ == '__main__':
    RunOpenFaceApp().run()
