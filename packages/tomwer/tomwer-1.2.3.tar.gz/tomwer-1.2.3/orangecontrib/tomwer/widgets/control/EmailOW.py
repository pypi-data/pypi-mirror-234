from orangewidget import gui
from orangewidget.settings import Setting

from silx.gui import qt
from ewoksorange.bindings.owwidgets import OWEwoksWidgetNoThread

import tomwer.core.process.control.email
from tomwer.gui.control.email import Emailwidget
from tomwer.core.utils import concatenate_dict


class EmailOW(
    OWEwoksWidgetNoThread,
    ewokstaskclass=tomwer.core.process.control.email.TomoEmailTask,
):
    """
    This widget will browse a folder and sub folder to find valid tomo scan project.
    Contrary to the scan watcher it will parse all folder / sub folders then stop.
    """

    name = "email notifier"
    id = "orangecontrib.widgets.tomwer.control.EmailOW.EmailOW"
    description = (
        "This widget will send an email to receivers when the input is provided. \n"
    )
    icon = "icons/email.svg"
    priority = 146
    keywords = [
        "tomography",
        "tomwer",
        "tomo_obj",
        "email",
        "notifier",
        "notification",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _ewoks_default_inputs = Setting({"configuration": {}, "tomo_obj": None})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = Emailwidget(parent=self)

        self._box = gui.vBox(self.mainArea, self.name)
        layout = self._box.layout()
        layout.addWidget(self._widget)

        # load settings
        self._widget.setConfiguration(self._ewoks_default_inputs)

        # connect signal / slot
        self._widget.sigChanged.connect(self._updateSettings)

    def _updateSettings(self):
        self._ewoks_default_inputs = {
            "configuration": self.getConfiguration(),
            "tomo_obj": None,
        }

    # expose some API
    def getConfiguration(self) -> dict:
        return self._widget.getConfiguration()

    def setConfiguration(self, config: dict):
        self._widget.setConfiguration(config.get("configuration", {}))

    def get_task_inputs(self):
        return concatenate_dict(
            super().get_task_inputs(),
            {"configuration": self.getConfiguration()},
        )

    def sizeHint(self):
        return qt.QSize(500, 200)

    def _execute_ewoks_task(self, *args, **kwargs):
        arguments = self._get_task_arguments()
        if arguments.get("inputs", {}).get("tomo_obj", None) is not None:
            super()._execute_ewoks_task(*args, **kwargs)
