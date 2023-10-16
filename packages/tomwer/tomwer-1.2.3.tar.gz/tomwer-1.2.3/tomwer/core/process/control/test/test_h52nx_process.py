import os
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.process.control.nxtomomill import (
    EDFToNxProcess,
    H5ToNxProcess,
    NXtomomillNXDefaultOutput,
)
from tomwer.core.utils.scanutils import MockHDF5, MockEDF
from nxtomomill.converter.hdf5.utils import PROCESSED_DATA_DIR_NAME, RAW_DATA_DIR_NAME


def test_h52nx_process_deduce_output_file_path(tmp_path):
    """test H5ToNxProcess.deduce_output_file_path function"""
    scan_path = str(tmp_path / "path" / RAW_DATA_DIR_NAME / "my_scan")
    os.makedirs(scan_path)

    scan = MockHDF5(scan_path=scan_path, n_proj=0).scan

    # test H52NXDefaultOutput.PROCESSED_DATA
    assert H5ToNxProcess.deduce_output_file_path(
        master_file_name=scan.master_file,
        scan=scan,
        entry=scan.entry,
        outputdir=NXtomomillNXDefaultOutput.PROCESSED_DATA.value,
    ) == str(
        tmp_path
        / "path"
        / PROCESSED_DATA_DIR_NAME
        / "my_scan"
        / f"my_scan_{scan.entry}.nx"
    )

    # test H52NXDefaultOutput.NEAR_BLISS_FILE
    assert H5ToNxProcess.deduce_output_file_path(
        master_file_name=scan.master_file,
        scan=scan,
        entry=scan.entry,
        outputdir=NXtomomillNXDefaultOutput.NEAR_INPUT_FILE.value,
    ) == str(
        tmp_path / "path" / RAW_DATA_DIR_NAME / "my_scan" / f"my_scan_{scan.entry}.nx"
    )

    # test providing output dir with some formatting to be done
    assert H5ToNxProcess.deduce_output_file_path(
        master_file_name=scan.master_file,
        scan=scan,
        entry=scan.entry,
        outputdir="{scan_parent_dir_basename}/../../toto/{scan_dir_name}",
    ) == str(tmp_path / "toto" / "my_scan" / f"my_scan_{scan.entry}.nx")

    # test providing output folder directly
    assert (
        H5ToNxProcess.deduce_output_file_path(
            master_file_name=scan.master_file,
            scan=scan,
            entry=scan.entry,
            outputdir="/tmp/",
        )
        == "/tmp/my_scan_entry.nx"
    )


def test_edf2nx_process_deduce_output_file_path(tmp_path):
    """test EDFToNxProcess.deduce_output_file_path function"""
    scan_path = str(tmp_path / "path" / RAW_DATA_DIR_NAME / "my_edf_scan")
    MockEDF(
        scan_path=scan_path,
        n_radio=10,
        n_ini_radio=10,
        n_extra_radio=0,
        dim=128,
        dark_n=1,
        flat_n=1,
    )
    scan = EDFTomoScan(scan_path)

    # test NEAR_INPUT_FILE
    assert EDFToNxProcess.deduce_output_file_path(
        folder_path=scan_path,
        output_dir=NXtomomillNXDefaultOutput.NEAR_INPUT_FILE.value,
        scan=scan,
    ) == os.path.join(tmp_path, "path", RAW_DATA_DIR_NAME, "my_edf_scan.nx")

    # test PROCESSED_DATA
    assert EDFToNxProcess.deduce_output_file_path(
        folder_path=scan_path,
        output_dir=NXtomomillNXDefaultOutput.PROCESSED_DATA.value,
        scan=scan,
    ) == os.path.join(tmp_path, "path", PROCESSED_DATA_DIR_NAME, "my_edf_scan.nx")

    # test providing output dir with some formatting to be done
    assert EDFToNxProcess.deduce_output_file_path(
        folder_path=scan_path,
        output_dir="{scan_parent_dir_basename}/../../toto/",
        scan=scan,
    ) == str(tmp_path / "toto" / "my_edf_scan.nx")

    # test providing output folder directly
    assert (
        EDFToNxProcess.deduce_output_file_path(
            folder_path=scan_path,
            output_dir="/tmp/output",
            scan=scan,
        )
        == "/tmp/output/my_edf_scan.nx"
    )
