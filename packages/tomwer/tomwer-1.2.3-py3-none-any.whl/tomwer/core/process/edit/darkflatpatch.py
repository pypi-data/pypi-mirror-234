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
__date__ = "04/11/2020"


import nxtomomill.version
from nxtomomill.utils import add_dark_flat_nx_file
from silx.io.url import DataUrl
from silx.utils.deprecation import deprecated_warning, deprecated

from tomwer.core.process.task import Task
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.scanutils import data_identifier_to_scan


def apply_dark_flat_patch(scan: HDF5TomoScan, config: dict) -> TomwerScanBase:
    """

    :param scan:
    :param config:
    :return:
    """
    if not isinstance(scan, HDF5TomoScan):
        raise ValueError(
            f"Dark and flat patch only manage HDF5TomoScan and not {type(scan)}"
        )
    if config is None:
        return scan
    for param in ("darks_start", "darks_end", "flats_start", "flats_end"):
        if param not in config:
            config[param] = None

    add_dark_flat_nx_file(
        file_path=scan.master_file,
        entry=scan.entry,
        **config,
    )
    return scan


class DarkFlatPatchTask(
    Task,
    input_names=("data", "configuration"),
    output_names=("data",),
    optional_input_names=("serialize_output_data",),
):
    """
    Patch an existing NXtomo calling nxtomomill
    """

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            return
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"scan is expected to be a dict or an instance of TomwerScanBase. Not {type(scan)}"
            )
        if not isinstance(scan, HDF5TomoScan):
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed")

        config = self.inputs.configuration
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dict. {type(config)} provided")
        apply_dark_flat_patch(scan=scan, config=config)
        keys = config.keys()
        for key in keys:
            value = config[key]
            if isinstance(value, DataUrl):
                config[key] = value.path()

        with scan.acquire_process_file_lock():
            self.register_process(
                process_file=scan.process_file,
                entry=scan.entry,
                configuration=config,
                results={},
                process_index=scan.pop_process_index(),
                overwrite=True,
            )
        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan

    @staticmethod
    def program_name():
        return "nxtomomill.utils.change_image_key_control"

    @staticmethod
    def program_version():
        return nxtomomill.version.version

    @staticmethod
    def definition():
        return "Apply patch for dark and references on a scan (TomwerScanBase)"

    @deprecated(
        since_version="1.2",
        replacement="DarkFlatPatchTask.inputs.configuration",
        reason="ewoksification",
    )
    def get_configuration(self):
        """

        :return: configuration of the process
        :rtype: dict
        """
        return self.inputs.configuration

    @deprecated(
        since_version="1.2",
        replacement="DarkFlatPatchTask.inputs.configuration",
        reason="ewoksification",
    )
    def set_configuration(self, configuration: dict) -> None:
        self.inputs.configuration = configuration


class DarkFlatPatch(DarkFlatPatchTask):
    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        deprecated_warning(
            name="tomwer.core.process.edit.darkflatpatch.DarkFlatPatch",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="DarkFlatPatchTask",
        )
        super().__init__(varinfo, inputs, node_id, node_attrs, execinfo)
