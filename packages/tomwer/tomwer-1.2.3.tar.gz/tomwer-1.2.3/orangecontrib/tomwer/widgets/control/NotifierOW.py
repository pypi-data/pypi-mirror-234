# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "19/07/2018"

from orangewidget import gui, settings, widget
from orangewidget.widget import Input, Output
from silx.gui import qt

from tomwer.core.tomwer_object import TomwerObject


class NotifierWidgetOW(widget.OWBaseWidget):
    """
    simple widget which pop up and closes when recive a new object
    """

    name = "notifier"
    id = "orangecontrib.tomwer.widgets.control.NotifierOW"
    description = "Simple widget which pop up for 2 second when recives a new object"
    icon = "icons/notification.png"
    priority = 145
    keywords = ["control", "notifier", "notification"]

    want_main_area = True
    resizing_enabled = False

    _muted = settings.Setting(False)

    class Inputs:
        tomo_obj = Input(name="tomo_obj", type=TomwerObject, multiple=True)

    class Outputs:
        tomo_obj = Output(name="tomo_obj", type=TomwerObject)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pop_up = None
        layout = gui.vBox(self.mainArea, self.name).layout()
        self._soundButton = qt.QPushButton(parent=self)
        self._soundButton.setMinimumSize(150, 100)
        self._soundButton.setCheckable(True)
        layout.addWidget(self._soundButton)
        self._updateButtonIcon()

        # connect signal / slot
        self._soundButton.toggled.connect(self._switchMute)

    def _switchMute(self):
        self._muted = not self._muted

        self._updateButtonIcon()

    @Inputs.tomo_obj
    def process(self, tomo_obj, *args, **kwargs):
        self.notify(tomo_obj)
        self.Outputs.tomo_obj.send(tomo_obj)

    def _updateButtonIcon(self):
        style = qt.QApplication.style()
        if self._muted:
            icon = style.standardIcon(qt.QStyle.SP_MediaVolumeMuted)
        else:
            icon = style.standardIcon(qt.QStyle.SP_MediaVolume)
        self._soundButton.setIcon(icon)

    def notify(self, tomo_obj):
        if self.pop_up is not None:
            self.pop_up.close()

        if not self._muted:
            # emit sound when requested
            try:
                qt.QApplication.beep()
            except Exception:
                pass

        self.pop_up = NotificationMessage()
        text = f"Object {tomo_obj} received."
        self.pop_up.setText(text)
        self.pop_up.show()


class NotificationMessage(qt.QMessageBox):
    EXPOSITION_TIME = 3000  # in ms

    def __init__(self) -> None:
        super().__init__()
        self.setModal(False)
        self.setIcon(qt.QMessageBox.Information)
        self.addButton(
            f"Ok - will close automatically after {self.EXPOSITION_TIME / 1000}s",
            qt.QMessageBox.YesRole,
        )

    def show(self):
        super().show()
        timer = qt.QTimer(self)
        timer.singleShot(
            self.EXPOSITION_TIME,
            self.close,
        )
