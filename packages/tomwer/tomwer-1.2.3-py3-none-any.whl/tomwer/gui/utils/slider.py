# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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
#############################################################################*/
"""some utils relative to PyHST
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "17/02/2021"


import numpy
from silx.gui import qt


class LogSlider(qt.QWidget):
    """Slider to select a value with a QSlider displayed with log scale"""

    valueChanged = qt.Signal(float)
    """signal emitted when the value changed"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        # QSlider
        self._slider = qt.QSlider(self)
        self._slider.setOrientation(qt.Qt.Horizontal)
        self.layout().addWidget(self._slider, 0, 0, 1, 1)
        # Double spin box
        self._valueQBSB = qt.QDoubleSpinBox(self)
        self.layout().addWidget(self._valueQBSB, 0, 1, 1, 1)

        # connect signal / slot
        self._slider.valueChanged.connect(self._sliderValueChanged)
        self._valueQBSB.valueChanged.connect(self._qdsbValueChanged)
        # set up
        self.setRange(1, 100)
        self.setValue(5)

    def setSuffix(self, txt):
        self._valueQBSB.setSuffix(txt)

    def setPrefix(self, txt):
        self._valueQBSB.setPrefix(txt)

    def setRange(self, min_: float, max_: float) -> None:
        """
        Define slider range

        :param float min_:
        :param float max_:
        """
        if min_ <= 0.0 or max_ <= 0.0:
            raise ValueError("LogSlider can only handled positive values")
        self._valueQBSB.setRange(min_, max_)
        self._slider.setRange(int(numpy.log(min_)), int(numpy.log(max_)))

    def _sliderValueChanged(self, *args, **kwargs):
        old = self._valueQBSB.blockSignals(True)
        self._valueQBSB.setValue(numpy.exp(self._slider.value()))
        self._valueQBSB.blockSignals(old)
        self.valueChanged.emit(self.value())

    def _qdsbValueChanged(self, *args, **kwargs):
        old = self._slider.blockSignals(True)
        self._slider.setValue(int(numpy.log(self._valueQBSB.value())))
        self._slider.blockSignals(old)
        self.valueChanged.emit(self.value())

    def value(self):
        return self._valueQBSB.value()

    def setValue(self, value):
        self._valueQBSB.setValue(value)
