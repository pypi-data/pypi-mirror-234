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
__date__ = "15/12/2021"


import logging
from typing import Optional

from silx.gui import qt
from silx.gui.utils import blockSignals

from tomwer.core.process.reconstruction.nabu.castvolume import (
    DEFAULT_OUTPUT_DIR,
    RESCALE_MAX_PERCENTILE,
    RESCALE_MIN_PERCENTILE,
)
from tomwer.core.process.reconstruction.nabu.nabucommon import NabuOutputFileFormat
from tomwer.gui.qlefilesystem import QLFileSystem
from tomwer.gui.reconstruction.nabu.nabuconfig.output import QNabuFileFormatComboBox
from nxtomomill.io.utils import convert_str_to_tuple

_logger = logging.getLogger(__name__)


class CastVolumeWidget(qt.QWidget):
    sigConfigChanged = qt.Signal()
    """Signal emit when the configuration changed"""

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

        self.setLayout(qt.QGridLayout())

        # output data size
        self._castToLabel = qt.QLabel("cast to", self)
        self._castToLabel.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.layout().addWidget(self._castToLabel, 0, 0, 1, 1)
        self._outputDataTypeCB = qt.QComboBox(self)
        for data_type in ("uint8", "uint16", "float32", "float64"):
            self._outputDataTypeCB.addItem(data_type)
        self.layout().addWidget(self._outputDataTypeCB, 0, 1, 1, 3)
        # output file format
        self._outputFileformatLabel = qt.QLabel("output file format", self)
        self.layout().addWidget(self._outputFileformatLabel, 1, 0, 1, 1)
        self._outputFileformatCB = QNabuFileFormatComboBox(self)
        self.layout().addWidget(self._outputFileformatCB, 1, 1, 1, 3)

        # let the user provide min and max manually
        self._minMaxLabel = qt.QLabel("min max values")
        self.layout().addWidget(self._minMaxLabel, 2, 0, 1, 1)
        self._minMaxAuto = qt.QCheckBox("auto with rescale from percentiles")
        self._minMaxAuto.setChecked(True)
        self._minMaxAuto.setToolTip(
            "If set to auto will try to get min/max pixel values from nabu histogram else will compute it. Otherwise will values provided by the user"
        )
        self.layout().addWidget(self._minMaxAuto, 2, 1, 1, 1)

        self._minPixValue = qt.QLineEdit("", self)
        self._minPixValue.setPlaceholderText("min")
        self._maxPixValue = qt.QLineEdit("", self)
        self._maxPixValue.setPlaceholderText("max")
        validator = qt.QDoubleValidator(self)
        validator.setNotation(qt.QDoubleValidator.ScientificNotation)
        self._minPixValue.setValidator(validator)
        self._maxPixValue.setValidator(validator)
        self.layout().addWidget(self._minPixValue, 4, 2, 1, 1)
        self.layout().addWidget(self._maxPixValue, 4, 3, 1, 1)
        self._minPixValue.setVisible(False)
        self._maxPixValue.setVisible(False)
        # or from percentiles
        self._percentilesLabel = qt.QLabel("rescale percentiles")
        self.layout().addWidget(self._percentilesLabel, 3, 1, 1, 1)
        self._lowPercentileQSB = qt.QSpinBox(self)
        self._lowPercentileQSB.setRange(0, 100)
        self._lowPercentileQSB.setPrefix("min:")
        self._lowPercentileQSB.setSuffix("%")
        self._lowPercentileQSB.setValue(RESCALE_MIN_PERCENTILE)
        self.layout().addWidget(self._lowPercentileQSB, 3, 2, 1, 1)
        self._highPercentileQSB = qt.QSpinBox(self)
        self._highPercentileQSB.setRange(0, 100)
        self._highPercentileQSB.setPrefix("max:")
        self._highPercentileQSB.setSuffix("%")
        self._highPercentileQSB.setValue(RESCALE_MAX_PERCENTILE)
        self.layout().addWidget(self._highPercentileQSB, 3, 3, 1, 1)
        # compression ratios for JP2K
        self._cRatiosLabel = qt.QLabel("compression ratios", self)
        self.layout().addWidget(self._cRatiosLabel, 5, 0, 1, 1)
        self._cRatiosQLE = qt.QLineEdit(self)
        fpm = "\\d*\\.?\\d+"  # float or int matching
        qRegExp = qt.QRegExp(
            "(" + fpm + "[;]?[,]?[ ]?){1,}" + "|" + ":".join((fpm, fpm, fpm))
        )
        self._cRatiosQLE.setValidator(qt.QRegExpValidator(qRegExp))
        self._cRatiosQLE.setPlaceholderText(
            "l1 compression rate, l2 compression rate..."
        )
        self._cRatiosQLE.setToolTip(
            "Optional list of int values defining the quality of the different layer. For example '20, 10, 1' will create 3 layers. The first one with a compression factor of 20, the second of 10 and the last will be lossless"
        )
        self.layout().addWidget(self._cRatiosQLE, 5, 1, 1, 3)
        # save dir
        self._saveDirLabel = qt.QLabel("output directory", self)
        self.layout().addWidget(self._saveDirLabel, 15, 0, 1, 1)
        self._useDefaultSaveDirQCB = qt.QCheckBox("default", self)
        self._useDefaultSaveDirQCB.setToolTip(
            f"Default directory is: {DEFAULT_OUTPUT_DIR}"
        )
        self._useDefaultSaveDirQCB.setSizePolicy(
            qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum
        )
        self._useDefaultSaveDirQCB.setChecked(True)
        self.layout().addWidget(self._useDefaultSaveDirQCB, 15, 1, 1, 1)
        self._saveDirQLE = QLFileSystem(text=DEFAULT_OUTPUT_DIR, parent=self)
        # force text because this is not a valid path
        self._saveDirQLE.setText(DEFAULT_OUTPUT_DIR)
        self._saveDirQLE.setToolTip(
            """
            can contains pattern / keywords. Those should be provided as '{keyword}'. Here are pattern currently handled:
            \n - 'volume_data_parent_folder': returns basename of the directory containing the volume (this will be the parent folder for edf, jp2k...)"
            """
        )
        self._saveDirQLE.setVisible(False)
        self.layout().addWidget(self._saveDirQLE, 15, 2, 1, 2)
        # overwrite
        self._overwriteCB = qt.QCheckBox("overwrite", self)
        self._overwriteCB.setChecked(True)
        self.layout().addWidget(self._overwriteCB, 16, 0, 1, 1)
        # spacer
        self._spacer = qt.QWidget(self)
        self._spacer.setSizePolicy(
            qt.QSizePolicy.MinimumExpanding, qt.QSizePolicy.Expanding
        )
        self.layout().addWidget(self._spacer, 99, 0, 1, 3)

        # set up
        self._updateCRatiosVis()

        # connect signal / slot
        self._outputFileformatCB.currentIndexChanged.connect(self._configChanged)
        self._outputFileformatCB.currentIndexChanged.connect(self._updateCRatiosVis)
        self._outputDataTypeCB.currentIndexChanged.connect(self._configChanged)
        self._saveDirQLE.editingFinished.connect(self._configChanged)
        self._useDefaultSaveDirQCB.toggled.connect(self._configChanged)
        self._overwriteCB.toggled.connect(self._configChanged)
        self._useDefaultSaveDirQCB.toggled.connect(self._updateOutputDirVis)
        self._minMaxAuto.toggled.connect(self._configChanged)
        self._minMaxAuto.toggled.connect(self._updatePixMinMaxVis)

    def _updateCRatiosVis(self, *args, **kwargs):
        self._cRatiosLabel.setVisible(
            self.getOutputFileFormat() == NabuOutputFileFormat.JP2K
        )
        self._cRatiosQLE.setVisible(
            self.getOutputFileFormat() == NabuOutputFileFormat.JP2K
        )

    def getOutputDataType(self) -> str:
        return self._outputDataTypeCB.currentText()

    def setOutputDataType(self, data_type) -> None:
        if hasattr(data_type, "value"):
            data_type = data_type.value
        idx = self._outputDataTypeCB.findText(data_type)
        if idx >= 0:
            self._outputDataTypeCB.setCurrentIndex(idx)

    def getOutputDir(self) -> str:
        if self._useDefaultSaveDirQCB.isChecked():
            return DEFAULT_OUTPUT_DIR
        else:
            return self._saveDirQLE.text()

    def setOutputDir(self, output_dir: str) -> None:
        self._useDefaultSaveDirQCB.setChecked(output_dir == DEFAULT_OUTPUT_DIR)
        self._saveDirQLE.setText(output_dir)

    def getOutputFileFormat(self) -> NabuOutputFileFormat:
        return NabuOutputFileFormat.from_value(self._outputFileformatCB.currentText())

    def setOutputFileformat(self, file_format: str) -> None:
        file_format = NabuOutputFileFormat.from_value(file_format)
        idx = self._outputFileformatCB.findText(file_format.value)
        if idx >= 0:
            self._outputFileformatCB.setCurrentIndex(idx)

    def getOverwrite(self) -> bool:
        return self._overwriteCB.isChecked()

    def setOverwrite(self, remove) -> None:
        self._overwriteCB.setChecked(remove)

    def getDataMin(self) -> Optional[float]:
        if (
            self._minMaxAuto.isChecked()
            or self._minPixValue.text().replace(" ", "") == ""
        ):
            return None
        else:
            return float(self._minPixValue.text())

    def setDataMin(self, value: Optional[float]) -> None:
        with blockSignals(self._minMaxAuto):
            self._minMaxAuto.setChecked(value is None)
        if value is not None:
            with blockSignals(self._minPixValue):
                self._minPixValue.setText(str(value))

    def getDataMax(self) -> Optional[float]:
        if (
            self._minMaxAuto.isChecked()
            or self._maxPixValue.text().replace(" ", "") == ""
        ):
            return None
        else:
            return float(self._maxPixValue.text())

    def setDataMax(self, value: Optional[float]) -> None:
        with blockSignals(self._minMaxAuto):
            self._minMaxAuto.setChecked(value is None)
        if value is not None:
            with blockSignals(self._maxPixValue):
                self._maxPixValue.setText(str(value))

    def setCompressionRatios(self, c_ratios: Optional[list]):
        if c_ratios in (None, tuple(), list()):
            c_ratios = ""
        self._cRatiosQLE.setText(str(c_ratios))

    def getCompressionRatios(self) -> tuple:
        if self.getOutputFileFormat() is NabuOutputFileFormat.JP2K:
            # for now the compression ratios are only handled for JP2K
            return tuple(
                [int(value) for value in convert_str_to_tuple(self._cRatiosQLE.text())]
            )
        else:
            return None

    def getConfiguration(self) -> dict:
        rescale_min_percentile, rescale_max_percentile = self.getRescalePercentiles()
        return {
            "output_data_type": self.getOutputDataType(),
            "output_type": self.getOutputFileFormat().value,
            "output_dir": self.getOutputDir(),
            "overwrite": self.getOverwrite(),
            "rescale_min_percentile": rescale_min_percentile,
            "rescale_max_percentile": rescale_max_percentile,
            "data_min": self.getDataMin(),
            "data_max": self.getDataMax(),
            "compression_ratios": self.getCompressionRatios(),
        }

    def getRescalePercentiles(self) -> tuple:
        return self._lowPercentileQSB.value(), self._highPercentileQSB.value()

    def setRescalePercentiles(self, low, high) -> tuple:
        if low is not None:
            self._lowPercentileQSB.setValue(low)
        if high is not None:
            self._highPercentileQSB.setValue(high)

    def setConfiguration(self, config: dict) -> None:
        output_data_type = config.get("output_data_type", None)
        if output_data_type is not None:
            self.setOutputDataType(output_data_type)
        output_file_format = config.get("output_file_format", None)
        if output_file_format is not None:
            self.setOutputFileformat(output_file_format)
        output_dir = config.get("output_dir", None)
        if output_dir is not None:
            self.setOutputDir(output_dir)
        overwrite = config.get("overwrite", None)
        if overwrite is not None:
            self.setOverwrite(overwrite)
        if "rescale_percentiles" in config:
            rescale_min_percentile, rescale_max_percentile = config[
                "rescale_percentiles"
            ]
            _logger.warning(
                "'rescale_percentiles' is deprecated. Please use 'rescale_min_percentile' and 'rescale_max_percentile' instead"
            )
        else:
            rescale_min_percentile = config.get("rescale_min_percentile", None)
            rescale_max_percentile = config.get("rescale_max_percentile", None)

        self.setRescalePercentiles(rescale_min_percentile, rescale_max_percentile)
        if "data_min" in config:
            self.setDataMin(config["data_min"])
        if "data_max" in config:
            self.setDataMax(config["data_max"])
        if "compression_ratios" in config:
            self.setCompressionRatios(config["compression_ratios"])

    def _configChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def _updateOutputDirVis(self, *args, **kwargs):
        self._saveDirQLE.setVisible(not self._useDefaultSaveDirQCB.isChecked())

    def _updatePixMinMaxVis(self, *args, **kwargs):
        self._minPixValue.setVisible(not self._minMaxAuto.isChecked())
        self._maxPixValue.setVisible(not self._minMaxAuto.isChecked())
        self._percentilesLabel.setVisible(self._minMaxAuto.isChecked())
        self._lowPercentileQSB.setVisible(self._minMaxAuto.isChecked())
        self._highPercentileQSB.setVisible(self._minMaxAuto.isChecked())
