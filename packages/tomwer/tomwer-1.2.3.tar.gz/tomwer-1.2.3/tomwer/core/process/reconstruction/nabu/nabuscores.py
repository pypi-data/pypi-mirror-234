# coding: utf-8
###########################################################################
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
#############################################################################

"""contain utils for score process
"""

__authors__ = [
    "H.Payno",
]
__license__ = "MIT"
__date__ = "28/10/2021"

try:
    from nabu.pipeline.fullfield.reconstruction import (  # noqa F401
        FullFieldReconstructor,
    )
except (ImportError, OSError):
    try:
        from nabu.pipeline.fullfield.local_reconstruction import (  # noqa F401
            ChunkedReconstructor,
        )
    except (ImportError, OSError):
        # import of cufft library can bring an OSError if cuda not install
        has_nabu = False
    else:
        has_nabu = True
else:
    has_nabu = True
import logging
import os
from copy import deepcopy
from typing import Iterable, Optional, Union

from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from processview.core.manager.manager import ProcessManager

from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.process.reconstruction.nabu.nabuslices import (
    SingleSliceRunner,
    _NabuBaseReconstructor,
    generate_nabu_configfile,
)
from tomwer.core.process.reconstruction.nabu.target import Target
from tomwer.core.progress import Progress
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.slurm import is_slurm_available
from tomwer.utils import docstring

from ..nabu import settings as nabu_settings
from . import utils
from .nabucommon import ResultsLocalRun, ResultSlurmRun, ResultsWithStd

_logger = logging.getLogger(__name__)


def run_nabu_one_slice_several_config(
    scan: TomwerScanBase,
    nabu_configs: Union[list, tuple],
    cluster_config: Optional[dict],
    dry_run: bool,
    slice_index: Union[int, str],
    file_format: str,
    advancement: Optional[Progress] = None,
    process_id: Optional[int] = None,
    instanciate_classes_only: bool = False,
    output_file_prefix_pattern=None,
) -> tuple:
    """
    Run several reconstruction of a specific slice.

    :param scan: dataset
    :param Iterable nabu_configs: set of nabu configurations to be run
    :param bool dry_run:
    :param int slice_index: slice index to reconstruct or "middle"
    :param Progress advancement: optional class to display advancement
    :param Optional[int] process_id: id of the process requesting this computation
    :param Optional[dict] cluster_config: cluster configuration if
    :return: success, recons_urls (list of output urls), tuple of outs, tuples of errs, dict future_scans (key is cor, value is future_scan)
             if `instanciate_classes_only` set to True then return a list of :class:`_Reconstructor`
    :rtype: tuple
    """
    if cluster_config in (None, {}):
        target = Target.LOCAL
    elif isinstance(cluster_config, dict):
        if not is_slurm_available():
            raise RuntimeError("Slurm computation requested but unvailable")
        target = Target.SLURM
    else:
        raise TypeError(
            f"cluster_config should be None or a dict not {type(cluster_config)}"
        )

    if process_id is not None:
        try:
            process_name = ProcessManager().get_process(process_id=process_id).name
        except KeyError:
            process_name = "unknow"
    else:
        process_name = ""

    reconstructor = _Reconstructor(
        scan=scan,
        nabu_configs=nabu_configs,
        advancement=advancement,
        slice_index=slice_index,
        target=target,
        dry_run=dry_run,
        file_format=file_format,
        cluster_config=cluster_config,
        process_name=process_name,
        output_file_prefix_pattern=output_file_prefix_pattern,
    )
    if instanciate_classes_only:
        return (reconstructor,)

    try:
        results = reconstructor.run()
    except TimeoutError as e:
        _logger.error(e)
        return None
    else:
        assert isinstance(
            results, dict
        ), "results should be a dictionary with var_value as key and urls as value"
        success = True
        recons_urls = {}
        std_outs = []
        std_errs = []
        future_tomo_objs = {}
        for var_value, res in results.items():
            success = success and res.success
            if isinstance(res, ResultsWithStd):
                std_outs.append(res.std_out)
                std_errs.append(res.std_err)
            if isinstance(res, ResultsLocalRun):
                recons_urls[var_value] = res.results_urls
            if isinstance(res, ResultSlurmRun):
                future_tomo_obj = FutureTomwerObject(
                    tomo_obj=scan,
                    process_requester_id=process_id,
                    futures=res.future_slurm_jobs,
                )
                future_tomo_objs[var_value] = future_tomo_obj
        return success, recons_urls, std_outs, std_errs, future_tomo_objs


class _Reconstructor(_NabuBaseReconstructor):
    def __init__(
        self,
        scan: TomwerScanBase,
        nabu_configs: Iterable,
        advancement: Optional[Progress],
        slice_index: Union[int, str],
        target: Target,
        dry_run: bool,
        file_format: str,
        cluster_config: Optional[dict],
        process_name: str,
        output_file_prefix_pattern=None,
    ) -> None:
        """
        :param str extra_output_file_pattern: possible extra file name pattern like for cor we want to add 'cor_' as prefix and cor value as suffix.
                                              To make the file name unique. For delta/beta it is already forseen to be unique. For now keywords are:
                                              * file_name: default file name according to db values and dataset name
                                              * value: value of the nabu_configs keys
        """
        super().__init__(
            scan=scan,
            dry_run=dry_run,
            target=target,
            cluster_config=cluster_config,
            process_name=process_name,
        )
        if not isinstance(slice_index, (int, str)):
            raise TypeError(
                f"slice_index should be an int or a string not {type(slice_index)}"
            )

        self.advancement = advancement
        self.slice_index = slice_index
        self.nabu_configs = nabu_configs
        self.file_format = file_format
        self._output_file_prefix_pattern = output_file_prefix_pattern

    @docstring(_NabuBaseReconstructor)
    def run(self) -> Iterable:
        if self.slice_index == "middle":
            if self.scan.dim_2 is not None:
                self.slice_index = self.scan.dim_2 // 2
            else:
                _logger.warning(
                    "scan.dim_2 returns None, unable to deduce middle " "pick 1024"
                )
                self.slice_index = 1024

        results = {}
        if self.advancement:
            self.advancement.setMaxAdvancement(len(self.nabu_configs))
        for var_value, config in self.nabu_configs.items():
            if self._cancelled:
                break
            config, conf_file = self.preprocess_config(deepcopy(config), var_value)
            print("conf file is", conf_file)
            print("confif output is", config.get("output"))

            # add some tomwer metadata and save the configuration
            # note: for now the section is ignored by nabu but shouldn't stay that way
            with utils.TomwerInfo(config) as config_to_dump:
                generate_nabu_configfile(
                    conf_file,
                    nabu_fullfield_default_config,
                    config=config_to_dump,
                    options_level="advanced",
                )

            results[var_value] = self._process_config(
                config_to_dump=config_to_dump,
                config_file=conf_file,
                file_format=self.file_format,
                start_z=None,
                end_z=None,
                info="nabu slice reconstruction",
                process_name=self.process_name,
            )
            # specific treatment for cor: rename output files
            if self.advancement:
                self.advancement.increaseAdvancement(1)
        return results

    def _format_file_prefix(self, file_prefix, value):
        if self._output_file_prefix_pattern is None:
            return file_prefix

        keywords = {
            "file_name": file_prefix,
            "value": value,
        }

        # filter necessary keywords
        def get_necessary_keywords():
            import string

            formatter = string.Formatter()
            return [
                field
                for _, field, _, _ in formatter.parse(self._output_file_prefix_pattern)
                if field
            ]

        requested_keywords = get_necessary_keywords()

        def keyword_needed(pair):
            keyword, _ = pair
            return keyword in requested_keywords

        keywords = dict(filter(keyword_needed, keywords.items()))
        return self._output_file_prefix_pattern.format(**keywords)

    def treateOutputConfig(self, _config, value):
        """
        - add or overwrite some parameters of the dictionary
        - create the output directory if does not exist
        """
        pag = False
        ctf = False
        db = None
        if "phase" in _config:
            phase_method = _config["phase"].get("method", "").lower()
            if phase_method in ("pag", "paganin"):
                pag = True
            elif phase_method in ("ctf",):
                ctf = True

            if "delta_beta" in _config["phase"]:
                db = round(float(_config["phase"]["delta_beta"]))
        if "output" in _config:
            file_prefix = SingleSliceRunner.get_file_basename_reconstruction(
                scan=self.scan,
                slice_index=self.slice_index,
                pag=pag,
                db=db,
                ctf=ctf,
            )
            file_prefix = self._format_file_prefix(file_prefix=file_prefix, value=value)
            _config["output"]["file_prefix"] = file_prefix
            assert _config["output"]["location"] not in ("", None)
            if not os.path.isdir(_config["output"]["location"]):
                os.makedirs(_config["output"]["location"])

        if "reconstruction" not in _config:
            _config["reconstruction"] = {}
        _config["reconstruction"]["start_z"] = self.slice_index
        _config["reconstruction"]["end_z"] = self.slice_index
        return _config, file_prefix

    def preprocess_config(self, config, value: float):
        dataset_params = self.scan.get_nabu_dataset_info()
        if "dataset" in config:
            dataset_params.update(config["dataset"])
        config["dataset"] = dataset_params

        config["resources"] = utils.get_nabu_resources_desc(
            scan=self.scan, workers=1, method="local"
        )
        # force overwrite results
        if "output" not in config:
            config["output"] = {}
        config["output"].update({"overwrite_results": 1})

        config, file_prefix = self.treateOutputConfig(config, value=value)
        # the policy is to save nabu .cfg file at the same location as the
        # force overwrite results

        cfg_folder = os.path.join(
            config["output"]["location"],
            nabu_settings.NABU_CFG_FILE_FOLDER,
        )
        os.makedirs(cfg_folder, exist_ok=True)

        conf_file = os.path.join(
            cfg_folder, file_prefix + nabu_settings.NABU_CONFIG_FILE_EXTENSION
        )
        return config, conf_file
