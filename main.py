import json
import os

from kivy import Config
from kivy.uix.screenmanager import NoTransition

Config.set("graphics", "multisamples", 2)


from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from utils.pages import Dashboard, AttendancePage


class RootWidget(ScreenManager):
    STATE = {}

    def __init__(self):
        super(RootWidget, self).__init__()
        self.transition = NoTransition()


class AM(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return RootWidget()


if __name__ == '__main__':
    app = AM()
    app.run()
