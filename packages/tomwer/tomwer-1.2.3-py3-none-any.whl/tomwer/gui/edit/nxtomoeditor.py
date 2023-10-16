import logging
import weakref
from typing import Optional

import h5py
import numpy
from silx.gui import qt
from silx.io.utils import h5py_read_dataset
from tomoscan.esrf.scan.hdf5scan import ImageKey
from tomoscan.io import HDF5File
from tomoscan.nexus.paths.nxtomo import get_paths as get_nexus_paths
from tomoscan.scanbase import _FOV

from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.gui.utils.scandescription import ScanNameLabelAndShape
from tomwer.gui.utils.unitsystem import MetricEntry
from tomwer.gui.edit.nxtomowarmer import NXtomoProxyWarmer

_logger = logging.getLogger(__name__)


class NXtomoEditorDialog(qt.QDialog):
    def __init__(self, parent=None, hide_lockers=True) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self.mainWidget = NXtomoEditor(parent=self, hide_lockers=hide_lockers)
        self.layout().addWidget(self.mainWidget)
        self._warmer = NXtomoProxyWarmer(parent=self)
        self.layout().addWidget(self._warmer)

        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self._buttons.button(qt.QDialogButtonBox.Ok).setText("validate")
        self.layout().addWidget(self._buttons)

    # expose API
    def setScan(self, scan):
        self.mainWidget.setScan(scan)
        self._warmer.setScan(scan)

    def overwriteNXtomo(self):
        self.mainWidget.overwriteNXtomo()

    def hasLockField(self) -> bool:
        return self.mainWidget.hasLockField()

    def getConfiguration(self) -> dict:
        return self.mainWidget.getConfiguration()

    def setConfiguration(self, config):
        self.mainWidget.setConfiguration(config)


class NXtomoEditor(qt.QWidget):
    """
    class to edit parameter of a NXtomo.
    The preliminary goal is to let the user define pixel / voxel position and x and z positions
    in order to simplify stitching down the line

    As energy and scan range was also often requested this part is also editable (user bonus ^^)
    """

    sigEditingFinished = qt.Signal()

    def __init__(self, parent=None, hide_lockers=True):
        super().__init__(parent)
        self._editableWidgets = []
        self._lockerPBs = []
        # list of all lockers
        self._scan = None
        self.setLayout(qt.QVBoxLayout())
        self._scanInfoQLE = ScanNameLabelAndShape(parent=self)
        self.layout().addWidget(self._scanInfoQLE)

        # nxtomo tree
        self._tree = qt.QTreeWidget(self)
        if hide_lockers:
            self._tree.setColumnCount(2)
            self._tree.setHeaderLabels(("entry", "value"))
        else:
            self._tree.setColumnCount(3)
            self._tree.setHeaderLabels(("entry", "value", "lockers"))
            self._tree.header().setStretchLastSection(False)
            self._tree.setColumnWidth(2, 20)
            self._tree.header().setSectionResizeMode(1, qt.QHeaderView.Stretch)
        self.layout().addWidget(self._tree)

        # 1: instrument
        self._instrumentQTWI = qt.QTreeWidgetItem(self._tree)
        self._instrumentQTWI.setText(0, "instrument")
        # handle energy
        self._beamQTWI = qt.QTreeWidgetItem(self._instrumentQTWI)
        self._beamQTWI.setText(0, "beam")
        self._energyQTWI = qt.QTreeWidgetItem(self._beamQTWI)
        self._energyQTWI.setText(0, "energy (keV)")
        self._energyEntry = EnergyEntry("", self)
        self._energyEntry.setPlaceholderText("energy in kev")
        self._tree.setItemWidget(self._energyQTWI, 1, self._energyEntry)
        self._editableWidgets.append(self._energyEntry)
        self._energyLockerLB = PadlockButton(self)
        self._energyLockerLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._energyLockerLB)
        self._tree.setItemWidget(self._energyQTWI, 2, self._energyLockerLB)

        # 1.1 detector
        self._detectorQTWI = qt.QTreeWidgetItem(self._instrumentQTWI)
        self._detectorQTWI.setText(0, "detector")
        ## pixel size
        self._xPixelSizeQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._xPixelSizeQTWI.setText(0, "x pixel size")
        self._xPixelSizeMetricEntry = MetricEntry("", parent=self)
        self._xPixelSizeMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(self._xPixelSizeQTWI, 1, self._xPixelSizeMetricEntry)
        self._editableWidgets.append(self._xPixelSizeMetricEntry)
        self._xPixelSizeLB = PadlockButton(self)
        self._xPixelSizeLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._xPixelSizeLB)
        self._tree.setItemWidget(self._xPixelSizeQTWI, 2, self._xPixelSizeLB)

        self._yPixelSizeQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._yPixelSizeQTWI.setText(0, "y pixel size")
        self._yPixelSizeMetricEntry = MetricEntry("", parent=self)
        self._yPixelSizeMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(self._yPixelSizeQTWI, 1, self._yPixelSizeMetricEntry)
        self._editableWidgets.append(self._yPixelSizeMetricEntry)
        self._yPixelSizeLB = PadlockButton(self)
        self._yPixelSizeLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._yPixelSizeLB)
        self._tree.setItemWidget(self._yPixelSizeQTWI, 2, self._yPixelSizeLB)

        ## distance
        self._sampleDetectorDistanceQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._sampleDetectorDistanceQTWI.setText(0, "distance")
        self._distanceMetricEntry = MetricEntry("", parent=self)
        self._distanceMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._sampleDetectorDistanceQTWI, 1, self._distanceMetricEntry
        )
        self._editableWidgets.append(self._distanceMetricEntry)
        self._distanceLB = PadlockButton(self)
        self._distanceLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._distanceLB)
        self._tree.setItemWidget(self._sampleDetectorDistanceQTWI, 2, self._distanceLB)

        ## field of view
        self._fieldOfViewQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._fieldOfViewQTWI.setText(0, "field of view")
        self._fieldOfViewCB = qt.QComboBox(self)
        for value in _FOV.values():
            self._fieldOfViewCB.addItem(value)
        self._tree.setItemWidget(self._fieldOfViewQTWI, 1, self._fieldOfViewCB)
        self._editableWidgets.append(self._fieldOfViewCB)
        self._fieldOfViewLB = PadlockButton(self)
        self._fieldOfViewLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._fieldOfViewLB)
        self._tree.setItemWidget(self._fieldOfViewQTWI, 2, self._fieldOfViewLB)

        ## x flipped
        self._xFlippedQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._xFlippedQTWI.setText(0, "x flipped")
        self._xFlippedCB = qt.QCheckBox("", self)
        self._tree.setItemWidget(self._xFlippedQTWI, 1, self._xFlippedCB)
        self._editableWidgets.append(self._xFlippedCB)
        self._xFlippedLB = PadlockButton(self)
        self._xFlippedLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._xFlippedLB)
        self._tree.setItemWidget(self._xFlippedQTWI, 2, self._xFlippedLB)
        ## y flipped
        self._yFlippedQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._yFlippedQTWI.setText(0, "y flipped")
        self._yFlippedCB = qt.QCheckBox("", self)
        self._tree.setItemWidget(self._yFlippedQTWI, 1, self._yFlippedCB)
        self._editableWidgets.append(self._yFlippedCB)
        self._yFlippedLB = PadlockButton(self)
        self._yFlippedLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._yFlippedLB)
        self._tree.setItemWidget(self._yFlippedQTWI, 2, self._yFlippedLB)
        # 2: sample
        self._sampleQTWI = qt.QTreeWidgetItem(self._tree)
        self._sampleQTWI.setText(0, "sample")
        ## x translation
        self._xTranslationQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._xTranslationQTWI.setText(0, "x translation")
        self._xTranslationQLE = _TranslationMetricEntry(name="", parent=self)
        self._tree.setItemWidget(self._xTranslationQTWI, 1, self._xTranslationQLE)
        self._editableWidgets.append(self._xTranslationQLE)

        ## z translation
        self._zTranslationQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._zTranslationQTWI.setText(0, "z translation")
        self._zTranslationQLE = _TranslationMetricEntry(name="", parent=self)
        self._tree.setItemWidget(self._zTranslationQTWI, 1, self._zTranslationQLE)
        self._editableWidgets.append(self._zTranslationQLE)

        # set up
        self._instrumentQTWI.setExpanded(True)
        self._sampleQTWI.setExpanded(True)
        self._beamQTWI.setExpanded(True)
        self._detectorQTWI.setExpanded(True)
        self.hideLockers(hide_lockers)

        # connect signal / slot
        self._energyEntry.editingFinished.connect(self._editingFinished)
        self._energyLockerLB.toggled.connect(self._editingFinished)
        self._xPixelSizeMetricEntry.editingFinished.connect(self._editingFinished)
        self._xPixelSizeLB.toggled.connect(self._editingFinished)
        self._yPixelSizeMetricEntry.editingFinished.connect(self._editingFinished)
        self._yPixelSizeLB.toggled.connect(self._editingFinished)
        self._distanceMetricEntry.editingFinished.connect(self._editingFinished)
        self._distanceLB.toggled.connect(self._editingFinished)
        self._fieldOfViewCB.currentIndexChanged.connect(self._editingFinished)
        self._fieldOfViewLB.toggled.connect(self._editingFinished)
        self._xFlippedCB.toggled.connect(self._editingFinished)
        self._xFlippedLB.toggled.connect(self._editingFinished)
        self._yFlippedCB.toggled.connect(self._editingFinished)
        self._yFlippedLB.toggled.connect(self._editingFinished)

    def _editingFinished(self, *args, **kwargs):
        self.sigEditingFinished.emit()

    def hasLockField(self) -> bool:
        """return True if the widget has at least one lock field"""
        return True in [locker.isLocked() for locker in self._lockerPBs]

    def hideLockers(self, hide: bool):
        for locker in self._lockerPBs:
            locker.setVisible(not hide)

    def getEditableWidgets(self):
        return self._editableWidgets

    def setScan(self, scan):
        if scan is None:
            self._scan = scan
        elif not isinstance(scan, HDF5TomoScan):
            raise TypeError(
                f"{scan} is expected to be an instance of {HDF5TomoScan}. Not {type(scan)}"
            )
        else:
            self._scan = weakref.ref(scan)
        self._scanInfoQLE.setScan(scan)
        # scan will only be read and not kept
        self.update_tree()

    def getScan(self):
        if self._scan is None or self._scan() is None:
            return None
        else:
            return self._scan()

    def update_tree(self):
        if self.getScan() is not None:
            for fct in (
                self._updateInstrument,
                self._updateSample,
            ):
                try:
                    fct()
                except Exception as e:
                    _logger.info(e)
            self._tree.resizeColumnToContents(0)

    def _updateInstrument(self):
        scan = self.getScan()
        if scan is None:
            return
        else:
            self._updateEnergy(scan=scan)
            self._updatePixelSize(scan=scan)
            self._updateFlipped(scan=scan)
            self._updateFieldOfView(scan=scan)
            self._updateDistance(scan=scan)

    def _updateSample(self):
        scan = self.getScan()
        if scan is None:
            return
        else:
            self._updateTranslations(scan=scan)

    def _updateTranslations(self, scan: HDF5TomoScan):
        assert isinstance(scan, HDF5TomoScan)

        # note: for now and in order to allow edition we expect to have at most a unique value. Will fail for helicoidal
        def reduce(values):
            if values is None:
                return None
            values = numpy.array(values)
            values = numpy.unique(
                values[scan.image_key_control == ImageKey.PROJECTION.value]
            )
            if values.size == 1:
                return values[0]
            elif values.size == 0:
                return None
            else:
                return f"{values[0]} ... {values[-1]}"

        x_translation = reduce(scan.x_translation)
        z_translation = reduce(scan.z_translation)
        self._xTranslationQLE.setValue(x_translation)
        self._zTranslationQLE.setValue(z_translation)

    def _updateFieldOfView(self, scan):
        if not self._fieldOfViewLB.isLocked():
            # if in ''auto mode: we want to overwrite the NXtomo existing value by the one of the GUI
            idx = self._fieldOfViewCB.findText(
                _FOV.from_value(scan.field_of_view).value
            )
            if idx > 0:
                self._fieldOfViewCB.setCurrentIndex(idx)

    def _updateFlipped(self, scan):
        if (not self._xFlippedLB.isLocked()) and scan.x_flipped is not None:
            self._xFlippedCB.setChecked(scan.x_flipped)
        if (not self._yFlippedLB.isLocked()) and scan.y_flipped is not None:
            self._yFlippedCB.setChecked(scan.y_flipped)

    def _updateDistance(self, scan):
        if not self._distanceLB.isLocked():
            # if in ''auto mode: we want to overwrite the NXtomo existing value by the one of the GUI
            self._distanceMetricEntry.setValue(scan.distance)

    def _updateEnergy(self, scan):
        assert isinstance(scan, HDF5TomoScan)
        if not self._energyLockerLB.isLocked():
            # if in ''auto mode: we want to overwrite the NXtomo existing value by the one of the GUI
            energy = scan.energy
            self._energyEntry.setValue(energy)

    def _updatePixelSize(self, scan):
        assert isinstance(scan, HDF5TomoScan)
        if not self._xPixelSizeLB.isLocked():
            x_pixel_size = scan.x_pixel_size
            self._xPixelSizeMetricEntry.setValue(x_pixel_size)
        if not self._yPixelSizeLB.isLocked():
            y_pixel_size = scan.y_pixel_size
            self._yPixelSizeMetricEntry.setValue(y_pixel_size)

    def getConfiguration(self) -> dict:
        """
        Return a dict with field full name as key
        and a tuple as value (field_value, is_locked)

        limitation: for now sample position are not handled because this is a 'corner case' for now
        """
        return {
            "instrument.beam.energy": (
                self._energyEntry.getValue(),
                self._energyLockerLB.isLocked(),
            ),
            "instrument.detector.x_pixel_size": (
                self._xPixelSizeMetricEntry.getValue(),
                self._xPixelSizeLB.isLocked(),
            ),
            "instrument.detector.y_pixel_size": (
                self._yPixelSizeMetricEntry.getValue(),
                self._yPixelSizeLB.isLocked(),
            ),
            "instrument.detector.distance": (
                self._distanceMetricEntry.getValue(),
                self._distanceLB.isLocked(),
            ),
            "instrument.detector.field_of_view": (
                self._fieldOfViewCB.currentText(),
                self._fieldOfViewLB.isChecked(),
            ),
            "instrument.detector.x_flipped": (
                self._xFlippedCB.isChecked(),
                self._xFlippedLB.isChecked(),
            ),
            "instrument.detector.y_flipped": (
                self._yFlippedCB.isChecked(),
                self._yFlippedLB.isChecked(),
            ),
        }

    def setConfiguration(self, config: dict):
        energy = config.get("instrument.beam.energy", None)
        if energy is not None:
            energy, energy_locked = energy
            self._energyEntry.setValue(energy)
            self._energyLockerLB.setLock(energy_locked)

        x_pixel_size = config.get("instrument.detector.x_pixel_size", None)
        if x_pixel_size is not None:
            x_pixel_size, x_pixel_size_locked = x_pixel_size
            self._xPixelSizeMetricEntry.setValue(x_pixel_size)
            self._xPixelSizeLB.setLock(x_pixel_size_locked)

        y_pixel_size = config.get("instrument.detector.y_pixel_size", None)
        if y_pixel_size is not None:
            y_pixel_size, y_pixel_size_locked = y_pixel_size
            self._yPixelSizeMetricEntry.setValue(y_pixel_size)
            self._yPixelSizeLB.setLock(y_pixel_size_locked)

        detector_sample_distance = config.get("instrument.detector.distance", None)
        if detector_sample_distance is not None:
            detector_sample_distance, distance_locked = detector_sample_distance
            self._distanceMetricEntry.setValue(detector_sample_distance)
            self._distanceLB.setLock(x_pixel_size_locked)

        field_of_view = config.get("instrument.detector.field_of_view", None)
        if field_of_view is not None:
            field_of_view, field_of_view_locked = field_of_view
            self._fieldOfViewCB.setCurrentText(field_of_view)
            self._fieldOfViewLB.setLock(field_of_view_locked)

        x_flipped = config.get("instrument.detector.x_flipped", None)
        if x_flipped is not None:
            x_flipped, x_flipped_locked = x_flipped
            x_flipped = x_flipped in (True, "True", "true")
            self._xFlippedCB.setChecked(x_flipped)
            self._xFlippedLB.setLock(x_flipped_locked)

        y_flipped = config.get("instrument.detector.y_flipped", None)
        if y_flipped is not None:
            y_flipped, y_flipped_locked = y_flipped
            y_flipped = y_flipped in (True, "True", "true")
            self._yFlippedCB.setChecked(y_flipped)
            self._yFlippedLB.setLock(y_flipped_locked)

    def clear(self):
        self._tree.clear()

    def overwriteNXtomo(self):
        """overwrite data on disk"""
        scan = self.getScan()
        if scan is None:
            _logger.warning("no scan found to be saved")
            return
        nexus_paths = get_nexus_paths(scan.nexus_version)
        assert isinstance(scan, HDF5TomoScan)
        with HDF5File(scan.master_file, mode="a") as h5f:
            entry = h5f[scan.entry]
            # overwrite energy
            energy = self._energyEntry.getValue()
            self.__write_to_file(
                entry=entry,
                path=nexus_paths.ENERGY_PATH,
                value=energy,
                name="energy",
                expected_type=float,
                units="kev",
            )
            # overwrite x pixel size
            self.__write_to_file(
                entry=entry,
                path=nexus_paths.X_PIXEL_SIZE_PATH,
                value=self._xPixelSizeMetricEntry.getValue(),
                name="x pixel size",
                expected_type=float,
                units="m",
            )
            # overwrite y pixel size
            self.__write_to_file(
                entry=entry,
                path=nexus_paths.Y_PIXEL_SIZE_PATH,
                value=self._yPixelSizeMetricEntry.getValue(),
                name="y pixel size",
                expected_type=float,
                units="m",
            )
            n_frames = len(scan.image_key_control)

            # overwrite x translation
            self.__write_to_file(
                entry=entry,
                path=nexus_paths.X_TRANS_PATH,
                value=self._xTranslationQLE.getValue(),
                name="x translation",
                expected_type=float,
                n_value=n_frames,
                units="m",
            )
            # overwrite z translation
            self.__write_to_file(
                entry=entry,
                path=nexus_paths.Z_TRANS_PATH,
                value=self._zTranslationQLE.getValue(),
                name="z translation",
                expected_type=float,
                n_value=n_frames,
                units="m",
            )
            # overwrite sample detector distance
            self.__write_to_file(
                entry=entry,
                path=nexus_paths.DISTANCE_PATH,
                value=self._distanceMetricEntry.getValue(),
                name="z translation",
                expected_type=float,
                units="m",
            )
            # overwrite FOV
            self.__write_to_file(
                entry=entry,
                path=nexus_paths.FOV_PATH,
                value=self._fieldOfViewCB.currentText(),
                name="field of view",
                expected_type=str,
            )
            # overwrite x flipped
            self.__write_to_file(
                entry=entry,
                path="/".join(
                    (
                        nexus_paths.INSTRUMENT_PATH,
                        nexus_paths.nx_instrument_paths.DETECTOR_PATH,
                        nexus_paths.nx_detector_paths.X_FLIPPED,
                    )
                ),
                value=self._xFlippedCB.isChecked(),
                name="x flipped",
                expected_type=bool,
            )
            # overwrite y flipped
            self.__write_to_file(
                entry=entry,
                path="/".join(
                    (
                        nexus_paths.INSTRUMENT_PATH,
                        nexus_paths.nx_instrument_paths.DETECTOR_PATH,
                        nexus_paths.nx_detector_paths.Y_FLIPPED,
                    )
                ),
                value=self._yFlippedCB.isChecked(),
                name="y flipped",
                expected_type=bool,
            )
            # clear caches to make sure all modifications will be considered
            scan.clear_caches()
            scan.clear_frames_caches()

    @staticmethod
    def _newValueIsExistingValue(dataset: h5py.Dataset, new_value, units):
        """
        return true if the given value is same as the one stored
        """
        current_value = h5py_read_dataset(dataset)
        attrs = dataset.attrs
        current_unit = attrs.get("units", attrs.get("unit", None))
        if units != current_unit:
            # if the unit is not the same, eithen if the value is the same we will overwrite it
            return False
        else:
            if isinstance(new_value, numpy.ndarray) and isinstance(
                current_value, numpy.ndarray
            ):
                return numpy.array_equal(new_value, current_value)
            elif numpy.isscalar(current_value) and numpy.isscalar(new_value):
                return current_value == new_value
            else:
                return False

    @staticmethod
    def __write_to_file(entry, path, value, name, expected_type, n_value=1, units=None):
        if path is None:
            # if the path does not exists (no handled by this version of nexus for example)
            return

        # try to cast the value
        if isinstance(value, str):
            value = value.replace(" ", "")
            if value.lower() == "none" or "..." in value:
                # if value is not defined or is an array not overwrite by the user (case of the ... )
                return
        elif value is None:
            pass
        else:
            try:
                value = expected_type(value)
            except (ValueError, TypeError) as e:
                _logger.error(f"Fail to overwrite {name} of {entry.name}. Error is {e}")
                return

        if path in entry:
            if NXtomoEditor._newValueIsExistingValue(
                dataset=entry[path], new_value=value, units=units
            ):
                # if no need to overwrite
                return
            else:
                del entry[path]
        if value is None:
            return
        elif n_value == 1:
            entry[path] = value
        else:
            entry[path] = numpy.array([value] * n_value)
        if units is not None:
            entry[path].attrs["units"] = units


class _TranslationMetricEntry(MetricEntry):
    LOADED_ARRAY = "loaded array"

    class TranslationValidator(qt.QDoubleValidator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setNotation(qt.QDoubleValidator.ScientificNotation)

        def validate(self, a0: str, a1: int):
            if "..." in a0:
                return (qt.QDoubleValidator.Acceptable, a0, a1)
            else:
                return super().validate(a0, a1)

    def __init__(self, name, default_unit="m", parent=None):
        super().__init__(name, default_unit=default_unit, parent=parent)
        self._qlePixelSize.setValidator(self.TranslationValidator(self))

    def getValue(self):
        """

        :return: the value in meter
        :rtype: float
        """
        if "..." in self._qlePixelSize.text():
            # in this case this is the representation of an array, we don;t wan't to overwrite it
            return self.LOADED_ARRAY
        if self._qlePixelSize.text() in ("unknown", ""):
            return None
        else:
            return float(self._qlePixelSize.text()) * self.getCurrentUnit()


class EnergyEntry(qt.QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setValidator(MetricEntry.DoubleValidator())

    def setValue(self, a0):
        if a0 is None:
            a0 = "unknown"
        else:
            a0 = str(a0)
        super().setText(a0)

    def getValue(self) -> Optional[float]:
        txt = self.text().replace(" ", "")
        if txt in ("unknown", ""):
            return None
        else:
            return float(txt)
