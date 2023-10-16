from time import sleep

import panel

from fragile.core.api_classes import Callback


class PauseSwarm(Callback):
    def __init__(self, value: bool = True, sleep=0.0):
        super().__init__()
        self.pause_widget = panel.widgets.Toggle(name="Pause", value=value)
        self.sleep_widget = panel.widgets.FloatInput(
            name="Sleep after epoch",
            value=sleep,
            start=0.0,
            end=60,
            width=75,
        )

    def after_evolve(self):
        while self.pause_widget.value:
            sleep(0.1)
        sleep(self.sleep_widget.value)
