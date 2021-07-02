# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty
import subprocess
import glob
from pathlib import Path

CMD = "/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti"  # 実行するコマンドのパス

suffixs = ['.mp4', '.MP4', '.avi', '.AVI', '.mov', '.MOV']
outdir = "/Users/mrkm-cmc/openface/output/210702/"  # 【要修正】引数で親ディレクトリを与えて，その中に動画ごとにフォルダを作る．

IS_VIDEO_FILE = 0
IS_DIR = 1


class RunWidget(Widget):
    label_text = StringProperty()    # プロパティの追加

    def __init__(self, **kwargs):
        super(RunWidget, self).__init__(**kwargs)
        self.label_text = 'File is not selected'

        self._filepath = None
        self._file = Window.bind(on_dropfile=self._get_file_path)

    def _get_file_path(self, window, file_path):
        self._filepath = Path(file_path.decode('utf-8'))
        self.label_text = self._filepath.name + " is selected"
        # self._make_outdir()

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

    def buttonClicked(self):        # ボタンをクリック時
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

        self.run_openface(videos)

        self._filepath = None
        self.label_text = "Done"

    def run_openface(self, videos):
        _i = 0
        for inputvideo in videos:
            target_path = Path(inputvideo)
            name = target_path.stem
            result = subprocess.run([CMD, "-f", target_path, "-out_dir", outdir + name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.returncode)
            print(result.stdout)
            if result.returncode == 0:
                self.label_text = "DONE" + str(_i)
            else:
                self.label_text = "error" + str(_i)
            _i += 1


class RunOpenFaceApp(App):
    def __init__(self, **kwargs):
        super(RunOpenFaceApp, self).__init__(**kwargs)
        self.title = 'OpenFace GUI'

    def build(self):
        return RunWidget()


if __name__ == '__main__':
    RunOpenFaceApp().run()
