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

"""contain the SAAxisProcess. Half automatic center of rotation calculation
"""

__authors__ = [
    "H.Payno",
]
__license__ = "MIT"
__date__ = "10/02/2021"


import copy
import logging
import os
from typing import Optional

import h5py
import numpy
from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.io.url import DataUrl
from silx.utils.deprecation import deprecated_warning

from tomoscan.io import HDF5File

import tomwer.version
from tomwer.core.process.reconstruction.axis import AxisRP
from tomwer.core.process.reconstruction.nabu.nabuscores import (
    run_nabu_one_slice_several_config,
)
from tomwer.core.process.reconstruction.nabu.nabuslices import (
    SingleSliceRunner,
    interpret_tomwer_configuration,
)
from tomwer.core.process.reconstruction.scores import (
    ComputedScore,
    apply_roi,
    compute_score,
    get_disk_mask_radius,
)
from tomwer.core.process.reconstruction.scores.params import ScoreMethod
from tomwer.core.process.task import Task
from tomwer.core.progress import Progress
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils import logconfig
from tomwer.core.utils.locker import FileLockerManager
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.core.utils.slurm import is_slurm_available
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.io.utils.utils import get_slice_data
from tomwer.io.utils import format_stderr_stdout
from tomwer.core.process.reconstruction.nabu.nabucommon import (
    ResultsLocalRun,
    ResultSlurmRun,
    ResultsWithStd,
)
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.process.reconstruction.saaxis.params import ReconstructionMode

from ..nabu import utils
from .params import SAAxisParams

_logger = logging.getLogger(__name__)


DEFAULT_RECONS_FOLDER = "saaxis_results"


def one_slice_several_cor(
    scan,
    configuration: dict,
    process_id: Optional[int] = None,
) -> tuple:
    """
    Run a slice reconstruction using nabu per Center Of Rotation (cor) provided
    Then for each compute a score (quality) of the center of rotation

    .. warning:: if target if the slurm cluster this will wait for the processing to be done to return the result.
                 as this function is returning the result of the score process on reconstructed slices

    :param TomwerScanBase scan:
    :param dict configuration: nabu reconstruction parameters (can include 'slurm-cluster' key defining the slurm configuration)
    :param int process_id: process id
    :return: cor_reconstructions, outs, errs
             cor_reconstructions is a dictionary of cor as key and a tuple
             (url, score) as value
    :rtype: tuple
    """
    task = SAAxisTask(
        process_id=process_id,
        inputs={
            "data": scan,
            "sa_axis_params": configuration,
            "serialize_output_data": False,
        },
    )
    task.run()
    return (
        task.outputs.scores,
        task.outputs.std_out,
        task.outputs.std_err,
        task.outputs.rois,
    )


class SAAxisTask(
    Task,
    SuperviseProcess,
    input_names=("data", "sa_axis_params"),
    output_names=("data", "best_cor"),
    optional_input_names=(
        "dry_run",
        "dump_roi",
        "dump_process",
        "serialize_output_data",
    ),
):
    """
    Main process to launch several reconstruction of a single slice with
    several Center Of Rotation (cor) values

    As the saaxis is integrating the score calculation we will never get a future_tomo_scan as output
    """

    def __init__(
        self, process_id=None, inputs=None, varinfo=None, node_attrs=None, execinfo=None
    ):
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        SuperviseProcess.__init__(self, process_id=process_id)
        self._dry_run = inputs.get("dry_run", False)
        self._dump_process = inputs.get("dump_process", True)
        self._dump_roi = inputs.get("dump_roi", False)
        self._std_outs = tuple()
        self._std_errs = tuple()
        self._current_processing = None
        self._cancelled = False

    @property
    def std_outs(self):
        return self._std_outs

    @property
    def std_errs(self):
        return self._std_errs

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    @property
    def dry_run(self):
        return self._dry_run

    @property
    def dump_roi(self):
        return self._dump_roi

    @dump_roi.setter
    def dump_roi(self, dump):
        self._dump_roi = dump

    @staticmethod
    def autofocus(scan) -> Optional[float]:
        scores = scan.saaxis_params.scores
        if scores is None:
            return
        score_method = scan.saaxis_params.score_method
        best_cor, best_score = None, 0
        for cor, (_, score_cls) in scores.items():
            if score_cls is None:  # if score calculation failed
                continue
            score = score_cls.get(score_method)
            if score is None:
                continue
            if score > best_score:
                best_cor, best_score = cor, score
        scan.saaxis_params.autofocus = best_cor
        if scan.axis_params is None:
            # create parameter if needed because will set it once he find the best cor
            scan.axis_params = AxisRP()
        scan.axis_params.frame_width = scan.dim_1
        scan.axis_params.set_relative_value(best_cor)
        return best_cor

    def _config_preprocessing(
        self, scan, config, cor_positions, file_format, output_dir, cluster_config
    ):
        """convert general configuration to nabu - single reconstruction - configuration"""
        nabu_configurations = interpret_tomwer_configuration(config, scan=None)
        if len(nabu_configurations) == 0:
            raise RuntimeWarning(
                "Unable to get a valid nabu configuration for " "reconstruction."
            )
        elif len(nabu_configurations) > 1:
            _logger.warning(
                "Several configuration found for nabu (you probably "
                "ask for several delta/beta value or several slices). "
                "Picking the first one."
            )

        # work on file name...
        if output_dir is None:
            output_dir = os.path.join(scan.path, DEFAULT_RECONS_FOLDER)
        if scan.process_file is not None:
            steps_file_basename, _ = os.path.splitext(scan.process_file)
            steps_file_basename = "_".join(
                ("steps_file_basename", "nabu", "sinogram", "save", "step")
            )
            steps_file_basename = steps_file_basename + ".hdf5"
            steps_file = os.path.join(output_dir, steps_file_basename)
        else:
            steps_file = ""

        base_config = nabu_configurations[0][0]
        if cluster_config == {}:
            cluster_config = None
        is_cluster_job = cluster_config is not None
        if is_cluster_job and not is_slurm_available():
            raise ValueError(
                "job on cluster requested but no access to slurm cluster found"
            )
        configs = {}

        for i_cor, cor in enumerate(cor_positions):
            nabu_configuration = copy.deepcopy(base_config)
            nabu_configuration["pipeline"] = {
                "save_steps": "sinogram" if i_cor == 0 else "",
                "resume_from_step": "sinogram",
                "steps_file": steps_file,
            }
            # convert cor from tomwer ref to nabu ref
            if scan.dim_1 is not None:
                cor_nabu_ref = cor + scan.dim_1 / 2.0
            else:
                _logger.warning("enable to get image half width. Set it to 1024")
                cor_nabu_ref = cor + 1024
            # handle reconstruction section
            if "reconstruction" not in nabu_configuration:
                nabu_configuration["reconstruction"] = {}
            nabu_configuration["reconstruction"]["rotation_axis_position"] = str(
                cor_nabu_ref
            )
            # handle output section
            if "output" not in nabu_configuration:
                nabu_configuration["output"] = {}
            nabu_configuration["output"]["location"] = output_dir
            nabu_configuration["output"]["file_format"] = file_format
            # handle resources section
            nabu_configuration["resources"] = utils.get_nabu_resources_desc(
                scan=scan, workers=1, method="local"
            )
            configs[cor] = nabu_configuration
        return configs

    def _run_slice_recons_per_cor(
        self,
        scan,
        configs,
        slice_index,
        file_format,
        advancement,
        cluster_config,
        dry_run=False,
    ):
        runners = run_nabu_one_slice_several_config(
            nabu_configs=configs,
            scan=scan,
            slice_index=slice_index,
            dry_run=dry_run,
            file_format=file_format,
            advancement=advancement,
            cluster_config=cluster_config.to_dict()
            if cluster_config is not None
            else None,
            process_id=self.process_id,
            instanciate_classes_only=True,
            output_file_prefix_pattern="cor_{file_name}_{value}",  # as the cor is evolving, create different files to make sure the name will be unique
        )

        future_tomo_objs = {}
        success = True
        recons_urls = {}
        std_outs = []
        std_errs = []

        for runner in runners:
            if self._cancelled:
                break
            self._current_processing = runner
            try:
                results = runner.run()
            except TimeoutError as e:
                _logger.error(e)
            else:
                assert isinstance(
                    results, dict
                ), "results should be a dictionary with cor as key and urls as value"

                for cor, res in results.items():
                    success = success and res.success
                    if isinstance(res, ResultsWithStd):
                        std_outs.append(res.std_out)
                        std_errs.append(res.std_err)
                    if isinstance(res, ResultsLocalRun):
                        recons_urls[cor] = res.results_urls
                    if isinstance(res, ResultSlurmRun):
                        future_tomo_obj = FutureTomwerObject(
                            tomo_obj=scan,
                            process_requester_id=self.process_id,
                            futures=res.future_slurm_jobs,
                        )
                        future_tomo_objs[cor] = future_tomo_obj
        return success, recons_urls, future_tomo_objs, std_outs, std_errs

    def _resolve_futures(
        self,
        scan,
        nabu_config,
        slice_index,
        file_format,
        cor_reconstructions,
        future_tomo_objs: dict,
        output_dir,
    ):
        """
        in case the task is launching jobs over slurm wait for them to be finished before resuming 'standard processing'
        """
        if output_dir is None:
            output_dir = os.path.join(scan.path, DEFAULT_RECONS_FOLDER)

        db = None
        pag = False
        ctf = False
        if "phase" in nabu_config:
            phase_method = nabu_config["phase"].get("method", "").lower()
            if phase_method in ("pag", "paganin"):
                pag = True
            elif phase_method in ("ctf",):
                ctf = True
            if "delta_beta" in nabu_config["phase"]:
                db = round(float(nabu_config["phase"]["delta_beta"]))

        for cor, future_tomo_obj in future_tomo_objs.items():
            if self._cancelled:
                break
            future_tomo_obj.results()
            # for saaxis we need to retrieve reconstruction url
            if future_tomo_obj.cancelled() or future_tomo_obj.exceptions():
                continue
            else:
                _file_name = SingleSliceRunner.get_file_basename_reconstruction(
                    scan=scan,
                    slice_index=slice_index,
                    pag=pag,
                    db=db,
                    ctf=ctf,
                )
                file_prefix = f"cor_{_file_name}_{cor}"

                recons_vol_id = utils.get_recons_volume_identifier(
                    scan=scan,
                    file_format=file_format,
                    file_prefix=file_prefix,
                    location=output_dir,
                    slice_index=None,
                    start_z=None,
                    end_z=None,
                    expects_single_slice=True,
                )
                assert len(recons_vol_id) == 1, "only one volume reconstructed expected"
                cor_reconstructions[cor] = recons_vol_id

    def _post_processing(self, scan, slice_index, cor_reconstructions):
        """
        compute score along the different slices
        """
        post_processing = _PostProcessing(
            slice_index=slice_index, scan=scan, cor_reconstructions=cor_reconstructions
        )
        post_processing._cancelled = self._cancelled
        self._current_processing = post_processing
        return post_processing.run()

    def _compute_mess_details(self, mess=""):
        """
        util to join a message and nabu std err and std out
        """
        nabu_logs = []
        for std_err, std_out in zip(self._std_errs, self.std_outs):
            nabu_logs.append(format_stderr_stdout(stdout=std_out, stderr=std_err))
        self._nabu_log = nabu_logs
        nabu_logs.insert(0, mess)
        return "\n".join(nabu_logs)

    @staticmethod
    def _preprocess_slice_index(slice_index, mode: ReconstructionMode):
        if isinstance(slice_index, str):
            if not slice_index == "middle":
                raise ValueError(f"slice index {slice_index} not recognized")
            else:
                return slice_index
        elif not len(slice_index) == 1:
            raise ValueError(f"{mode.value} mode only manage one slice")
        else:
            return list(slice_index.values())[0]

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            self.outputs.data = None
            return
        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed")
        # TODO: look and update if there is some nabu reconstruction
        # or axis information to be used back
        configuration = self.inputs.sa_axis_params
        params = SAAxisParams.from_dict(configuration)
        # insure output dir is created
        if params.output_dir in (None, ""):
            params.output_dir = os.path.join(scan.path, "saaxis_results")
            if not os.path.exists(params.output_dir):
                os.makedirs(params.output_dir)
        # try to find an estimated cor
        #  from a previously computed cor
        if params.estimated_cor is None and scan.axis_params is not None:
            relative_cor = scan.axis_params.relative_cor_value
            if relative_cor is not None and numpy.issubdtype(
                type(relative_cor), numpy.number
            ):
                params.estimated_cor = relative_cor
                _logger.info(
                    f"{scan}: set estimated cor from previously computed cor ({params.estimated_cor})"
                )
        #  from scan.estimated_cor_position
        if params.estimated_cor is None and scan.estimated_cor_frm_motor is not None:
            params.estimated_cor = scan.estimated_cor_frm_motor
            _logger.info(
                f"{scan}: set estimated cor from motor position ({params.estimated_cor})"
            )
        if scan.dim_1 is not None:
            params.image_width = scan.dim_1
        scan.saaxis_params = params

        mode = ReconstructionMode.from_value(params.mode)
        if mode is not ReconstructionMode.VERTICAL:
            raise ValueError(f"{mode} is not handled for now")

        output_dir = params.output_dir
        if output_dir is None:
            output_dir = os.path.join(scan.path, DEFAULT_RECONS_FOLDER)
        nabu_output_config = configuration.get("output", {})
        file_format = nabu_output_config.get("file_format", "hdf5")
        slice_index = self._preprocess_slice_index(
            params.slice_indexes,
            mode=mode,
        )
        cluster_config = params.cluster_config
        dry_run = self._dry_run

        # step one: complete nabu configuration(s)
        configs = self._config_preprocessing(
            scan=scan,
            config=configuration,
            cor_positions=params.cors,
            file_format=file_format,
            output_dir=output_dir,
            cluster_config=cluster_config,
        )
        # step 2: run reconstructions
        advancement = Progress(
            f"sa-axis - slice {slice_index} of {scan.get_identifier().short_description()}"
        )
        cors_res = {}
        rois = {}

        try:
            (
                _,
                cor_reconstructions,
                future_tomo_objs,
                self._std_outs,
                self._std_errs,
            ) = self._run_slice_recons_per_cor(
                scan=scan,
                configs=configs,
                slice_index=slice_index,
                file_format=file_format,
                advancement=advancement,
                cluster_config=cluster_config,
                dry_run=dry_run,
            )
        except Exception as e:
            _logger.error(e)
            mess = f"sa-axis -nabu- computation for {str(scan)} failed."
            state = DatasetState.FAILED
        else:
            # step 3: wait for future if any
            self._resolve_futures(
                scan=scan,
                nabu_config=configuration,
                slice_index=slice_index,
                file_format=file_format,
                cor_reconstructions=cor_reconstructions,
                future_tomo_objs=future_tomo_objs,
                output_dir=output_dir,
            )

            # step 4: run post processing (compute score for each slice)
            try:
                cors_res, rois = self._post_processing(
                    scan=scan,
                    slice_index=slice_index,
                    cor_reconstructions=cor_reconstructions,
                )
            except Exception as e:
                _logger.error(e)
                mess = f"sa-axis -post-processing- computation for {str(scan)} failed."
                state = DatasetState.FAILED
                cors_res = {}
            else:
                state = DatasetState.WAIT_USER_VALIDATION
                mess = "sa-axis computation succeeded"

        if self._cancelled:
            state = DatasetState.CANCELLED
            mess = "scan cancelled by the user"

        ProcessManager().notify_dataset_state(
            dataset=scan,
            process=self,
            state=state,
            details=self._compute_mess_details(mess),
        )

        scan.saaxis_params.scores = cors_res
        best_relative_cor = self.autofocus(scan=scan)

        if best_relative_cor is not None:
            scan.axis_params.set_relative_value(best_relative_cor)

        self._process_end(scan=scan, cors_res=cors_res, score_rois=rois)

        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan
        self.outputs.best_cor = best_relative_cor

    def _process_end(self, scan, cors_res, score_rois):
        assert isinstance(scan, TomwerScanBase)
        state = ProcessManager().get_dataset_state(
            dataset_id=scan.get_identifier(), process=self
        )
        if state not in (
            DatasetState.CANCELLED,
            DatasetState.FAILED,
            DatasetState.SKIPPED,
        ):
            try:
                extra = {
                    logconfig.DOC_TITLE: self._scheme_title,
                    logconfig.SCAN_ID: str(scan),
                }
                slice_index = self.inputs.sa_axis_params.get("slice_index", None)

                if cors_res is None:
                    info = f"fail to compute cor scores of slice {slice_index} for scan {scan}."
                    _logger.processFailed(info, extra=extra)
                    ProcessManager().notify_dataset_state(
                        dataset=scan,
                        process=self,
                        state=DatasetState.FAILED,
                        details=info,
                    )
                else:
                    info = (
                        f"cor scores of slice {slice_index} for scan {scan} computed."
                    )
                    _logger.processSucceed(info, extra=extra)
                    ProcessManager().notify_dataset_state(
                        dataset=scan,
                        process=self,
                        state=DatasetState.WAIT_USER_VALIDATION,
                        details=info,
                    )
            except Exception as e:
                _logger.error(e)
            else:
                if self._dump_process:
                    process_idx = SAAxisTask.process_to_tomwer_processes(
                        scan=scan,
                    )
                    if self.dump_roi and process_idx is not None:
                        self.dump_rois(
                            scan, score_rois=score_rois, process_index=process_idx
                        )

    @staticmethod
    def dump_rois(scan, score_rois, process_index):
        process_file = scan.process_file
        process_name = "tomwer_process_" + str(process_index)

        if scan.saaxis_params.scores in (None, {}):
            return

        def get_process_path():
            return "/".join((scan.entry or "entry", process_name))

        # save it to the file
        with FileLockerManager.get_lock(process_file):
            # needs an extra lock for multiprocessing

            with HDF5File(process_file, mode="a") as h5f:
                nx_process = h5f.require_group(get_process_path())
                score_roi_grp = nx_process.require_group("score_roi")
                for cor, roi in score_rois.items():
                    score_roi_grp[str(cor)] = roi
                    score_roi_grp[str(cor)].attrs["interpretation"] = "image"

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "semi-automatic axis"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "Semi automatic center of rotation / axis calculation"

    @staticmethod
    def process_to_tomwer_processes(scan):
        if scan.process_file is not None:
            entry = "entry"
            if isinstance(scan, HDF5TomoScan):
                entry = scan.entry

            cor = None
            if hasattr(scan, "axis_params"):
                cor = scan.axis_params.relative_cor_value

            process_index = scan.pop_process_index()
            try:
                with scan.acquire_process_file_lock():
                    Task._register_process(
                        process_file=scan.process_file,
                        entry=entry,
                        results={"center_of_rotation": cor if cor is not None else "-"},
                        configuration=scan.saaxis_params.to_dict(),
                        process_index=process_index,
                        overwrite=True,
                        process=SAAxisTask,
                    )
                    SAAxisTask._extends_results(
                        scan=scan, entry=entry, process_index=process_index
                    )
            except Exception as e:
                _logger.warning(
                    f"Fail to register process of with index {process_index}. Reason is {e}"
                )
            return process_index

    @staticmethod
    def _extends_results(scan, entry, process_index):
        process_file = scan.process_file
        process_name = "tomwer_process_" + str(process_index)

        if scan.saaxis_params.scores in (None, {}):
            return

        def get_process_path():
            return "/".join((entry or "entry", process_name))

        # save it to the file
        with FileLockerManager().get_lock(process_file):
            # needs an extra lock for multiprocessing

            with HDF5File(process_file, mode="a") as h5f:
                nx_process = h5f.require_group(get_process_path())
                if "NX_class" not in nx_process.attrs:
                    nx_process.attrs["NX_class"] = "NXprocess"

                results = nx_process.require_group("results")
                for cor, (url, score) in scan.saaxis_params.scores.items():
                    results_cor = results.require_group(str(cor))
                    for method in ScoreMethod:
                        method_score = score.get(method)
                        if method_score is None:
                            results_cor[method.value] = "None"
                        else:
                            results_cor[method.value] = method_score

                    link_path = os.path.relpath(
                        url.file_path(),
                        os.path.dirname(process_file),
                    )
                    results_cor["reconstructed_slice"] = h5py.ExternalLink(
                        link_path, url.data_path()
                    )

    def cancel(self):
        """
        stop current processing
        """
        if self._current_processing is not None:
            self._cancelled = True
            self._current_processing.cancel()


class _PostProcessing:
    """class used to run SA-axis post-processing on reconstructed slices"""

    def __init__(self, cor_reconstructions, slice_index, scan) -> None:
        self._cor_reconstructions = cor_reconstructions
        self._slice_index = slice_index
        self._scan = scan
        self._cancelled = False

    def run(self):
        datasets = self.load_datasets()

        mask_disk_radius = get_disk_mask_radius(datasets)
        scores = {}
        rois = {}
        for cor, (url, data) in datasets.items():
            if self._cancelled:
                break

            if data is None:
                score = None
            else:
                assert data.ndim == 2
                data_roi = apply_roi(data=data, radius=mask_disk_radius, url=url)
                rois[cor] = data_roi

                # move data_roi to [0-1] range
                #  preprocessing: get percentile 0 and 99 from image and
                #  "clean" highest and lowest pixels from it
                min_p, max_p = numpy.percentile(data_roi, (1, 99))
                data_roi_int = data_roi[...]
                data_roi_int[data_roi_int < min_p] = min_p
                data_roi_int[data_roi_int > max_p] = max_p
                data_roi_int = (data_roi_int - min_p) / (max_p - min_p)

                if isinstance(self._scan, EDFTomoScan):
                    _logger.info("tomo consistency is not handled for EDF scan")
                    tomo_consistency_score = None
                else:
                    try:
                        projections_with_angle = self._scan.projections_with_angle()
                        angles_ = [
                            frame_angle
                            for frame_angle, frame in projections_with_angle.items()
                        ]
                        angles = []
                        for angle in angles_:
                            if not isinstance(angle, str):
                                angles.append(angle)
                        if self._slice_index == "middle":
                            if self._scan.dim_2 is not None:
                                self._slice_index = self._scan.dim_2 // 2
                            else:
                                _logger.warning(
                                    "scan.dim_2 returns None, unable to deduce middle "
                                    "pick 1024"
                                )
                                self._slice_index = 1024
                        tomo_consistency_score = compute_score(
                            data=data,
                            method=ScoreMethod.TOMO_CONSISTENCY,
                            angles=angles,
                            original_sinogram=self._scan.get_sinogram(
                                self._slice_index
                            ),
                            detector_width=self._scan.dim_1,
                            original_axis_position=cor + self._scan.dim_1 / 2.0,
                        )
                    except Exception as e:
                        _logger.error(e)
                        tomo_consistency_score = None
                score = ComputedScore(
                    tv=compute_score(data=data_roi_int, method=ScoreMethod.TV),
                    std=compute_score(data=data_roi_int, method=ScoreMethod.STD),
                    tomo_consistency=tomo_consistency_score,
                )
            scores[cor] = (url, score)
        return scores, rois

    def load_datasets(self):
        datasets_ = {}
        for cor, volume_identifiers in self._cor_reconstructions.items():
            if self._cancelled:
                break

            if len(volume_identifiers) == 0:
                # in the case failed to load the url
                continue
            elif len(volume_identifiers) > 1:
                raise ValueError("only one slice reconstructed expected per cor")
            volume = VolumeFactory.create_tomo_object_from_identifier(
                volume_identifiers[0]
            )
            urls = tuple(volume.browse_data_urls())
            if len(urls) != 1:
                raise ValueError(
                    f"volume is expected to have at most one url (single slice volume). get {len(urls)} - most likely nabu reconstruction failed. Do you have GPU ? Are the requested COR values valid ? - Especially for Half-acquisition"
                )
            url = urls[0]
            if not isinstance(url, (DataUrl, str)):
                raise TypeError(
                    f"url is expected to be a str or DataUrl not {type(url)}"
                )

            try:
                data = get_slice_data(url=url)
            except Exception as e:
                _logger.error(
                    f"Fail to compute a score for {url.path()}. Reason is {e}"
                )
                datasets_[cor] = (url, None)
            else:
                if data.ndim == 3:
                    if data.shape[0] == 1:
                        data = data.reshape(data.shape[1], data.shape[2])
                    elif data.shape[2] == 1:
                        data = data.reshape(data.shape[0], data.shape[1])
                    else:
                        raise ValueError(f"Data is expected to be 2D. Not {data.ndim}D")
                elif data.ndim == 2:
                    pass
                else:
                    raise ValueError("Data is expected to be 2D. Not {data.ndim}D")

                datasets_[cor] = (url, data)
        return datasets_

    def cancel(self):
        self._cancelled = True


class SAAxisProcess(SAAxisTask):
    def __init__(
        self, process_id=None, inputs=None, varinfo=None, node_attrs=None, execinfo=None
    ):
        deprecated_warning(
            name="tomwer.core.process.reconstruction.saaxis.SAAxisProcess",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="SAAxisTask",
        )
        super().__init__(process_id, inputs, varinfo, node_attrs, execinfo)
