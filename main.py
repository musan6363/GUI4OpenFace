# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import subprocess

# CMD = "~/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti"  # 実行するコマンドのパス, Not found
CMD = "/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti"  # 実行するコマンドのパス

# inputvideo = "~/openface/OpenFace-OpenFace_2.2.0/samples/multi_face.avi"  # Not found
inputvideo = "/Users/mrkm-cmc/openface/OpenFace-OpenFace_2.2.0/samples/multi_face.avi"  # 【要修正】直接指定せずwith文等で走査させる
# outdir = "~/cmc/210629/test"  # 【要修正】引数で親ディレクトリを与えて，その中に動画ごとにフォルダを作る．
outdir = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210629/test"  # 【要修正】引数で親ディレクトリを与えて，その中に動画ごとにフォルダを作る．


class TextWidget(Widget):
    text = StringProperty()    # プロパティの追加

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
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


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = 'greeting'

    def build(self):
        return TextWidget()


if __name__ == '__main__':
    TestApp().run()
