import logging

from tomoscan.serie import Serie

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output
from orangecontrib.tomwer.orange.managedprocess import TomwerWithStackStack
from silx.gui import qt
from typing import Optional

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.process.control.nxtomoconcatenate import (
    ConcatenateNXtomoTask,
    format_output_location,
)

from tomwer.gui.control.serie.nxtomoconcatenate import NXtomoConcatenateWidget

_logger = logging.getLogger(__name__)


class NXtomoConcatenateOW(
    TomwerWithStackStack,
    ewokstaskclass=ConcatenateNXtomoTask,
):
    """
    widget used to call do a concatenation of a serie (of NXtomo) into a single Nxtomo

    :param parent: the parent widget
    """

    # note of this widget should be the one registered on the documentation
    name = "NXtomo concatenation"
    id = "orangecontrib.tomwer.widgets.control.NXtomoConcatenate.NXtomoConcatenate"
    description = "concatenate a serie (of NXtomo / HDF5TomoScan) into a single Nxtomo"
    icon = "icons/concatenate_nxtomos.svg"
    priority = 200
    keywords = [
        "tomography",
        "nabu",
        "reconstruction",
        "concatenate",
        "NXtomo",
        "data",
        "HDF5TomoScan",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _ewoks_default_inputs = Setting(
        {
            "serie": None,
            "output_file": "{common_path}/concatenate.nx",
            "output_entry": "entry0000",
            "overwrite": False,
        }
    )

    TIMEOUT = 30

    class Inputs:
        serie = Input(
            name="serie",
            type=Serie,
            doc="serie to concatenate",
            default=True,
            multiple=False,
        )

    class Outputs:
        data = Output(name="data", type=TomwerScanBase, doc="concatenated scan")

    LOGGER = _logger

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__serie = None

        # gui definition
        _layout = gui.vBox(self.mainArea, self.name).layout()
        self.widget = NXtomoConcatenateWidget(parent=self)
        _layout.addWidget(self.widget)

        ## connect signal / slot
        self.widget.sigConfigChanged.connect(self._updateSettings)

        self.task_output_changed_callbacks.add(self._notify_state)

        ## handle settings
        self._loadSettings()
        self.task_executor_queue.sigComputationStarted.connect(self._newTaskStarted)

    def _updateSettings(self):
        config = self.widget.getConfiguration()
        for key in ("output_file", "output_entry", "overwrite"):
            self._ewoks_default_inputs[key] = config[key]  # pylint: disable=E1137

    @property
    def request_input(self):
        return self.__request_input

    @request_input.setter
    def request_input(self, request):
        self.__request_input = request

    def get_task_inputs(self):
        assert self.__serie is not None
        return {
            "serie": self.__serie,
            "output_file": self.widget.getConfiguration()["output_file"],
            "output_entry": self.widget.getConfiguration()["output_entry"],
            "overwrite": self.widget.getConfiguration()["overwrite"],
        }

    def handleNewSignals(self) -> None:
        """Invoked by the workflow signal propagation manager after all
        signals handlers have been called.
        """
        # for now we want to avoid propagation any processing.
        # task will be executed only when the user validates the dialog
        data = super().get_task_inputs().get("data", None)
        if data is not None:
            if not isinstance(data, HDF5TomoScan):
                raise TypeError(
                    f"data is expected to be an instance of HDF5TomoScan. {type(data)} are not handled"
                )
            self.add(data.path)

    def _loadSettings(self):
        self.widget.setConfiguration(self._ewoks_default_inputs)

    def _newTaskStarted(self):
        try:
            task_executor = self.sender()
            scan_about_to_be_created = HDF5TomoScan(
                scan=format_output_location(
                    file_path=task_executor.current_task.inputs.output_file_path,
                    serie=task_executor.current_task.inputs.serie,
                ),
                entry=task_executor.current_task.inputs.output_entry,
            )
            self.notify_on_going(scan_about_to_be_created)
        except Exception:
            pass

    def _notify_state(self):
        try:
            task_executor = self.sender()
            task_suceeded = task_executor.succeeded
            scan = task_executor.current_task.outputs.data
            if task_suceeded:
                self.notify_succeed(scan=scan)
            else:
                self.notify_failed(scan=scan)
        except Exception as e:
            _logger.error(f"failed to handle task finished callback. Raiseon is {e}")

    @Inputs.serie
    def process_serie(self, serie: Optional[Serie]):
        self._process_serie(serie=serie)

    def _process_serie(self, serie: Optional[Serie]):
        if serie is None:
            return
        else:
            self.__serie = serie
            scan_about_to_be_created = HDF5TomoScan(
                scan=format_output_location(
                    file_path=self.getOutputFilePath(),
                    serie=serie,
                ),
                entry=self.getOutputEntry(),
            )
            self.notify_pending(scan=scan_about_to_be_created)
            self.execute_ewoks_task()

    def sizeHint(self) -> qt.QSize:
        return qt.QSize(500, 200)

    # expose API
    def getOutputFilePath(self) -> str:
        return self.widget.getOutputFilePath()

    def getOutputEntry(self) -> str:
        return self.widget.getOutputEntry()
