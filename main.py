# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty
import subprocess
import glob

CMD = "/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti"  # 実行するコマンドのパス

# inputvideo = "/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/samples/multi_face.avi"  # 【要修正】直接指定せずwith文等で走査させる
# inputdir = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210629/inputvideo/"
filetype = 'mp4'
outdir = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210629/test"  # 【要修正】引数で親ディレクトリを与えて，その中に動画ごとにフォルダを作る．


class RunWidget(Widget):
    text = StringProperty()    # プロパティの追加

    def __init__(self, **kwargs):
        super(RunWidget, self).__init__(**kwargs)
        self.text = ''
        self._filepath = None
        self._file = Window.bind(on_dropfile=self._get_file_path)

    def _get_file_path(self, window, file_path):
        self._filepath = file_path.decode('utf-8')
        return

    def buttonClicked(self):        # ボタンをクリック時
        if self._filepath is None:
            self.text = "NONE"
            return
        else:
            self.text = "Running..."  # 出てこない

        videos = glob.glob(self._filepath + "/*." + filetype)  # self._filepath内でfiletype拡張子に一致するファイルパスを取得
        print(self._filepath + "/*." + filetype)

        _i = 0
        for inputvideo in videos:
            result = subprocess.run([CMD, "-f", inputvideo, "-out_dir", outdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.returncode)
            print(result.stdout)
            if result.returncode == 0:
                self.text = "DONE" + str(_i)
            else:
                self.text = "error" + str(_i)
            _i += 1

        self._filepath = None


class RunOpenFaceApp(App):
    def __init__(self, **kwargs):
        super(RunOpenFaceApp, self).__init__(**kwargs)
        self.title = 'OpenFace GUI'

    def build(self):
        return RunWidget()


if __name__ == '__main__':
    RunOpenFaceApp().run()
