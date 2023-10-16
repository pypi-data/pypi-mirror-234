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


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "16/05/2023"


import pytest
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.gui.visualization.reconstructionparameters import ReconstructionParameters

from tomwer.tests.conftest import qtapp  # noqa F401


@pytest.mark.parametrize("phase_method", ("", "CTF", "Paganin"))
def test_ReconstructionParameters(qtapp, phase_method):  # noqa F401
    window = ReconstructionParameters()
    volume = HDF5Volume(
        file_path="test.hdf5",
        data_path="data",
        data=None,
        metadata={
            "nabu_config": {
                "reconstruction": {
                    "method": "FBP",
                },
                "phase": {
                    "method": phase_method,
                    "delta_beta": 110.0,
                },
            },
            "processing_options": {
                "reconstruction": {
                    "voxel_size_cm": (0.2, 0.2, 0.2),
                    "rotation_axis_position": 104,
                    "enable_halftomo": True,
                    "fbp_filter_type": "Hilbert",
                    "sample_detector_dist": 0.4,
                },
                "take_log": {
                    "log_min_clip": 1.0,
                    "log_max_clip": 10.0,
                },
            },
        },
    )
    window.setVolumeMetadata(metadata=volume.metadata)

    assert window._methodQLE.text() == "FBP"
    assert window._paganinQLE.text() == phase_method
    assert window._deltaBetaQLE.text() == "110.0"
    assert window._distanceQLE.text() == "0.4"
    assert window._pixelSizeQLE.text() == "0.2"
    assert window._corQLE.text() == "104.00"
    assert window._halfTomoCB.isChecked()
    assert window._fbpFilterQLE.text() == "Hilbert"
    assert window._minLogClipQLE.text() == "1.0"
    assert window._maxLogClipQLE.text() == "10.0"

    window.setVolumeMetadata(metadata=None)
