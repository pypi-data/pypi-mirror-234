#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import signal
import sys

from silx.gui import qt

from nabu.utils import Progress
from nabu.stitching.config import StitchingType

from tomwer.core.utils.resource import increase_max_number_file
from tomwer.core.process.stitching.nabustitcher import StitcherTask
from tomwer.io.utils.tomoobj import get_tomo_objs_instances
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.gui.stitching.stitching import ZStitchingWindow as _ZStitchingWindow
from tomwer.gui.cluster.slurm import SlurmSettingsWidget

logging.basicConfig(level=logging.WARNING)

_logger = logging.getLogger(__name__)


class MainWidget(qt.QTabWidget):
    DEFAULT_NB_WORKERS = 10

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._stitchingConfigWindow = _ZStitchingWindow(parent=self)
        self.addTab(self._stitchingConfigWindow, "stitching config")
        self._slurmConfig = SlurmSettingsWidget(
            parent=self, n_gpu=0, jobLimitation=None
        )
        self._slurmConfig.setNJobs(20)
        self._stitchingConfigWindow.setCallbackToGetSlurmConfig(
            self._slurmConfig.getConfiguration
        )
        self._stitchingConfigWindow.setCallbackToSetSlurmConfig(
            self._slurmConfig.setConfiguration
        )
        self.addTab(self._slurmConfig, "slurm config")
        # add an option to clearly activate / deactivate slurm config
        slurm_config_idx = self.indexOf(self._slurmConfig)
        self._slurmCB = qt.QCheckBox(self)
        self.tabBar().setTabButton(
            slurm_config_idx,
            qt.QTabBar.LeftSide,
            self._slurmCB,
        )
        self._slurmCB.setChecked(True)

        # set up
        self._slurmConfig.setNWorkers(self.DEFAULT_NB_WORKERS)

    def close(self):
        self._stitchingConfigWindow.close()
        # requested for the waiting plot update
        super().close()

    def keyPressEvent(self, event):
        """
        To shortcut orange and make sure the `F5` <=> refresh stitching preview
        """
        modifiers = event.modifiers()
        key = event.key()

        if key == qt.Qt.Key_F5:
            self._stitchingConfigWindow._trigger_update_preview()
        elif key == qt.Qt.Key_O and modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            self._stitchingConfigWindow._loadSettings()
        elif key == qt.Qt.Key_S and modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            self._stitchingConfigWindow._saveSettings()

    def getStitchingConfiguration(self) -> dict:
        return self._stitchingConfigWindow.getConfiguration()

    def getClusterConfig(self) -> dict:
        return self._slurmConfig.getConfiguration()

    # expose API
    def addTomoObj(self, *args, **kwargs):
        self._stitchingConfigWindow.addTomoObj(*args, **kwargs)

    def setStitchingType(self, stitching_type):
        self._stitchingConfigWindow.setStitchingType(stitching_type)

    def loadSettings(self, config_file):
        self._stitchingConfigWindow._loadSettings(config_file)


class _StitcherThread(qt.QThread):
    def __init__(self, parent, stitching_config, cluster_config) -> None:
        super().__init__(parent)
        assert isinstance(stitching_config, dict)
        assert isinstance(cluster_config, dict)
        self._stitching_config = stitching_config
        self._cluster_config = cluster_config

    def run(self):
        task = StitcherTask(
            inputs={
                "stitching_config": self._stitching_config,
                "cluster_config": self._cluster_config,
                "progress": Progress("stitching"),
                "serialize_output_data": False,
            },
        )

        if self._cluster_config in (None, {}):
            self._runLocally(task)
        else:
            self._runRemotly(task)

    def _runLocally(self, task):
        task.run()

    def _runRemotly(self, task):
        task.run()
        # wait for processing to be finished
        for future in task.outputs.future_tomo_obj.futures:
            future.result()
        # note: there is also a callback to aggregate result once all are finished.
        # so at this stage the final "nxtomo" or "volume" might not exists yet
        print("Add slurm job finished.")


class MainWindow(qt.QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self.setWindowTitle("tomwer z-stitching")
        self._mainWindow = MainWidget(parent=self)
        self.layout().addWidget(self._mainWindow)

        types = qt.QDialogButtonBox.Apply
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)
        self._buttons.button(qt.QDialogButtonBox.Apply).setText("Launch stitching")
        self._buttons.button(qt.QDialogButtonBox.Apply).clicked.connect(self.accept)

    def close(self):
        self._mainWindow.close()
        # requested for the waiting plot update
        super().close()

    def reject(self):
        self.close()
        super().reject()

    def accept(self):
        self.process_stitching()

    def process_stitching(self):
        self._processingThread = _StitcherThread(
            parent=self,
            stitching_config=self.getStitchingConfiguration(),
            cluster_config=self.getClusterConfig(),
        )
        self._processingThread.start()

    def disableSlurmconfig(self):
        self._mainWindow._slurmCB.setChecked(False)
        self._mainWindow._slurmCB.setCheckable(False)

        slurm_config_idx = self._mainWindow.indexOf(self._mainWindow._slurmConfig)

        self._mainWindow.setTabEnabled(
            slurm_config_idx,
            False,
        )
        self._mainWindow.setTabToolTip(
            slurm_config_idx,
            "not available because unable to find slurm command (computer is probably not a slurm client ?",
        )

    # expose API
    def addTomoObj(self, *args, **kwargs):
        self._mainWindow.addTomoObj(*args, **kwargs)

    def getClusterConfig(self) -> dict:
        if self._mainWindow._slurmCB.isChecked():
            return self._mainWindow.getClusterConfig()
        else:
            return {}

    def getStitchingConfiguration(self) -> dict:
        return self._mainWindow.getStitchingConfiguration()

    def setStitchingType(self, stitching_type):
        self._mainWindow.setStitchingType(stitching_type)

    def loadSettings(self, config_file: str):
        self._mainWindow.loadSettings(config_file)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "tomo_objs",
        help="All tomo objects to be stitched together",
        nargs="*",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )

    parser.add_argument(
        "--config",
        "--config-file",
        dest="config_file",
        default=None,
        help="Provide stitching configuration file to load parameters from it",
    )
    parser.add_argument(
        "--use-opengl-plot",
        help="Use OpenGL for plots (instead of matplotlib)",
        action="store_true",
        default=False,
    )

    options = parser.parse_args(argv[1:])

    if options.use_opengl_plot:
        import silx

        silx.config.DEFAULT_PLOT_BACKEND = "gl"

    if options.debug:
        logging.root.setLevel(logging.DEBUG)

    increase_max_number_file()

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication(["tomwer"])
    splash = getMainSplashScreen()
    qt.QApplication.processEvents()

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler

    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    window = MainWindow()
    window.setWindowFlags(qt.Qt.Window)

    window.show()
    from sluurp.utils import has_sbatch_available

    # load configuration is some provided
    if options.config_file is not None:
        window.loadSettings(options.config_file)

    if not has_sbatch_available():
        window.disableSlurmconfig()

    tomo_objs, (has_scans, has_vols) = get_tomo_objs_instances(options.tomo_objs)
    for tomo_obj in tomo_objs:
        window.addTomoObj(tomo_obj=tomo_obj)
    if has_scans and has_vols:
        _logger.warning(
            "seems like you have both volumes and scan on your inputs. Unable to stitch the two at the same time"
        )
    elif has_scans:
        window.setStitchingType(StitchingType.Z_PREPROC)
    elif has_vols:
        window.setStitchingType(StitchingType.Z_POSTPROC)

    window.setAttribute(qt.Qt.WA_DeleteOnClose)
    splash.finish(window)
    exit(app.exec_())


def getinputinfo():
    return "tomwer z-stitching [tomo objects]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.closeAllWindows()  # needed because get a waiting thread behind
    qt.QApplication.quit()


if __name__ == "__main__":
    main(sys.argv)
