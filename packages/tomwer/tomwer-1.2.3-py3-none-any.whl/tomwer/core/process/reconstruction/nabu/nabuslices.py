# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2020 European Synchrotron Radiation Facility
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
__date__ = "26/10/2021"


import copy
import functools
import logging
import os
import gc
from tomwer.io.utils import format_stderr_stdout
from silx.utils.deprecation import deprecated, deprecated_warning

from processview.core.manager.manager import ProcessManager, DatasetState

from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.core.utils.slurm import is_slurm_available

try:
    from nabu.pipeline.fullfield.reconstruction import (  # noqa F401
        FullFieldReconstructor,
    )
except (ImportError, OSError) as e:
    _err_import_nabu = e
    try:
        from nabu.pipeline.fullfield.local_reconstruction import (  # noqa F401
            ChunkedReconstructor,
        )
    except (ImportError, OSError):
        # import of cufft library can bring an OSError if cuda not install
        has_nabu = False
    else:
        has_nabu = True
        _err_import_nabu = None
else:
    has_nabu = True
    _err_import_nabu = None

from typing import Iterable, Optional, Union

from nabu import version as nabu_version
from nabu.pipeline.config import (
    _extract_nabuconfig_keyvals,
    generate_nabu_configfile,
    get_default_nabu_config,
)
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from processview.core.superviseprocess import SuperviseProcess
from silx.io.dictdump import h5todict
from silx.io.utils import h5py_read_dataset
from silx.utils.enum import Enum as _Enum
from tomoscan.io import HDF5File

from tomwer.core.process.task import Task
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.io.utils.h5pyutils import EntryReader
from tomwer.utils import docstring

from . import settings as nabu_settings
from . import utils
from .nabucommon import (
    ResultsLocalRun,
    ResultSlurmRun,
    ResultsRun,
    _NabuBaseReconstructor,
)
from .target import Target

_logger = logging.getLogger(__name__)
if not has_nabu:
    _logger.error(_err_import_nabu)


def run_slices_reconstruction(
    scan: TomwerScanBase,
    config: dict,
    dry_run: bool = False,
    advancement=None,
    process_id=None,
    instanciate_classes_only: bool = False,
) -> tuple:
    """
    call nabu for a reconstruction on scan with the given configuration

    :param TomwerScanBase scan: scan to reconstruct
    :param dict config: configuration to run the reconstruction.
                        Contains nabu reconstruction parameters and slurm cluster
                        configruation if requested (key: `slurm-cluster`).
    :param bool dry_run: do we want to run dry
    :param bool local: do we want to run a local reconstruction
    :param stderr: file to redirect stderr
    :param stdout: file to redirect stdout
    :param advancement: optional Progress class to display advancement
    :param int process_id: optional process id
    :param bool instanciate_class_only: if we don't want to run the SingleSliceRunner but only return them. Use case: we want to keep a hand on processing and it can be cancelled

    :return: (all_succeed, stdouts, stderrs, final_configs, future_scan)
             * all_succeed: bool, True if all the reconstruction succeed or if all job request succeed.
             * stdouts: list of stdout of job reconstruction or job requests
             * stderrs: list of stderr of job reconstruction or job requests
             * final_configs: list of configurations submits to nabu
             * future_scan: Optional[FutureTomwerScan] future scan containing futures pointing to job submited to the cluster.
                            None if local reconstruction
    :rtype: tuple

    Behavior: will clear the last slices reconstructed
    """
    # TODO: remove the local parameter
    _logger.info(f"start reconstruction of {scan}")

    cluster_config = config.pop("cluster_config", None)
    if cluster_config == {}:
        cluster_config = None
    is_cluster_job = cluster_config is not None
    if is_cluster_job and not is_slurm_available():
        raise ValueError(
            "job on cluster requested but no access to slurm cluster found"
        )

    # beam shape is not directly used by nabu (uses ctf_geometry directly)
    config.get("phase", {}).pop("beam_shape", None)

    # if scan contains some center of position copy it to nabu
    if scan.axis_params is not None and scan.axis_params.relative_cor_value is not None:
        if "reconstruction" in config:
            # move the cor value to the nabu reference
            cor_nabu_ref = scan.axis_params.relative_cor_value + scan.dim_1 / 2.0
            config["reconstruction"]["rotation_axis_position"] = str(cor_nabu_ref)
    _logger.info(f"set nabu reconstruction parameters to {scan}")

    # update nabu recons_params used
    sc_config = get_default_nabu_config(nabu_fullfield_default_config)
    sc_config.update(config)
    scan.nabu_recons_params = sc_config

    # handle special cases like several db...
    nabu_configurations = interpret_tomwer_configuration(config, scan=scan)
    if "phase" in config and "delta_beta" in config["phase"]:
        db_list = utils.retrieve_lst_of_value_from_str(
            config["phase"]["delta_beta"], type_=float
        )
    else:
        db_list = ()
    ask_sinogram_registration = len(db_list) > 0
    ask_sinogram_load = False
    output_urls = []
    stderrs = []
    stdouts = []
    final_configs = []
    futures = []
    instanciated_classes = []
    all_succeed = True
    if advancement is not None:
        advancement.setMaxAdvancement(len(nabu_configurations))
    scan.clear_latest_reconstructions()
    for nabu_configuration in nabu_configurations:
        l_config, slice_index = nabu_configuration
        result = run_single_slice_reconstruction(
            nabu_config=l_config,
            cluster_config=cluster_config,
            scan=scan,
            slice_index=slice_index,
            dry_run=dry_run,
            ask_sinogram_registration=ask_sinogram_registration,
            ask_sinogram_load=ask_sinogram_load,
            instanciate_class_only=instanciate_classes_only,
        )

        # specific treatments of results
        if result is None:
            # in case of timeout or another issue. Log should already have been provided
            pass
        elif instanciate_classes_only:
            instanciated_classes.append(result)
            continue
        if slice_index is None:
            continue
        elif isinstance(result, ResultsLocalRun):
            assert not is_cluster_job, "cluster job should not return ResultsLocalRun"
            stderrs.append(result.std_err)
            stdouts.append(result.std_out)
            output_urls.extend(result.results_urls)
            # if slice_index is None this mean that we are simply creating the
            # .cfg file for nabu full volume.
        elif isinstance(result, ResultSlurmRun):
            assert (
                is_cluster_job
            ), "local reconstruction should not return ResultSlurmRun"
            stderrs.append(result.std_err)
            stdouts.append(result.std_out)
            futures.extend(result.future_slurm_jobs)
        elif not isinstance(result, ResultsRun):
            raise ValueError(
                f"result is expected to be an instance of {ResultsRun} not {type(result)}"
            )

        # common treatments of results
        if result is not None:
            final_configs.append(result.config)
            all_succeed = all_succeed and result.success

        if ask_sinogram_registration:
            ask_sinogram_load = True
            ask_sinogram_registration = False
        if advancement is not None:
            advancement.increaseAdvancement(1)

    if instanciate_classes_only:
        return instanciated_classes
    if is_cluster_job:
        future_tomo_obj = FutureTomwerObject(
            tomo_obj=scan,
            futures=tuple(futures),
            process_requester_id=process_id,
        )
        scan.set_latest_reconstructions(output_urls)
        return all_succeed, stdouts, stderrs, final_configs, future_tomo_obj
    else:
        # tag latest reconstructions
        scan.set_latest_reconstructions(output_urls)
        return all_succeed, stdouts, stderrs, final_configs, None


class NabuSlicesTask(
    Task,
    SuperviseProcess,
    input_names=(
        "data",
        "nabu_params",
    ),
    optional_input_names=(
        "dry_run",
        "serialize_output_data",
    ),
    output_names=(
        "data",
        "nabu_params",
        "future_tomo_obj",
    ),
):
    """
    Definition of the nabu reconstruction volume reconstruction process
    """

    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        SuperviseProcess.__init__(self, process_id=process_id)
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        self._dry_run = inputs.get("dry_run", False)
        self._current_processing = None
        # we can sometime call several time a nabu subprocess. The idea is to keep track of it
        # if we want to stop the processing

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        configuration = self.inputs.nabu_params

        self.outputs.nabu_params = None
        if scan is None:
            self.outputs.data = None
            return
        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed" "")
        assert isinstance(configuration, dict), "configuration is expected to be a dict"

        entry = "entry"
        if isinstance(scan, HDF5TomoScan):
            entry = scan.entry

        output_urls = []
        stderrs = []
        stdouts = []
        final_configs = []
        futures = []
        all_succeed = True
        is_cluster_job = configuration.get("cluster_config", None) is not None
        # loop is required for distributed since version 2021
        try:
            single_slice_runner_instances = run_slices_reconstruction(
                config=configuration,
                scan=scan,
                dry_run=self._dry_run,
                process_id=self.process_id,
                instanciate_classes_only=True,
            )
        except Exception as e:
            mess = f"Fail to instanciate slice reconstructor for {str(scan)}. Reason is {e}."
            _logger.processFailed(mess)
            ProcessManager().notify_dataset_state(
                dataset=scan,
                process=self,
                state=DatasetState.FAILED,
                details=mess,
            )
            self.outputs.future_tomo_obj = None
            return

        for slice_runner in single_slice_runner_instances:
            self._current_processing = slice_runner
            result = self._current_processing.run()[
                0
            ]  # we are expecting a single slice per run in this configuration
            if result is None:
                # in case of timeout or another issue. Log should already have been provided
                pass
            elif isinstance(result, ResultsLocalRun):
                assert (
                    not is_cluster_job
                ), "cluster job should not return ResultsLocalRun"
                stderrs.append(result.std_err)
                stdouts.append(result.std_out)
                output_urls.extend(result.results_urls)
                # if slice_index is None this mean that we are simply creating the
                # .cfg file for nabu full volume.
            elif isinstance(result, ResultSlurmRun):
                assert (
                    is_cluster_job
                ), "local reconstruction should not return ResultSlurmRun"
                stderrs.append(result.std_err)
                stdouts.append(result.std_out)
                futures.extend(result.future_slurm_jobs)
            elif not isinstance(result, ResultsRun):
                raise ValueError(
                    f"result is expected to be an instance of {ResultsRun} not {type(result)}"
                )

            # common treatments of results
            if result is not None:
                final_configs.append(result.config)
                all_succeed = all_succeed and result.success

        # update future object and scan latest reconstructions
        self._current_processing = None
        if not self._cancelled and is_cluster_job:
            future_tomo_obj = FutureTomwerObject(
                tomo_obj=scan,
                futures=tuple(futures),
                process_requester_id=self.process_id,
            )
            scan.set_latest_reconstructions(output_urls)
        else:
            # tag latest reconstructions
            scan.set_latest_reconstructions(output_urls)
            future_tomo_obj = None

        process_index = scan.pop_process_index()
        # update processes information / registration
        gc.collect()

        # TODO: check output files with the tomoscan validator ?
        if self._cancelled:
            state = DatasetState.CANCELLED
            details = "cancelled by user"
            future_tomo_obj = None
            _logger.info(f"Slices computation for {scan} cancelled")
        else:
            if not all_succeed:
                mess = f"Slices computation for {scan} failed."
                state = DatasetState.FAILED
                _logger.processFailed(mess)
            else:
                state = DatasetState.SUCCEED
                mess = f"Slices computed for {scan}."
                _logger.processSucceed(mess)
            elmts = [
                format_stderr_stdout(stderr=stderr, stdout=stdout)
                for stderr, stdout in zip(stderrs, stdouts)
            ]
            elmts.insert(0, mess)
            details = "\n".join(elmts)

        ProcessManager().notify_dataset_state(
            dataset=scan,
            process=self,
            state=state,
            details=details,
        )

        # register result
        with scan.acquire_process_file_lock():
            self.register_process(
                process_file=scan.process_file,
                entry=entry,
                configuration=configuration,
                results={},
                process_index=process_index,
                overwrite=True,
            )
        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan
        self.outputs.nabu_params = scan.nabu_recons_params
        self.outputs.future_tomo_obj = future_tomo_obj

    def set_configuration(self, configuration: dict) -> None:
        Task.set_configuration(self, configuration=configuration)
        if "dry_run" in configuration:
            self.set_dry_run(bool(configuration["dry_run"]))

    @staticmethod
    def program_name():
        return "nabu-slices"

    @staticmethod
    def program_version():
        return nabu_version

    @deprecated(replacement="provide dry_run to the task inputs", since_version="1.2")
    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    @property
    @deprecated(replacement="Task.inputs.dry_run", since_version="1.2")
    def dry_run(self):
        return self._dry_run

    @staticmethod
    def get_process_frm_process_file(process_file, entry):
        """
        Read informations regarding the nabu process save in the
        tomwer_process.h5 file

        :param process_file:
        :param entry:
        :return: dictionary with the contain of the nabu process
        :rtype:dict
        """
        if entry is None:
            with HDF5File(process_file, "r", swmr=True) as h5f:
                entries = NabuSlicesTask._get_process_nodes(
                    root_node=h5f, process=NabuSlicesTask
                )
                if len(entries) == 0:
                    _logger.info("unable to find a Axis process in %s" % process_file)
                    return None
                elif len(entries) > 1:
                    raise ValueError("several entry found, entry should be " "specify")
                else:
                    entry = list(entries.keys())[0]
                    _logger.info("take %s as default entry" % entry)

        configuration_path = None
        res = {}

        with HDF5File(process_file, "r", swmr=True) as h5f:
            nabu_nodes = NabuSlicesTask._get_process_nodes(
                root_node=h5f[entry], process=NabuSlicesTask
            )
            index_to_path = {}
            for key, index in nabu_nodes.items():
                index_to_path[index] = key

            if len(nabu_nodes) == 0:
                return None
            # take the last processed dark ref
            last_process_index = sorted(list(nabu_nodes.values()))[-1]
            last_process_dark = index_to_path[last_process_index]
            if (len(index_to_path)) > 1:
                _logger.debug(
                    "several processing found for dark-ref, "
                    "take the last one: %s" % last_process_dark
                )

            for key_name in (
                "class_instance",
                "date",
                "program",
                "sequence_index",
                "version",
            ):
                if key_name in h5f[last_process_dark]:
                    res[key_name] = h5py_read_dataset(h5f[last_process_dark][key_name])
            if "configuration" in h5f[last_process_dark]:
                configuration_path = "/".join(
                    (h5f[last_process_dark].name, "configuration")
                )

        if configuration_path is not None:
            res["configuration"] = h5todict(
                h5file=process_file, path=configuration_path
            )
        return res

    def cancel(self):
        """
        stop current processing
        """
        self._cancelled = True
        if self._current_processing is not None:
            self._current_processing.cancel()

    @staticmethod
    def retrieve_last_relative_cor(scan):
        with EntryReader(scan.process_file_url) as h5f:
            latest_nabu_node = Task.get_most_recent_process(h5f, NabuSlicesTask)
            path = "configuration/reconstruction/rotation_axis_position"
            if latest_nabu_node is not None and path in latest_nabu_node:
                return h5py_read_dataset(latest_nabu_node[path])


def interpret_tomwer_configuration(
    config: dict, scan: Union[TomwerScanBase, None]
) -> tuple:
    """
    tomwer can 'mock' the nabu reconstruction to request more feature.
    Typical use case is that we can ask for reconstruction of several
    slices and not only the volume

    :param dict config: tomwer configuration for nabu
    :param scan: requested if we want to get slices
    :return: tuple of tuples (nabu configuration, is slice)
    """
    if not isinstance(config, dict):
        raise TypeError("config is expected to be a dict")

    def get_nabu_config(config):
        nabu_config = copy.deepcopy(config)
        if "tomwer_slices" in nabu_config:
            del nabu_config["tomwer_slices"]
        return nabu_config

    if "tomwer_slices" in config and scan is not None:
        slices = list(NabuSliceMode.getSlices(config["tomwer_slices"], scan))
    else:
        slices = []

    if "phase" in config and "delta_beta" in config["phase"]:
        pag_dbs = config["phase"]["delta_beta"]
        if isinstance(pag_dbs, str):
            pag_dbs = utils.retrieve_lst_of_value_from_str(pag_dbs, type_=float)
        if len(pag_dbs) == 0:
            pag_dbs = (None,)
    else:
        pag_dbs = (None,)

    # remove slices that 'cannot' be reconstructed (out of bounds)
    def filter_slice(slice_index: int):
        if scan.dim_2 is not None and slice_index > scan.dim_2:
            _logger.error(
                f"slice index {slice_index} requested. But slice index must be in 0-{scan.dim_2} - ignore this request"
            )
            return False
        return True

    slices = list(filter(lambda slice_index: filter_slice(int(slice_index)), slices))

    # by default add the slice 'None' which is the slice for the volume
    slices.append(None)
    nabu_config = get_nabu_config(config=config)
    res = []
    for slice_ in slices:
        for pag_db in pag_dbs:
            local_config = copy.deepcopy(nabu_config)
            if pag_db is not None:
                local_config["phase"]["delta_beta"] = str(pag_db)
            res.append((local_config, slice_))
    return tuple(res)


class SingleSliceRunner(_NabuBaseReconstructor):
    def __init__(
        self,
        scan: TomwerScanBase,
        config: dict,
        dry_run: bool,
        slice_index: Union[int, str, None],
        target: Target,
        ask_sinogram_registration: bool,
        ask_sinogram_load: bool,
        cluster_config: Optional[dict],
        process_name: str,
        add_to_latest_reconstructions: bool = True,
    ) -> None:
        super().__init__(
            scan=scan,
            dry_run=dry_run,
            target=target,
            cluster_config=cluster_config,
            process_name=process_name,
        )
        self._slice_index = slice_index
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dictionary not {type(dict)}")
        self._config = config
        self._ask_sinogram_registration = ask_sinogram_registration
        self._ask_sinogram_load = ask_sinogram_load
        self._add_to_latest_reconstructions = add_to_latest_reconstructions

    @property
    def slice_index(self):
        return self._slice_index

    @property
    def config(self):
        return self._config

    @property
    def ask_sinogram_load(self):
        return self._ask_sinogram_load

    @property
    def ask_sinogram_registration(self):
        return self._ask_sinogram_registration

    @property
    def add_to_latest_reconstructions(self):
        return self._add_to_latest_reconstructions

    @docstring(_NabuBaseReconstructor)
    def only_create_config_file(self):
        return self.slice_index is None

    @docstring(_NabuBaseReconstructor)
    def run(self) -> Iterable:
        """
        If the target is local will wait for the reconstruction to be finish to return

        :raise: TIMEOUT_SLURM_JOB_SUBMISSION if not all workers spwan
        """
        if isinstance(self.slice_index, str):
            if self.slice_index == "middle":
                self._slice_index = self.scan.dim_2 // 2
            else:
                raise ValueError(
                    f"slice index is expected to an int or 'middle' and not {type(self.slice_index)}"
                )
        elif (
            isinstance(self.slice_index, float)
            and int(self.slice_index) == self.slice_index
        ):
            self._slice_index = int(self.slice_index)
        elif not isinstance(self.slice_index, (int, type(None))):
            raise TypeError(
                f"slice index is expected to an int or 'middle' or None and not {type(self.slice_index)}"
            )
        config_complete = _extract_nabuconfig_keyvals(nabu_fullfield_default_config)
        config_complete["dataset"] = self.scan.get_nabu_dataset_info()
        for key in config_complete.keys():
            if key in self.config:
                config_complete[key].update(self.config[key])
        config = config_complete

        config["resources"] = utils.get_nabu_resources_desc(
            scan=self.scan, workers=1, method="local"
        )
        # force overwrite results
        if "output" not in config:
            config["output"] = {}
        # handle nabu sinogram step
        if self.scan.process_file is not None:
            steps_file_basename, _ = os.path.splitext(self.scan.process_file)
            steps_file_basename = "_".join(
                ("steps_file_basename", "nabu", "sinogram", "save", "step")
            )
            steps_file_basename = steps_file_basename + ".hdf5"
            steps_file = os.path.join(
                os.path.dirname(self.scan.process_file), steps_file_basename
            )
        else:
            steps_file = ""

        config["output"].update({"overwrite_results": 1})
        config["pipeline"] = {
            "save_steps": "sinogram" if self.ask_sinogram_registration else "",
            "resume_from_step": "sinogram" if self.ask_sinogram_load else "",
            "steps_file": steps_file,
        }

        config, cfg_folder = self._treateOutputSliceConfig(config)
        # the policy is to save nabu .cfg file at the same location as the
        # force overwrite results
        if self.slice_index is not None:
            config["reconstruction"]["start_z"] = self.slice_index
            config["reconstruction"]["end_z"] = self.slice_index

        if self.slice_index is not None:
            os.makedirs(config["output"]["location"], exist_ok=True)

        name = (
            config["output"]["file_prefix"] + nabu_settings.NABU_CONFIG_FILE_EXTENSION
        )
        if not isinstance(self.scan, EDFTomoScan):
            name = "_".join((self.scan.entry.lstrip("/"), name))
        conf_file = os.path.join(cfg_folder, name)

        _logger.info(f"{self.scan}: create {conf_file}")
        # add some tomwer metadata and save the configuration
        # note: for now the section is ignored by nabu but shouldn't stay that way
        with utils.TomwerInfo(config) as config_to_dump:
            generate_nabu_configfile(
                conf_file,
                nabu_fullfield_default_config,
                config=config_to_dump,
                options_level="advanced",
            )

        return tuple(
            [
                self._process_config(
                    config_to_dump=config_to_dump,
                    config_file=conf_file,
                    start_z=None,
                    end_z=None,
                    info="nabu slice reconstruction",
                    file_format=config_to_dump["output"]["file_format"],
                    process_name=self.process_name,
                ),
            ]
        )

    @docstring(_NabuBaseReconstructor)
    def _get_futures_slurm_callback(self, config_to_dump):
        if self.add_to_latest_reconstructions:
            # add callback to set slices reconstructed urls
            class CallBack:
                # we cannot create a future directly because distributed enforce
                # the callback to have a function signature with only the future
                # as single parameter.
                def __init__(self, f_partial, scan) -> None:
                    self.f_partial = f_partial
                    self.scan = scan

                def process(self, fn):
                    if fn.done() and not (fn.cancelled() or fn.exception()):
                        # update reconstruction urls only if processing succeed.
                        recons_urls = self.f_partial()
                        self.scan.add_latest_reconstructions(recons_urls)

            file_format = config_to_dump["output"]["file_format"]
            callback = functools.partial(
                utils.get_recons_volume_identifier,
                file_prefix=config_to_dump["output"]["file_prefix"],
                location=config_to_dump["output"]["location"],
                file_format=file_format,
                scan=self.scan,
                slice_index=None,
                start_z=None,
                end_z=None,
                expects_single_slice=True,
            )

            return (CallBack(callback, self.scan),)
        else:
            return super()._get_futures_slurm_callback(config_to_dump)

    @staticmethod
    def get_file_basename_reconstruction(
        scan, pag, ctf, db, slice_index: Union[str, int]
    ):
        if pag:
            assert db is not None, "if paganin defined, db should not be None"
        if slice_index == "middle":
            slice_index = scan.dim_2 // 2
        assert type(db) in (int, type(None))
        if isinstance(scan, HDF5TomoScan):
            basename, _ = os.path.splitext(scan.master_file)
            basename = os.path.basename(basename)
            try:
                with HDF5File(scan.master_file, mode="r") as h5f:
                    if len(h5f.keys()) > 1:
                        # if there is more than one entry in the file append the entry name to the file basename
                        basename = "_".join((basename, scan.entry.lstrip("/")))
            except Exception:
                pass
        else:
            basename = os.path.basename(scan.path)
        if slice_index is None:
            if pag:
                return "_".join((basename + "pag", "db" + str(db).zfill(4)))
            elif ctf:
                return "_".join((basename + "ctf", "db" + str(db).zfill(4)))
            else:
                return basename
        else:
            if pag:
                return "_".join(
                    (
                        basename + "slice_pag",
                        str(slice_index).zfill(6),
                        "db" + str(db).zfill(4),
                    )
                )
            elif ctf:
                return "_".join(
                    (
                        basename + "slice_ctf",
                        str(slice_index).zfill(6),
                        "db" + str(db).zfill(4),
                    )
                )
            else:
                return "_".join((basename + "slice", str(slice_index).zfill(6)))

    @docstring(_NabuBaseReconstructor)
    def _get_file_basename_reconstruction(self, pag, db, ctf):
        """

        :param TomwerScanBase scan: scan reconstructed
        :param Union[None, int] slice_index: index of the slice reconstructed.
                                            if None, we want to reconstruct the
                                            entire volume
        :param bool pag: is it a paganin reconstruction
        :param int db: delta / beta parameter
        :return: basename of the file reconstructed (without any extension)
        """
        return self.get_file_basename_reconstruction(
            scan=self.scan, db=db, pag=pag, slice_index=self.slice_index, ctf=ctf
        )


def run_single_slice_reconstruction(
    scan,
    nabu_config,
    dry_run,
    slice_index: Union[int, str, None],
    ask_sinogram_registration: bool,
    ask_sinogram_load: bool,
    process_id: Optional[int] = None,
    cluster_config: Optional[dict] = None,
    add_to_latest_reconstructions=True,
    instanciate_class_only=False,
) -> Optional[ResultsRun]:
    """
    # TODO: might need something like a context or an option "keep" slice in memory

    :param scan:
    :param nabu_config: configruation of nabu process
    :param cluster_config: configruation of cluster (slurm-cluster only for now)
    :param dry_run:
    :param Union[None,int, str] slice_index: slice index to reconstruct.
                                             If str should be "middle"
    :param local:
    :param stdout: file to redirect stdout
    :param stderr: file to redirect stderr
    :param bool ask_sinogram_registration: should we ask nabu to register sinogram
    :param bool ask_sinogram_load: should we ask nabu to load sinogram
    :param bool add_to_latest_reconstructions: if true add reconstructed slice to the latest reconstruction.
                                               We wan't to avoid this treatment for saaxis and sadeltebeta for example
    :param bool instanciate_class_only: if we don't want to run the SingleSliceRunner but only return them. Use case: we want to keep a hand on processing and it can be cancelled
    :return: result of the slice reconstruction if succeed to launch it.
    :rtype: Optional[ResultsRun]
    """
    # TODO: remove local from the function signature
    target = Target.SLURM if cluster_config not in ({}, None) else Target.LOCAL

    if process_id is not None:
        try:
            process_name = ProcessManager().get_process(process_id=process_id).name
        except KeyError:
            process_name = "unknow"
    else:
        process_name = ""

    slice_reconstructor = SingleSliceRunner(
        scan=scan,
        config=nabu_config,
        dry_run=dry_run,
        slice_index=slice_index,
        target=target,
        ask_sinogram_registration=ask_sinogram_registration,
        ask_sinogram_load=ask_sinogram_load,
        cluster_config=cluster_config,
        add_to_latest_reconstructions=add_to_latest_reconstructions,
        process_name=process_name,
    )
    if instanciate_class_only:
        return slice_reconstructor

    try:
        results = slice_reconstructor.run()
    except TimeoutError as e:
        _logger.error(e)
        return None
    else:
        assert len(results) == 1, "only one slice should be reconstructed"
        return results[0]


class NabuSliceMode(_Enum):
    MIDDLE = "middle"
    OTHER = "other"

    @staticmethod
    def getSlices(slices, scan) -> tuple:
        res = []
        try:
            mode = NabuSliceMode.from_value(slices)
        except ValueError:
            try:
                res = utils.retrieve_lst_of_value_from_str(slices, type_=int)
            except Exception:
                pass
        else:
            if mode == mode.MIDDLE:
                n_slice = scan.dim_2 or 2048
                res.append(n_slice // 2)
            else:
                raise ValueError(
                    "there should be only two ways of defining "
                    "slices: middle one or other, by giving "
                    "an unique value or a list or a tuple"
                )
        return tuple(res)


class NabuSlices(NabuSlicesTask):
    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        deprecated_warning(
            name="tomwer.core.process.reconstruction.nabu.nabuslices.Nabuslices",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="NabuSlicesTask",
        )
        super().__init__(process_id, varinfo, inputs, node_id, node_attrs, execinfo)
