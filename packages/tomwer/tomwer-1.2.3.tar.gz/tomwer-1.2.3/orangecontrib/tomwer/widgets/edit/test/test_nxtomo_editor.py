import gc
import os
import pickle
import tempfile

import numpy
import pytest
from nxtomomill.nexus.nxtomo import NXtomo
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt
from tomoscan.esrf.scan.hdf5scan import ImageKey

from orangecontrib.tomwer.widgets.edit.NXtomoEditorOW import NXtomoEditorOW
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestNXtomoEditorOW(TestCaseQt):
    """Test that the NXtomoEditorOW widget work correctly. Processing test are done in the core module. gui test are done in the tomwer.gui.edit module"""

    def setUp(self):
        super().setUp()
        self._window = NXtomoEditorOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def getDefaultConfig(self) -> dict:
        return {
            "instrument.beam.energy": (5.9, False),
            "instrument.detector.distance": (2.4, True),
            "instrument.detector.field_of_view": ("Full", False),
            "instrument.detector.x_pixel_size": (0.023, True),
            "instrument.detector.y_pixel_size": (0.025, True),
            "instrument.detector.x_flipped": (True, True),
            "instrument.detector.y_flipped": (False, False),
        }

    def testSerialization(self):
        self._window.setConfiguration(self.getDefaultConfig())
        assert self._window.getConfiguration() == self.getDefaultConfig()
        pickle.dumps(self._window.getConfiguration())

    def testLiteralDumps(self):
        self._window.setConfiguration(self.getDefaultConfig())
        assert self._window.getConfiguration() == self.getDefaultConfig()
        literal_dumps(self._window.getConfiguration())

    def testAutomation(self):
        """
        test that if some field are locked then this will overwrite the Nxtomo and send the signal
        """
        signal_listener = SignalListener()
        self._window.sigScanReady.connect(signal_listener)
        # set up the widget to define and lock distance, energy and x pixel size
        distance_widget = self._window.widget.mainWidget._distanceMetricEntry
        distance_widget.setValue(0.6)
        distance_widget.setUnit("mm")
        distance_locker = self._window.widget.mainWidget._distanceLB
        distance_locker.setLock(True)
        energy_widget = self._window.widget.mainWidget._energyEntry
        energy_widget.setValue(88.058)
        energy_locker = self._window.widget.mainWidget._energyLockerLB
        energy_locker.setLock(True)
        x_pixel_widget = self._window.widget.mainWidget._xPixelSizeMetricEntry
        x_pixel_widget.setValue(45)
        x_pixel_widget.setUnit("nm")
        x_pixel_locker = self._window.widget.mainWidget._xPixelSizeLB
        x_pixel_locker.setLock(True)

        with tempfile.TemporaryDirectory() as tmp_dir:
            # 1.0 create nx tomos with raw data
            nx_tomo = NXtomo()
            nx_tomo.instrument.detector.x_pixel_size = 0.023
            nx_tomo.instrument.detector.y_pixel_size = 0.025
            nx_tomo.instrument.detector.field_of_view = "full"
            nx_tomo.instrument.detector.distance = 2.4
            nx_tomo.instrument.detector.x_flipped = False
            nx_tomo.instrument.detector.y_flipped = True
            nx_tomo.energy = 5.9
            nx_tomo.instrument.detector.image_key_control = [
                ImageKey.PROJECTION.value
            ] * 12
            nx_tomo.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
            nx_tomo.sample.rotation_angle = numpy.linspace(0, 20, num=12)

            file_path = os.path.join(tmp_dir, "nxtomo.nx")
            entry = "entry0000"
            nx_tomo.save(
                file_path=file_path,
                data_path=entry,
            )
            # 2.0 set scan to the nxtomo-editor
            scan = HDF5TomoScan(file_path, entry)
            self._window._setScan(scan=scan)
            self.qapp.processEvents()
            # 3.0 check results are as expected
            # make sure the scan has been re-emitted
            assert signal_listener.callCount() == 1
            # make sure the edition of the parameters have been done and only those
            overwrite_nx_tomo = NXtomo().load(
                file_path=file_path,
                data_path=entry,
                detector_data_as="as_numpy_array",
            )
            numpy.testing.assert_almost_equal(
                overwrite_nx_tomo.instrument.detector.x_pixel_size.value, 45e-9
            )
            assert (
                overwrite_nx_tomo.instrument.detector.y_pixel_size.value
                == nx_tomo.instrument.detector.y_pixel_size.value
            )
            assert (
                overwrite_nx_tomo.instrument.detector.field_of_view
                == nx_tomo.instrument.detector.field_of_view
            )
            numpy.testing.assert_almost_equal(
                overwrite_nx_tomo.instrument.detector.distance.value, 6.0e-4
            )
            assert (
                overwrite_nx_tomo.instrument.detector.x_flipped
                == nx_tomo.instrument.detector.x_flipped
            )
            assert (
                overwrite_nx_tomo.instrument.detector.y_flipped
                == nx_tomo.instrument.detector.y_flipped
            )
            numpy.testing.assert_almost_equal(overwrite_nx_tomo.energy.value, 88.058)
            numpy.testing.assert_array_almost_equal(
                overwrite_nx_tomo.instrument.detector.data,
                nx_tomo.instrument.detector.data,
            )
