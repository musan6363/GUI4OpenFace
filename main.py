# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import subprocess

CMD = "/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti"  # 実行するコマンドのパス

inputvideo = "/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/samples/multi_face.avi"  # 【要修正】直接指定せずwith文等で走査させる
outdir = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210629/test"  # 【要修正】引数で親ディレクトリを与えて，その中に動画ごとにフォルダを作る．


class RunWidget(Widget):
    text = StringProperty()    # プロパティの追加

    def __init__(self, **kwargs):
        super(RunWidget, self).__init__(**kwargs)
        self.text = ''

    def buttonClicked(self):        # ボタンをクリック時
        self.text = "Running..."
        result = subprocess.run([CMD, "-f", inputvideo, "-out_dir", outdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.returncode)
        print(result.stdout)
        if result.returncode == 0:
            self.text = "DONE"
        else:
            self.text = "error"


class RunOpenFaceApp(App):
    def __init__(self, **kwargs):
        super(RunOpenFaceApp, self).__init__(**kwargs)
        self.title = 'OpenFace GUI'

    def build(self):
        return RunWidget()


if __name__ == '__main__':
    RunOpenFaceApp().run()
