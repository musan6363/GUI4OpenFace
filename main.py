# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import subprocess


class TextWidget(Widget):
    text = StringProperty()    # プロパティの追加

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = ''

    def buttonClicked(self):        # ボタンをクリック時
        result = subprocess.run("~/openface/OpenFace-OpenFace_2.2.0/build/bin/FaceLandmarkVidMulti -f ~/openface/OpenFace-OpenFace_2.2.0/samples/multi_face.avi -out_dir ~/cmc/210628/test",
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.returncode)
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
