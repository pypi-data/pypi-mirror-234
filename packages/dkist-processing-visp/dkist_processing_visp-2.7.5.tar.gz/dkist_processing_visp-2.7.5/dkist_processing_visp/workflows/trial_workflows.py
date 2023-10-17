"""Workflows for trial runs (i.e., not Production)."""
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TrialTeardown
from dkist_processing_core import Workflow

from dkist_processing_visp.tasks.background_light import BackgroundLightCalibration
from dkist_processing_visp.tasks.dark import DarkCalibration
from dkist_processing_visp.tasks.geometric import GeometricCalibration
from dkist_processing_visp.tasks.instrument_polarization import InstrumentPolarizationCalibration
from dkist_processing_visp.tasks.lamp import LampCalibration
from dkist_processing_visp.tasks.parse import ParseL0VispInputData
from dkist_processing_visp.tasks.science import ScienceCalibration
from dkist_processing_visp.tasks.solar import SolarCalibration
from dkist_processing_visp.tasks.trial_output_data import TransferVispTrialData
from dkist_processing_visp.tasks.write_l1 import VispWriteL1Frame

non_science_trial_pipeline = Workflow(
    category="visp",
    input_data="l0",
    output_data="l1",
    detail="non-science-trial",
    workflow_package=__package__,
)
non_science_trial_pipeline.add_node(task=TransferL0Data, upstreams=None)
non_science_trial_pipeline.add_node(task=ParseL0VispInputData, upstreams=TransferL0Data)
non_science_trial_pipeline.add_node(task=DarkCalibration, upstreams=ParseL0VispInputData)
non_science_trial_pipeline.add_node(task=BackgroundLightCalibration, upstreams=DarkCalibration)
non_science_trial_pipeline.add_node(task=LampCalibration, upstreams=DarkCalibration)
non_science_trial_pipeline.add_node(task=GeometricCalibration, upstreams=DarkCalibration)
non_science_trial_pipeline.add_node(
    task=SolarCalibration,
    upstreams=[LampCalibration, GeometricCalibration, BackgroundLightCalibration],
)
non_science_trial_pipeline.add_node(
    task=InstrumentPolarizationCalibration, upstreams=SolarCalibration
)
non_science_trial_pipeline.add_node(
    task=TransferVispTrialData, upstreams=InstrumentPolarizationCalibration
)
non_science_trial_pipeline.add_node(task=TrialTeardown, upstreams=TransferVispTrialData)

full_trial_pipeline = Workflow(
    category="visp",
    input_data="l0",
    output_data="l1",
    detail="full-trial",
    workflow_package=__package__,
)
full_trial_pipeline.add_node(task=TransferL0Data, upstreams=None)
full_trial_pipeline.add_node(task=ParseL0VispInputData, upstreams=TransferL0Data)
full_trial_pipeline.add_node(task=DarkCalibration, upstreams=ParseL0VispInputData)
full_trial_pipeline.add_node(task=BackgroundLightCalibration, upstreams=DarkCalibration)
full_trial_pipeline.add_node(task=LampCalibration, upstreams=DarkCalibration)
full_trial_pipeline.add_node(task=GeometricCalibration, upstreams=DarkCalibration)
full_trial_pipeline.add_node(
    task=SolarCalibration,
    upstreams=[LampCalibration, GeometricCalibration, BackgroundLightCalibration],
)
full_trial_pipeline.add_node(task=InstrumentPolarizationCalibration, upstreams=SolarCalibration)
full_trial_pipeline.add_node(task=ScienceCalibration, upstreams=InstrumentPolarizationCalibration)
full_trial_pipeline.add_node(task=VispWriteL1Frame, upstreams=ScienceCalibration)
full_trial_pipeline.add_node(task=TransferVispTrialData, upstreams=VispWriteL1Frame)
full_trial_pipeline.add_node(task=TrialTeardown, upstreams=TransferVispTrialData)
