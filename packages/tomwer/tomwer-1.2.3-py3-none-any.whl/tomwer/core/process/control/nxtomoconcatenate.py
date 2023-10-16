import os
import logging
from tomoscan.serie import Serie

from ewokscore.missing_data import is_missing_data

from tomwer.core.process.task import TaskWithProgress
from tomwer.core.scan.hdf5scan import HDF5TomoScan

from nxtomomill.nexus.nxtomo import NXtomo
from nxtomomill.nexus.utils import concatenate as nx_concatenate

_logger = logging.getLogger(__name__)


class ConcatenateNXtomoTask(
    TaskWithProgress,
    input_names=(
        "serie",
        "output_file",
        "output_entry",
        "overwrite",
    ),
    optional_input_names=(
        "progress",
        "serialize_output_data",
    ),
    output_names=("data",),
):
    """
    Task used to concatenate a list of NXtomo (HDF5TomoScan) into a single NXtomo
    """

    def run(self):
        scans_serie = self.inputs.serie
        if is_missing_data(scans_serie) or len(scans_serie) < 1:
            raise ValueError("expected at least one nxtomo to be concatenated")
        elif not isinstance(scans_serie, Serie):
            raise TypeError(f"serie is expected to be a Serie. Get {type(scans_serie)}")

        # format output location if necessary
        output_file = format_output_location(
            file_path=self.inputs.output_file, serie=scans_serie
        )

        # cast scan from HDF5tomoScan to NXtomo
        def cast_scan_to_nxtomo(obj: HDF5TomoScan):
            # convert HDF5Tomoscan to NXtomo as we expect to get HDF5TomoScan
            if isinstance(obj, HDF5TomoScan):
                return NXtomo().load(
                    file_path=obj.master_file,
                    data_path=obj.entry,
                )
            else:
                raise TypeError(
                    f"nxtomos are supposed to be instances of {NXtomo} or {HDF5TomoScan}. Get {type(obj)}"
                )

        scans_serie = tuple([cast_scan_to_nxtomo(nxtomo) for nxtomo in scans_serie])

        # apply concatenation
        output_nxtomo = nx_concatenate(scans_serie)

        # dump result
        output_nxtomo.save(
            file_path=output_file,
            data_path=self.inputs.output_entry,
            overwrite=self.inputs.overwrite,
        )

        # cast back nxtomomill NXtomo to HDF5TomoScan (reference object for tomwer)
        scan = HDF5TomoScan(
            scan=output_file,
            entry=self.inputs.output_entry,
        )
        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan


def format_output_location(file_path, serie: Serie):
    """
    format possible keys from the location like {scan_dir} or {scan_path}

    :param file_path:
    :param serie: serie of HDF5TomoScan
    :return:
    """
    if serie is None:
        _logger.warning("scan is !none, enable to format the nabu output location")

    for scan in serie:
        if not isinstance(scan, HDF5TomoScan):
            raise TypeError

    def get_common_path():
        if len(serie) == 0:
            return ""
        elif len(serie) == 1:
            return os.path.dirname(serie[0].master_file)
        else:
            return os.path.commonpath(
                [os.path.dirname(scan.master_file) for scan in serie]
            )

    keywords = {
        "common_path": get_common_path(),
    }

    # filter necessary keywords
    def get_necessary_keywords():
        import string

        formatter = string.Formatter()
        return [field for _, field, _, _ in formatter.parse(file_path) if field]

    requested_keywords = get_necessary_keywords()

    def keyword_needed(pair):
        keyword, _ = pair
        return keyword in requested_keywords

    keywords = dict(filter(keyword_needed, keywords.items()))
    file_path = file_path.format(**keywords)
    file_path = os.path.abspath(file_path)
    return file_path
