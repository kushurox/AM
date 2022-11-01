from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
import uuid
from utils.pages import Dashboard, AttendancePage


class RootWidget(MDScreenManager):
    STATE = {}

    def __init__(self, *args, **kwargs):
        super(RootWidget, self).__init__(*args, **kwargs)

    def btn_pressed(self):
        print("Pressed")


class AM(MDApp):
    def build(self):
        Window.maximize()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return RootWidget()


if __name__ == '__main__':
    app = AM()
    app.run()
