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


__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "03/08/2020"


import code
import logging

import tomwer.version
from tomwer.core.process.task import Task
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.core.utils.volumeutils import volume_identifier_to_volume

_logger = logging.getLogger(__name__)


class PythonScript(
    Task,
    optional_input_names=("data", "volume", "serialize_output_data"),
    output_names=("data", "volume"),
):
    def run(self):
        # load data
        scan = data_identifier_to_scan(self.inputs.data)
        if isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        elif isinstance(scan, (TomwerScanBase, type(None))):
            scan = scan
        else:
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed")
        # load volume
        volume = volume_identifier_to_volume(self.inputs.volume)

        cfg = self.get_configuration()
        interpreter = code.InteractiveConsole(locals={"in_data": scan})
        interpreter = code.InteractiveConsole(locals={"in_volume": volume})
        interpreter.runcode(cfg["scriptText"])
        out_data = data_identifier_to_scan(interpreter.locals.get("out_data"))
        out_volume = data_identifier_to_scan(interpreter.locals.get("out_volume"))

        # register process
        if isinstance(scan, EDFTomoScan):
            entry = None
        else:
            entry = scan.entry

        try:
            self.register_process(
                process_file=scan.process_file,
                entry=entry,
                configuration={"scriptText": self.get_configuration()["scriptText"]},
                results=None,
                process_index=scan.pop_process_index(),
                overwrite=True,
            )
        except Exception as e:
            _logger.error("Fail to register process. Error is " + str(e))

        if out_data is not None and self.get_input_value("serialize_output_data", True):
            self.outputs.data = out_data.to_dict()
        else:
            self.outputs.data = out_data
        self.outputs.volume = out_volume

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "Python script"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "Execute some random python code"
