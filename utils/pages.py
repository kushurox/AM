import uuid
from io import BytesIO
from kivymd.app import MDApp
import pyqrcode
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen


class Dashboard(MDScreen):
    def __init__(self, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)

    def to_attendance(self):
        # Make sure to save state before changing
        self.parent.STATE["attendance hash"] = str(uuid.uuid4())

        unique_hash = pyqrcode.create(self.parent.STATE["attendance hash"])
        unique_hash.png("tmp/current.png", scale=10, background=(128, 128, 128, 255))

        self.parent.current = "attendance"


class AttendancePage(MDScreen):

    def __init__(self, *args, **kwargs):
        super(AttendancePage, self).__init__(*args, **kwargs)

    def on_pre_enter(self, *args):
        self.ah.text = f'Attendance Hash: {self.parent.STATE["attendance hash"]}'
        self.qrcode_holder.source = "tmp/current.png"

