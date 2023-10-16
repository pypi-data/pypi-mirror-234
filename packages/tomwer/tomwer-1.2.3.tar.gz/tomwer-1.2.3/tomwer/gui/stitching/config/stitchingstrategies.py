from typing import Union, Optional
from tomwer.io.utils.utils import str_to_dict

from nabu.stitching import config as stitching_config
from nabu.stitching.overlap import OverlapStitchingStrategy
from silx.gui import qt


class _StithcingHeightSpinBox(qt.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())
        self._autoCB = qt.QCheckBox("max", self)
        self.layout().addWidget(self._autoCB)
        self._stitchingHeight = qt.QSpinBox(self)
        self._stitchingHeight.setMinimum(3)
        self._stitchingHeight.setMaximum(999999)
        self._stitchingHeight.setValue(200)
        self.layout().addWidget(self._stitchingHeight)

        self._autoCB.toggled.connect(self._stitchingHeight.setDisabled)

    def getStitchingHeight(self) -> Optional[int]:
        if self._autoCB.isChecked():
            return None
        else:
            return self._stitchingHeight.value()

    def setStitchingHeight(self, height: Optional[int]) -> None:
        self._autoCB.setChecked(height is None)
        if height is not None:
            self._stitchingHeight.setValue(int(height))


class StitchingStrategies(qt.QWidget):
    """
    Defines algorithm and strategies to be used
    """

    DEFAULT_STITCHING_HEIGHT = None  # max value is the default

    sigChanged = qt.Signal()

    def __init__(self, parent=None, axis=0) -> None:
        super().__init__(parent)
        self.setLayout(qt.QFormLayout())
        self._stitchingStrategyCG = qt.QComboBox(parent=self)
        for strategy in OverlapStitchingStrategy.values():
            self._stitchingStrategyCG.addItem(strategy)
        self._stitchingStrategyCG.setToolTip(
            "stitcher behavior is also know as stitching strategy. It define the behavor to have on overlaping areas"
        )
        self.layout().addRow("stitcher behavior", self._stitchingStrategyCG)
        self._axis = axis

        self._stitchingHeight = _StithcingHeightSpinBox(parent=self)
        self._stitchingHeight.setStitchingHeight(self.DEFAULT_STITCHING_HEIGHT)
        self.layout().addRow("stitching height", self._stitchingHeight)

        # set up
        idx = self._stitchingStrategyCG.findText(
            OverlapStitchingStrategy.COSINUS_WEIGHTS.value
        )
        self._stitchingStrategyCG.setCurrentIndex(idx)

        # connect signal / slot
        self._stitchingStrategyCG.currentIndexChanged.connect(self._changed)

    def _changed(self, *args, **kwargs):
        self.sigChanged.emit()

    def getStitchingStrategy(self) -> OverlapStitchingStrategy:
        return OverlapStitchingStrategy.from_value(
            self._stitchingStrategyCG.currentText()
        )

    def setStitchingStrategy(self, strategy: Union[OverlapStitchingStrategy, str]):
        strategy = OverlapStitchingStrategy.from_value(strategy)
        idx = self._stitchingStrategyCG.findText(strategy.value)
        if idx >= 0:
            self._stitchingStrategyCG.setCurrentIndex(idx)

    def getConfiguration(self) -> dict:
        overlap_size = self._stitchingHeight.getStitchingHeight()
        if overlap_size is None:
            overlap_size = ""
        return {
            stitching_config.STITCHING_SECTION: {
                stitching_config.STITCHING_STRATEGY_FIELD: self.getStitchingStrategy().value,
                f"axis_{self._axis}_params": f"overlap_size={overlap_size}",
            }
        }

    def setConfiguration(self, config: dict):
        strategy = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.STITCHING_SECTION, None
        )
        if strategy is not None:
            self.setStitchingStrategy(strategy=strategy)

        axis_0_params_dict = str_to_dict(
            config.get(stitching_config.STITCHING_SECTION, {}).get(
                f"axis_{self._axis}_params", ""
            )
        )
        stitching_height = axis_0_params_dict.get(
            stitching_config.KEY_OVERLAP_SIZE, "unknown"
        )
        if stitching_height in ("None", "", None):
            self._stitchingHeight.setStitchingHeight(None)
        elif stitching_height != "unknown":
            self._stitchingHeight.setStitchingHeight(stitching_height)
