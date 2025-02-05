import threading
from logging import Logger

import kvui
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.layout import Layout

from . import Rac2ProcedurePatch


class PatcherUI(App):
    def __init__(self, aprac2_path: str, output_path: str, logger: Logger):
        self.title = "Rac2 Patcher"
        self.icon = r"data/icon.png"
        self.aprac2_path = aprac2_path
        self.output_path = output_path
        self.logger = logger
        super(PatcherUI, self).__init__()

    def build(self) -> Layout:
        self.container = GridLayout()
        self.container.cols = 1

        self.progresstext = Label(text="Progress")
        self.container.add_widget(self.progresstext)
        self.indicatorbar = ProgressBar(size_hint_y=None, height=3)
        self.container.add_widget(self.indicatorbar)

        def update_bar(dt):
            self.indicatorbar.value = (self.indicatorbar.value + 1) % self.indicatorbar.max

        Clock.schedule_interval(update_bar, 1/60)

        return self.container

    def on_start(self):
        threading.Thread(target=self.patch).start()

    def patch(self):
        @mainthread
        def update_progress(msg: str, percent: float):
            self.progresstext.text = msg
            self.logger.info(f"{msg}")
            if percent >= 99:
                App.get_running_app().stop()

        aprac2 = Rac2ProcedurePatch()
        aprac2.read(self.aprac2_path)
        try:
            aprac2.patch_mmap(self.output_path, update_progress)
        except Exception as e:
            self.progresstext.text = f"Error\n\n{e.args[0]}\n\nYou can close this window when you are done reading."
