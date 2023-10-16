import logging

from ewokscore.missing_data import is_missing_data

from sluurp.executor import submit as submit_to_slurm_cluster

from nabu.stitching.config import (
    dict_to_config_obj,
    PreProcessedZStitchingConfiguration,
    PostProcessedZStitchingConfiguration,
    SlurmConfig,
    StitchingConfiguration,
    StitchingType,
)
from nabu.stitching.z_stitching import (
    z_stitching,
    StitchingPostProcAggregation as _StitchingPostProcAggregation,
)
from nabu.stitching.slurm_utils import split_stitching_configuration_to_slurm_job

from processview.core.superviseprocess import SuperviseProcess

from tomwer.core.process.task import Task
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.volume.volumefactory import VolumeFactory


_logger = logging.getLogger(__name__)


class StitcherTask(
    Task,
    SuperviseProcess,
    input_names=("stitching_config",),
    optional_input_names=(
        "cluster_config",
        "progress",
        "serialize_output_data",
    ),
    output_names=(
        "data",
        "future_tomo_obj",
        "volume",
    ),
):
    def __init__(self, process_id=None, *args, **kwargs):
        SuperviseProcess.__init__(self, process_id=process_id)
        super().__init__(*args, **kwargs)

    def run(self):
        cluster_config = self.inputs.cluster_config
        assert cluster_config is None or isinstance(cluster_config, dict)
        stitching_config = self.inputs.stitching_config
        assert isinstance(stitching_config, dict)

        config = dict_to_config_obj(stitching_config)
        config.slurm_config = SlurmConfig.from_dict(cluster_config)
        if cluster_config in ({}, None):
            # opt1: run locally
            config.slurm_config = SlurmConfig.from_dict(cluster_config)

            progress = (
                None if is_missing_data(self.inputs.progress) else self.inputs.progress
            )
            stitched_identifier = z_stitching(configuration=config, progress=progress)
            if config.stitching_type is StitchingType.Z_PREPROC:
                nx_tomo = ScanFactory.create_tomo_object_from_identifier(
                    stitched_identifier.to_str()
                )
                if self.get_input_value("serialize_output_data", True):
                    self.outputs.data = nx_tomo.to_dict()
                else:
                    self.outputs.data = nx_tomo
                self.outputs.volume = None
                self.outputs.future_tomo_obj = None
            elif config.stitching_type is StitchingType.Z_POSTPROC:
                volume = VolumeFactory.create_tomo_object_from_identifier(
                    stitched_identifier.to_str()
                )
                self.outputs.volume = volume
                self.outputs.data = None
                self.outputs.future_tomo_obj = None
            else:
                raise NotImplementedError()
        else:
            # opt2: run remotly and aggregate locally
            futures = {}

            # 2.1 launch jobs
            for i_job, (job, sub_config) in enumerate(
                split_stitching_configuration_to_slurm_job(
                    config, yield_configuration=True
                )
            ):
                _logger.info(f"submit job nb {i_job}: handles {sub_config.slices}")
                output_tomo_obj = (
                    sub_config.get_output_object().get_identifier().to_str()
                )
                futures[output_tomo_obj] = submit_to_slurm_cluster(job, timeout=999999)

            # handle post processing
            data_aggregation = StitchingPostProcAggregation(
                futures=futures,
                stitching_config=config,
            )
            for future in futures.values():
                # TODO: do we ned to make sure the processing is not finished yet ?
                future.add_done_callback(data_aggregation.onePartFinished)

            if config.stitching_type is StitchingType.Z_PREPROC:
                output_nx_tomo_file = config.output_file_path
                output_nx_tomo_entry = config.output_data_path
                tomwer_scan = HDF5TomoScan(
                    scan=output_nx_tomo_file, entry=output_nx_tomo_entry
                )
                self.outputs.future_tomo_obj = FutureTomwerObject(
                    tomo_obj=tomwer_scan,
                    futures=tuple(futures.values()),
                )
                self.outputs.data = None
                self.outputs.volume = None

            elif config.stitching_type is StitchingType.Z_POSTPROC:
                tomwer_volume = VolumeFactory.create_tomo_object_from_identifier(
                    config.output_volume.get_identifier().to_str()
                )
                self.outputs.future_tomo_obj = FutureTomwerObject(
                    tomo_obj=tomwer_volume,
                    futures=tuple(futures.values()),
                )
                self.outputs.volume = None
                self.outputs.data = None


class StitchingPostProcAggregation(_StitchingPostProcAggregation):
    """
    once stitching is done remotly we need to 'aggregate' the different part in the correct order
    """

    def __init__(self, futures, stitching_config) -> None:
        self._n_finished = 0
        self._futures = futures
        if isinstance(stitching_config, dict):
            stitching_type = StitchingType.from_value(
                stitching_config["stitching"]["type"]
            )
            if stitching_type is StitchingType.Z_PREPROC:
                self._stitching_config = PreProcessedZStitchingConfiguration.from_dict(
                    stitching_config
                )
            elif stitching_type is StitchingType.Z_POSTPROC:
                self._stitching_config = PostProcessedZStitchingConfiguration.from_dict(
                    stitching_config
                )
            else:
                raise NotImplementedError("stitching type not handled")
        elif not isinstance(stitching_config, StitchingConfiguration):
            raise TypeError(
                f"stitching_config is expected to be an instance of {StitchingConfiguration}. {type(stitching_config)} provided instead"
            )
        else:
            self._stitching_config = stitching_config

    def onePartFinished(self, *args, **kwargs):
        self._n_finished += 1
        if self._n_finished == len(self._futures):
            _logger.info("All slurm job finished. Will aggregate results")
            self.process()
