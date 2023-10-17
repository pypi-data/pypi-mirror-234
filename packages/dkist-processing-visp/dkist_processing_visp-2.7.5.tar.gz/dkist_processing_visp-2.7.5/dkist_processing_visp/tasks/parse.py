"""ViSP parse task."""
from typing import TypeVar

from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.parsers.cs_step import CSStepFlower
from dkist_processing_common.parsers.cs_step import NumCSStepBud
from dkist_processing_common.parsers.time import ExposureTimeFlower
from dkist_processing_common.parsers.time import ReadoutExpTimeFlower
from dkist_processing_common.parsers.time import TaskExposureTimesBud
from dkist_processing_common.parsers.time import TaskReadoutExpTimesBud
from dkist_processing_common.parsers.unique_bud import UniqueBud
from dkist_processing_common.tasks import ParseL0InputDataBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin

from dkist_processing_visp.models.constants import VispBudName
from dkist_processing_visp.models.parameters import VispParameters
from dkist_processing_visp.parsers.map_repeats import MapScanFlower
from dkist_processing_visp.parsers.map_repeats import NumMapScansBud
from dkist_processing_visp.parsers.modulator_states import ModulatorStateFlower
from dkist_processing_visp.parsers.modulator_states import NumberModulatorStatesBud
from dkist_processing_visp.parsers.polarimeter_mode import PolarimeterModeBud
from dkist_processing_visp.parsers.raster_step import RasterScanStepFlower
from dkist_processing_visp.parsers.raster_step import TotalRasterStepsBud
from dkist_processing_visp.parsers.task import parse_header_ip_task
from dkist_processing_visp.parsers.task import VispTaskTypeFlower
from dkist_processing_visp.parsers.time import ObsIpStartTimeBud
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess
from dkist_processing_visp.parsers.wavelength import ObserveWavelengthBud

S = TypeVar("S", bound=Stem)


class ParseL0VispInputData(ParseL0InputDataBase, InputDatasetMixin):
    """
    Parse input ViSP data. Subclassed from the ParseL0InputDataBase task in dkist_processing_common to add ViSP specific parameters.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        self.parameters = VispParameters(self.input_dataset_parameters)

    @property
    def fits_parsing_class(self):
        """FITS access class to use in this task."""
        return VispL0FitsAccess

    @property
    def constant_buds(self) -> list[S]:
        """Add ViSP specific constants to common constants."""
        return super().constant_buds + [
            NumMapScansBud(),
            TotalRasterStepsBud(),
            NumCSStepBud(self.parameters.max_cs_step_time_sec),
            ObsIpStartTimeBud(),
            NumberModulatorStatesBud(),
            ObserveWavelengthBud(),
            PolarimeterModeBud(),
            TaskExposureTimesBud(
                stem_name=VispBudName.lamp_exposure_times.value,
                ip_task_type="LAMP_GAIN",
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskExposureTimesBud(
                stem_name=VispBudName.solar_exposure_times.value,
                ip_task_type="SOLAR_GAIN",
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskExposureTimesBud(
                stem_name=VispBudName.observe_exposure_times.value,
                ip_task_type="OBSERVE",
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskExposureTimesBud(
                stem_name=VispBudName.polcal_exposure_times.value,
                ip_task_type="POLCAL",
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskReadoutExpTimesBud(
                stem_name=VispBudName.lamp_readout_exp_times.value,
                ip_task_type="LAMP_GAIN",
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskReadoutExpTimesBud(
                stem_name=VispBudName.solar_readout_exp_times.value,
                ip_task_type="SOLAR_GAIN",
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskReadoutExpTimesBud(
                stem_name=VispBudName.observe_readout_exp_times.value,
                ip_task_type="OBSERVE",
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskReadoutExpTimesBud(
                stem_name=VispBudName.polcal_readout_exp_times.value,
                ip_task_type="POLCAL",
                header_task_parsing_func=parse_header_ip_task,
            ),
            UniqueBud(constant_name=VispBudName.axis_1_type.value, metadata_key="axis_1_type"),
            UniqueBud(constant_name=VispBudName.axis_2_type.value, metadata_key="axis_2_type"),
            UniqueBud(constant_name=VispBudName.axis_3_type.value, metadata_key="axis_3_type"),
        ]

    @property
    def tag_flowers(self) -> list[S]:
        """Add ViSP specific tags to common tags."""
        return super().tag_flowers + [
            CSStepFlower(max_cs_step_time_sec=self.parameters.max_cs_step_time_sec),
            MapScanFlower(),
            VispTaskTypeFlower(),
            RasterScanStepFlower(),
            ModulatorStateFlower(),
            ExposureTimeFlower(),
            ReadoutExpTimeFlower(),
        ]
