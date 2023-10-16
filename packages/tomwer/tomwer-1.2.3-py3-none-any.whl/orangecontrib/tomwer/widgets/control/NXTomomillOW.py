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
__date__ = "11/03/2020"

import logging
import os
from copy import copy

from nxtomomill.io.config import TomoHDF5Config as HDF5Config
from orangewidget import gui
from silx.gui import qt

from orangecontrib.tomwer.orange.managedprocess import TomwerWithStackStack
from orangecontrib.tomwer.widgets.control.NXTomomillMixIn import NXTomomillMixIn
from tomwer.core.process.control.nxtomomill import H5ToNxProcess
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan, HDF5TomoScanIdentifier
from tomwer.gui.control.datalist import BlissHDF5DataListMainWindow
from tomwer.gui.control.nxtomomill import NXTomomillInput, OverwriteMessage
from ewoksorange.bindings.owwidgets import invalid_data


logger = logging.getLogger(__name__)


class NXTomomillOW(
    TomwerWithStackStack,
    NXTomomillMixIn,
    ewokstaskclass=H5ToNxProcess,
):
    """
    Widget to allow user to pick some bliss files and that will convert them
    to HDF5scan.
    """

    name = "bliss(HDF5)-nxtomomill"
    id = "orange.widgets.tomwer.control.NXTomomillOW.NXTomomillOW"
    description = (
        "Read a bliss .h5 file and extract from it all possible"
        "NxTomo. When validated create a TomwerBaseScan for each "
        "file and entry"
    )
    icon = "icons/nxtomomill.svg"
    priority = 120
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "convert",
        "NXTomo",
        "tomography",
        "nxtomomill",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    CONFIG_CLS = HDF5Config

    LOGGER = logger

    def __init__(self, parent=None):
        TomwerWithStackStack.__init__(self, parent=parent)
        NXTomomillMixIn.__init__(self)
        _layout = gui.vBox(self.mainArea, self.name).layout()

        self.widget = BlissHDF5DataListMainWindow(parent=self)
        _layout.addWidget(self.widget)
        self.__request_input = True
        # do we ask the user for input if missing
        self._inputGUI = None
        """Gui with cache for missing field in files to be converted"""
        self._canOverwriteOutputs = False
        """Cache to know if we have to ask user permission for overwriting"""

        # expose API
        self.n_scan = self.widget.n_scan
        # alias used for the 'simple workflow' for now
        self.start = self._sendAll

        # connect signal / slot
        self.widget._sendButton.clicked.connect(self._sendAll)
        self.widget._sendSelectedButton.clicked.connect(self._sendSelected)
        self.widget.sigNXTomoCFGFileChanged.connect(self._saveNXTomoCfgFile)
        self.widget.sigUpdated.connect(self._updateSettings)

        # set default configuration is no existing configuration file defined in the settings
        self.update_default_inputs(
            h5_to_nx_configuration=HDF5Config().to_dict(),
        )
        self.task_output_changed_callbacks.add(self._notify_state)

        # handle settings
        self._loadSettings()

    def _updateSettings(self):
        self._scans = []
        for scan in self.widget.datalist._myitems:
            # kept for backward compatibility since 0.11. To be removed on the future version.
            if "@" in scan:
                entry, file_path = scan.split("@")
                hdf5_tomo_scan = HDF5TomoScan(entry=entry, scan=file_path)
                self.add(hdf5_tomo_scan)
            else:
                self._scans.append(scan)
        self._ewoks_default_inputs[  # pylint: disable=E1137
            "output_dir"
        ] = self.widget.getOutputFolder()

    @property
    def request_input(self):
        return self.__request_input

    @request_input.setter
    def request_input(self, request):
        self.__request_input = request

    def get_task_inputs(self):
        return {
            "h5_to_nx_configuration": self.__configuration_cache.to_dict(),
            "serialize_output_data": False,
        }

    def handleNewSignals(self) -> None:
        """Invoked by the workflow signal propagation manager after all
        signals handlers have been called.
        """
        # for now we want to avoid propagation any processing.
        # task will be executed only when the user validates the dialog
        h5_scan = super().get_task_inputs().get("hdf5_scan", None)
        if h5_scan is not None:
            if not isinstance(h5_scan, H5ToNxProcess):
                raise TypeError(
                    "hdf5_scan is expected to be an instance of HDF5TomoScan"
                )
            self.add(h5_scan.path)

    def _convertAndSend(self, bliss_url):
        """

        :param str bliss_url: string at entry@file format
        """
        logger.processStarted(f"Start translate {bliss_url} to NXTomo")
        self.__configuration_cache = HDF5Config.from_dict(
            copy(self.get_default_input_values()["h5_to_nx_configuration"])
        )

        identifier = HDF5TomoScanIdentifier.from_str(bliss_url)
        bliss_scan = BlissScan(
            master_file=identifier.file_path,
            entry=identifier.data_path,
            proposal_file=None,
        )

        output_file_path = H5ToNxProcess.deduce_output_file_path(
            bliss_scan.master_file,
            entry=bliss_scan.entry,
            outputdir=self.widget.getOutputFolder(),
            scan=bliss_scan,
        )

        self.__configuration_cache.input_file = bliss_scan.master_file
        self.__configuration_cache.output_file = output_file_path
        self.__configuration_cache.entries = (bliss_scan.entry,)
        self.__configuration_cache.single_file = False
        self.__configuration_cache.overwrite = True
        self.__configuration_cache.request_input = self.request_input
        self.__configuration_cache.file_extension = ".nx"

        self._processBlissScan(bliss_scan)

    def _userAgreeForOverwrite(self, file_path):
        if self._canOverwriteOutputs:
            return True
        else:
            msg = OverwriteMessage(self)
            text = "NXtomomill will overwrite \n %s. Do you agree ?" % file_path
            msg.setText(text)
            if msg.exec_():
                self._canOverwriteOutputs = msg.canOverwriteAll()
                return True
            else:
                return False

    def _processBlissScan(self, bliss_scan):
        if bliss_scan is None:
            return
        output_file_path = H5ToNxProcess.deduce_output_file_path(
            bliss_scan.master_file,
            entry=bliss_scan.entry,
            outputdir=self.widget.getOutputFolder(),
            scan=bliss_scan,
        )
        # check user has rights to write on the folder
        dirname = os.path.dirname(output_file_path)
        if os.path.exists(dirname) and not os.access(dirname, os.W_OK):
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Warning)
            text = f"You don't have write rights on '{dirname}'. Unable to generate the nexus file associated to {str(bliss_scan)}"
            msg.setWindowTitle("No rights to write")
            msg.setText(text)
            msg.show()
            return
        # check if need to overwrite the file
        elif os.path.exists(output_file_path):
            if not self._userAgreeForOverwrite(output_file_path):
                return

        # keep 'h5_to_nx_configuration' up to date according to input folder and output_file updates
        self.update_default_inputs(
            h5_to_nx_configuration=self.__configuration_cache.to_dict()
        )
        self._execute_ewoks_task(propagate=True)

    def _loadSettings(self):
        for scan in self._scans:
            assert isinstance(scan, str)
            try:
                self.widget.add(scan)
            except Exception as e:
                logger.error(f"Fail to add {scan}. Error is {e}")
            else:
                logger.warning(f"{scan} is an invalid link to a file")
        if "nxtomomill_cfg_file" in self._ewoks_default_inputs:  # pylint: disable=E1135
            nxtomo_cfg_file = self._ewoks_default_inputs[  # pylint: disable=E1136
                "nxtomomill_cfg_file"
            ]
            self.widget.setCFGFilePath(nxtomo_cfg_file)
        if "output_dir" in self._ewoks_default_inputs:  # pylint: disable=E1135
            self.widget.setOutputFolder(
                self._ewoks_default_inputs["output_dir"]  # pylint: disable=E1136
            )

    def getHDF5Config(self):
        configuration_file = self.widget.getCFGFilePath()
        if configuration_file in (None, ""):
            configuration = HDF5Config()
        else:
            try:
                configuration = HDF5Config.from_cfg_file(configuration_file)
            except Exception as e:
                logger.error(
                    f"Fail to use configuration file {configuration_file}. Error is {e}. No conversion will be done."
                )
                return None
        return configuration

    def _saveNXTomoCfgFile(self, cfg_file):
        super()._saveNXTomoCfgFile(cfg_file, keyword="h5_to_nx_configuration")

    def _sendSelected(self):
        """Send a signal for selected scans found to the next widget"""
        self._inputGUI = NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for bliss_url in self.widget.datalist.selectedItems():
            identifier = HDF5TomoScanIdentifier.from_str(bliss_url.text())
            self._inputGUI.setBlissScan(
                entry=identifier.data_path, file_path=identifier.file_path
            )
            self._convertAndSend(bliss_url.text())

    def _sendAll(self):
        """Send a signal for each scan found to the next widget"""
        self._inputGUI = NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for bliss_url in self.widget.datalist.selectedItems():
            identifier = HDF5TomoScanIdentifier.from_str(bliss_url.text())
            self._inputGUI.setBlissScan(
                entry=identifier.data_path, file_path=identifier.file_path
            )
            self._convertAndSend(bliss_url.text())

    def _notify_state(self):
        try:
            task_executor = self.sender()
            task_suceeded = task_executor.succeeded
            config = task_executor.current_task.inputs.h5_to_nx_configuration
            config = HDF5Config.from_dict(config)
            scan = task_executor.current_task.outputs.data
            if task_suceeded:
                self.notify_succeed(scan=scan)
            else:
                self.notify_failed(scan=scan)
        except Exception as e:
            logger.error(f"failed to handle task finished callback. Raiseon is {e}")

    def trigger_downstream(self) -> None:
        for ewoksname, var in self.get_task_outputs().items():
            # note: for now we want to trigger 'data' for each items of 'datas'
            if ewoksname == "datas" and not (
                invalid_data.is_invalid_data(var.value) or var.value is None
            ):
                for data in var.value:
                    channel = self._get_output_signal("data")
                    channel.send(data)
            else:
                super().trigger_downstream()
