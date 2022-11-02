import datetime
import json
import socket
import uuid

import pyqrcode
from kivy.uix.screenmanager import ScreenManager
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen

import requests

HOST_ADDR = socket.gethostbyname(socket.gethostname())


class Dashboard(MDScreen):
    def __init__(self, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)

    def to_attendance(self):
        # Make sure to save state before changing
        self.parent: ScreenManager

        if not self.tname.text or not self.section.text:
            toast("Please fill in required details")
            return

        self.parent.STATE["session"] = {
            "attendance hash": str(uuid.uuid4()),
            "staff name": self.tname.text,
            "section": self.section.text,
            "students": []
        }

        r = requests.post(f'http://{HOST_ADDR}:5000/start-session', json=self.parent.STATE['session'])

        print("Started Session", self.parent.STATE["session"]["attendance hash"])
        unique_hash = pyqrcode.create(f'{HOST_ADDR}:5000/verify?hash={self.parent.STATE["session"]["attendance hash"]}')
        unique_hash.png("tmp/current.png", scale=10, background=(0, 0, 0, 0), module_color=[255, 255, 0, 255])

        self.parent.current = "attendance"


class AttendancePage(MDScreen):

    def __init__(self, *args, **kwargs):
        super(AttendancePage, self).__init__(*args, **kwargs)

    def on_enter(self, *args):
        self.ah.text = f'Attendance Hash: {self.parent.STATE["session"]["attendance hash"]}'
        self.qrcode_holder.source = "tmp/current.png"

    def mark_as_present(self, roll_no: str):
        self.roll_no.text = ""
        r = requests.post(f'http://{HOST_ADDR}:5000/commit', data={"rollno": roll_no})
        toast("Marked")

    def finish_session(self):
        r = requests.get(f'http://{HOST_ADDR}:5000/get-state')
        self.parent.STATE['session'].update(json.loads(r.text))
        with open("data/present.txt", "a") as fp:
            fp.write("\n")
            fp.write("="*5)
            fp.write(f"\nhash: {self.parent.STATE['session']['attendance hash']}\n")
            fp.write(f"staff name: {self.parent.STATE['session']['staff name']}\n")
            fp.write(f"Section: {self.parent.STATE['session']['section']}\n")
            for student in self.parent.STATE["session"]["students"]:
                fp.write(student + "\n")

            fp.write(f"\nDate: {datetime.datetime.now()}\n")
            fp.write("=" * 5)
        self.parent.current = "dashboard"
