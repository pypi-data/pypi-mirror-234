import os
from tomoscan.serie import Serie

from tomwer.core.process.control.nxtomoconcatenate import (
    ConcatenateNXtomoTask,
    format_output_location,
)
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.utils.scanutils import MockHDF5


def test_concatenate_nx_tomo_task(tmp_path):
    """
    test execution of ConcatenateNXtomoTask with two HDF5TomoScan
    """
    scan_1 = MockHDF5(
        scan_path=os.path.join(tmp_path, "scan1"),
        n_proj=10,
        n_ini_proj=10,
        scan_range=180,
        dim=20,
        energy=12.3,
    ).scan
    scan_2 = MockHDF5(
        scan_path=os.path.join(tmp_path, "scan2"),
        n_proj=10,
        n_ini_proj=10,
        scan_range=180,
        dim=20,
        energy=12.3,
    ).scan

    output_scan_file = os.path.join(tmp_path, "concatenation.nx")
    assert not os.path.exists(output_scan_file)
    task = ConcatenateNXtomoTask(
        inputs={
            "serie": Serie(iterable=[scan_1, scan_2]),
            "output_file": output_scan_file,
            "output_entry": "my_entry",
            "overwrite": False,
            "serialize_output_data": False,
        }
    )
    task.run()
    assert isinstance(task.outputs.data, HDF5TomoScan)
    assert os.path.exists(output_scan_file)
    # note: correct processing of the concatenation is done at nxtomomill


def test_format_output_location():
    """test behavior of format_output_location"""
    scan1 = HDF5TomoScan(
        "/path/to/scan_1.nx",
        entry="entry0000",
    )
    scan2 = HDF5TomoScan(
        "/path/to/scan_2.nx",
        entry="entry0001",
    )
    assert (
        format_output_location(
            "{common_path}/concatenate.nx", Serie(iterable=[scan1, scan2])
        )
        == "/path/to/concatenate.nx"
    )

    assert format_output_location(
        "concatenate.nx", Serie([scan1, scan2])
    ) == os.path.abspath("concatenate.nx")

    assert (
        format_output_location(
            "{common_path}/concatenate.nx",
            Serie(
                iterable=[
                    scan1,
                ]
            ),
        )
        == "/path/to/concatenate.nx"
    )
