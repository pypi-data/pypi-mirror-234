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
__date__ = "30/07/2020"


import logging
import os
import pathlib

from nxtomomill import converter as nxtomomill_converter
from nxtomomill.io.config import TomoEDFConfig as EDFConfig
from nxtomomill.io.config import TomoHDF5Config as HDF5Config
from nxtomomill.converter.hdf5.utils import get_default_output_file

from tomwer.core.process.task import TaskWithProgress
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.utils.scanutils import format_output_location

from silx.utils.enum import Enum as _Enum

_logger = logging.getLogger(__name__)


class NXtomomillNXDefaultOutput(_Enum):
    NEAR_INPUT_FILE = "near input"
    PROCESSED_DATA = "processed data dir"


class H5ToNxProcess(
    TaskWithProgress,
    input_names=("h5_to_nx_configuration",),
    optional_input_names=(
        "progress",
        "hdf5_scan",
        "serialize_output_data",
    ),
    output_names=("data", "datas"),
):
    """
    Task to convert from a bliss dataset to a nexus compliant dataset
    """

    @staticmethod
    def deduce_output_file_path(master_file_name, scan, entry, outputdir):
        assert isinstance(outputdir, str), "outputdir is expected to be a str"

        master_file_name = os.path.realpath(master_file_name)
        # step 1: get output dir
        try:
            outputdir = NXtomomillNXDefaultOutput.from_value(outputdir)
        except ValueError:
            output_folder = format_output_location(outputdir, scan=scan)
        else:
            if outputdir is NXtomomillNXDefaultOutput.PROCESSED_DATA:
                path = pathlib.Path(
                    get_default_output_file(input_file=master_file_name)
                )
                output_folder = str(path.parent)
            elif outputdir is NXtomomillNXDefaultOutput.NEAR_INPUT_FILE:
                output_folder = os.path.dirname(master_file_name)
            else:
                raise RuntimeError(f"output dir {outputdir} not handled")

        file_name = os.path.basename(master_file_name)
        if "." in file_name:
            file_name = "".join(file_name.split(".")[:-1])

        entry_for_file_name = entry.lstrip("/")
        entry_for_file_name = entry_for_file_name.replace("/", "_")
        entry_for_file_name = entry_for_file_name.replace(".", "_")
        entry_for_file_name = entry_for_file_name.replace(":", "_")
        output_file_name = "_".join(
            (os.path.splitext(file_name)[0], entry_for_file_name + ".nx")
        )
        return os.path.join(output_folder, output_file_name)

    def run(self):
        config = self.inputs.h5_to_nx_configuration
        if isinstance(config, dict):
            config = HDF5Config.from_dict(config)
        elif not isinstance(config, HDF5Config):
            raise TypeError(
                "h5_to_nx_configuration should be a dict or an instance of {HDF5Config}"
            )
        config.bam_single_file = True
        try:
            convs = nxtomomill_converter.from_h5_to_nx(
                configuration=config, progress=self.progress
            )
        except Exception as e:
            _logger.error(e)
            return

        if len(convs) == 0:
            return

        datas = []
        for conv in convs:
            conv_file, conv_entry = conv
            scan_converted = HDF5TomoScan(scan=conv_file, entry=conv_entry)
            _logger.processSucceed(
                f"{config.input_file} {config.entries} has been translated to {scan_converted}"
            )
            if self.get_input_value("serialize_output_data", True):
                data = scan_converted.to_dict()
            else:
                data = scan_converted
            datas.append(data)
        self.outputs.datas = datas
        self.outputs.data = datas[-1] if len(datas) > 0 else None


class EDFToNxProcess(
    TaskWithProgress,
    input_names=("edf_to_nx_configuration",),
    optional_input_names=(
        "progress",
        "edf_scan",
        "serialize_output_data",
    ),
    output_names=("data",),
):
    """
    Task calling edf2nx in order to insure conversion from .edf to .nx (create one NXtomo to be used elsewhere)
    """

    def run(self):
        config = self.inputs.edf_to_nx_configuration
        if isinstance(config, dict):
            config = EDFConfig.from_dict(config)
        elif not isinstance(config, EDFConfig):
            raise TypeError(
                "edf_to_nx_configuration should be a dict or an instance of {TomoEDFConfig}"
            )
        file_path, entry = nxtomomill_converter.from_edf_to_nx(
            configuration=config, progress=self.progress
        )
        scan = HDF5TomoScan(entry=entry, scan=file_path)
        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan

    @staticmethod
    def deduce_output_file_path(folder_path, output_dir, scan):
        if output_dir in (None, NXtomomillNXDefaultOutput.NEAR_INPUT_FILE.value):
            output_folder = os.path.dirname(folder_path)
        elif output_dir == NXtomomillNXDefaultOutput.PROCESSED_DATA.value:
            path = pathlib.Path(get_default_output_file(folder_path))
            output_folder = str(path.parent)
        else:
            output_folder = format_output_location(output_dir, scan=scan)
        print("output output_folder is", output_folder)
        return os.path.join(output_folder, os.path.basename(folder_path) + ".nx")
