import argparse
import json
import os
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from random import randint
from unittest.mock import patch

from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_header_validator import spec214_validator
from dkist_processing_common.manual import ManualProcessing
from dkist_processing_common.tasks import QualityL1Metrics
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_service_configuration import logger

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess
from dkist_processing_visp.tasks.assemble_movie import AssembleVispMovie
from dkist_processing_visp.tasks.background_light import BackgroundLightCalibration
from dkist_processing_visp.tasks.dark import DarkCalibration
from dkist_processing_visp.tasks.geometric import GeometricCalibration
from dkist_processing_visp.tasks.instrument_polarization import InstrumentPolarizationCalibration
from dkist_processing_visp.tasks.l1_output_data import VispSubmitQuality
from dkist_processing_visp.tasks.lamp import LampCalibration
from dkist_processing_visp.tasks.make_movie_frames import MakeVispMovieFrames
from dkist_processing_visp.tasks.parse import ParseL0VispInputData
from dkist_processing_visp.tasks.quality_metrics import VispL0QualityMetrics
from dkist_processing_visp.tasks.quality_metrics import VispL1QualityMetrics
from dkist_processing_visp.tasks.science import ScienceCalibration
from dkist_processing_visp.tasks.solar import SolarCalibration
from dkist_processing_visp.tasks.visp_base import VispTaskBase
from dkist_processing_visp.tasks.write_l1 import VispWriteL1Frame
from dkist_processing_visp.tests.conftest import VispTestingParameters
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadBackgroundCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadDarkCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadGeometricCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadInputParsing
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadInstPolCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadLampCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadSolarCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveBackgroundCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveDarkCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveGeometricCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveInputParsing
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveInstPolCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveLampCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveSolarCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import (
    transfer_trial_data_locally_task,
)

INV = False
try:
    from dkist_inventory.asdf_generator import dataset_from_fits

    INV = True
except ModuleNotFoundError:
    # Bitbucket pipelines won't have dkist-inventory installed
    pass

QRM = False
try:
    from quality_report_maker.libraries import report
    from quality_report_maker.libraries.json_encoder import datetime_json_object_hook

    QRM = True
except ModuleNotFoundError:
    logger.warning("Could not find quality_report_maker (must be installed manually)")
if QRM:
    import matplotlib.pyplot as plt

    plt.ioff()


class DatetimeEncoder(json.JSONEncoder):
    # Copied from quality_report_maker
    """
    A JSON encoder which encodes datetime(s) as iso formatted strings.
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return {"iso_date": obj.isoformat("T")}
        return super().default(obj)


class Translate122To214L0(WorkflowTaskBase):
    def run(self) -> None:
        raw_dir = Path(self.scratch.scratch_base_path) / f"VISP{self.recipe_run_id:03n}"
        if not os.path.exists(self.scratch.workflow_base_path):
            os.makedirs(self.scratch.workflow_base_path)

        if not raw_dir.exists():
            raise FileNotFoundError(
                f"Expected to find a raw VISP{{run_id:03n}} folder in {self.scratch.scratch_base_path}"
            )

        for file in raw_dir.glob("*.FITS"):
            translated_file_name = Path(self.scratch.workflow_base_path) / os.path.basename(file)
            logger.info(f"Translating {file} -> {translated_file_name}")
            hdl = fits.open(file)

            header = spec122_validator.validate_and_translate_to_214_l0(
                hdl[0].header, return_type=fits.HDUList
            )[0].header

            comp_hdu = fits.CompImageHDU(header=header, data=hdl[0].data)
            comp_hdl = fits.HDUList([fits.PrimaryHDU(), comp_hdu])
            comp_hdl.writeto(translated_file_name, overwrite=True)

            hdl.close()
            del hdl
            comp_hdl.close()
            del comp_hdl


class CreateInputDatasetParameterDocument(WorkflowTaskBase):
    def run(self) -> None:
        doc_path = self.scratch.workflow_base_path / "input_dataset_parameters.json"
        with open(doc_path, "w") as f:
            f.write(json.dumps(self.input_dataset_document_simple_parameters_part))
        self.tag(doc_path, VispTag.input_dataset_parameters())
        logger.info(f"Wrote input dataset doc to {doc_path}")

    @property
    def input_dataset_document_simple_parameters_part(self):
        parameters_list = []
        value_id = randint(1000, 2000)
        for pn, pv in asdict(VispTestingParameters()).items():
            values = [
                {
                    "parameterValueId": value_id,
                    "parameterValue": json.dumps(pv),
                    "parameterValueStartDate": "1946-11-20",
                }
            ]
            parameter = {"parameterName": pn, "parameterValues": values}
            parameters_list.append(parameter)

        return parameters_list


def tag_inputs_task(suffix: str):
    class TagInputs(WorkflowTaskBase):
        def run(self) -> None:
            logger.info(f"Looking in {os.path.abspath(self.scratch.workflow_base_path)}")
            input_file_list = list(self.scratch.workflow_base_path.glob(f"*.{suffix}"))
            if len(input_file_list) == 0:
                raise FileNotFoundError(
                    f"Did not find any files matching '*.{suffix}' in {self.scratch.workflow_base_path}"
                )
            for file in input_file_list:
                logger.info(f"Found {file}")
                self.tag(path=file, tags=[VispTag.input(), VispTag.frame()])

    return TagInputs


class ShowPolMode(VispTaskBase):
    def run(self) -> None:
        logger.info(f"{self.constants.correct_for_polarization = }")


class ShowExposureTimes(VispTaskBase):
    def run(self) -> None:
        logger.info(f"{self.constants.dark_exposure_times = }")
        logger.info(f"{self.constants.dark_readout_exp_times = }")
        logger.info(f"{self.constants.lamp_exposure_times = }")
        logger.info(f"{self.constants.lamp_readout_exp_times = }")
        logger.info(f"{self.constants.solar_exposure_times = }")
        logger.info(f"{self.constants.solar_readout_exp_times = }")
        if self.constants.correct_for_polarization:
            logger.info(f"{self.constants.polcal_exposure_times = }")
            logger.info(f"{self.constants.polcal_readout_exp_times = }")
        logger.info(f"{self.constants.observe_exposure_times = }")
        logger.info(f"{self.constants.observe_readout_exp_times = }")


class ShowMapMapping(VispTaskBase):
    def run(self) -> None:
        logger.info(f"Found {self.constants.num_map_scans} map scans")
        step = 0
        logger.info(f"Step {step} is organized thusly:")
        for map in range(1, self.constants.num_map_scans + 1):
            logger.info(f"Map #{map}:")
            for mod in range(1, self.constants.num_modstates + 1):
                fits_obj = list(
                    self.fits_data_read_fits_access(
                        tags=[
                            VispTag.input(),
                            VispTag.frame(),
                            VispTag.map_scan(map),
                            VispTag.modstate(mod),
                            VispTag.raster_step(step),
                        ],
                        cls=VispL0FitsAccess,
                    )
                )
                logger.info(
                    f"\tModstate {mod} has {len(fits_obj)} files. Date is {fits_obj[0].time_obs}"
                )


class SubmitAndExposeQuality(VispSubmitQuality):
    """A direct copy paste of SumbitQuality with an additional step of writing the report to disk"""

    def run(self):

        # To make sure the subclassing worked
        super().run()

        # Now regenerate the report str and save it
        logger.info("Building quality report for save to disk")
        report_str = self.quality_build_report(polcal_label_list=self.polcal_label_list)

        doc_path = self.scratch.workflow_base_path / "quality_report.json"
        report_container = {
            "datasetId": self.constants.dataset_id,
            "qualityReport": json.dumps(report_str, cls=DatetimeEncoder),
        }
        json_str = json.dumps(report_container)
        with open(doc_path, "w") as f:
            f.write(json_str)
        logger.info(f"Wrote report to {doc_path}")


class ValidateL1Output(VispTaskBase):
    def run(self) -> None:
        files = self.read(tags=[VispTag.output(), VispTag.frame()])
        for f in files:
            logger.info(f"Validating {f}")
            spec214_validator.validate(f, extra=False)


def setup_APM_config() -> None:
    mesh_config = {
        "system-monitoring-log-apm": {
            "mesh_address": "system-monitoring-log-apm.service.sim.consul",
            "mesh_port": 8200,
        },
        "automated-processing-scratch-inventory": {"mesh_address": "localhost", "mesh_port": 6379},
        "internal-api-gateway": {"mesh_address": "localhost", "mesh_port": 80},
    }
    apm_options = {"TRANSACTION_MAX_SPANS": 10000}
    os.environ["MESH_CONFIG"] = json.dumps(mesh_config)
    os.environ["ELASTIC_APM_ENABLED"] = "true"
    os.environ["ELASTIC_APM_OTHER_OPTIONS"] = json.dumps(apm_options)


def make_pdf_report(scratch_path: str, recipe_run_id: int) -> None:
    if not QRM:
        logger.info("Did NOT make quality report pdf because quality_report_maker is not installed")
        return

    json_file = os.path.join(scratch_path, str(recipe_run_id), "quality_report.json")
    pdf_file = os.path.join(scratch_path, str(recipe_run_id), "quality_report.pdf")
    with open(json_file, "r") as f:
        report_container = json.load(f)
        dataset_id = report_container["datasetId"]
        report_dict = json.loads(
            report_container["qualityReport"], object_hook=datetime_json_object_hook
        )

    pdf_bytes = report.format_report(report_dict, f"GROGU_TEST_{dataset_id}")
    with open(pdf_file, "wb") as f:
        f.write(pdf_bytes)

    logger.info(f"Wrote quality report PDF to {pdf_file}")


def make_dataset_asdf(recipe_run_id, scratch_path):
    if not INV:
        logger.warning("Did NOT make dataset asdf file because dkist_inventory is not installed")
        return

    output_dir = os.path.join(scratch_path, str(recipe_run_id))
    asdf_name = f"dataset_{recipe_run_id:03n}.asdf"
    logger.info(f"Creating ASDF file from {output_dir} and saving to {asdf_name}")
    dataset_from_fits(output_dir, asdf_name, hdu=1)


def main(
    scratch_path: str,
    suffix: str = "FITS",
    recipe_run_id: int = 2,
    skip_translation: bool = False,
    only_translate: bool = False,
    load_input_parsing: bool = False,
    load_dark: bool = False,
    load_background: bool = False,
    load_lamp: bool = False,
    load_geometric: bool = False,
    load_solar: bool = False,
    load_inst_pol: bool = False,
    use_apm: bool = False,
    transfer_trial_data: str | None = None,
):
    if use_apm:
        setup_APM_config()
    with ManualProcessing(
        workflow_path=scratch_path,
        recipe_run_id=recipe_run_id,
        testing=True,
        workflow_name="visp-l0-pipeline",
        workflow_version="GROGU",
    ) as manual_processing_run:
        if not skip_translation:
            manual_processing_run.run_task(task=Translate122To214L0)
        if only_translate:
            return
        manual_processing_run.run_task(task=CreateInputDatasetParameterDocument)

        if load_input_parsing:
            manual_processing_run.run_task(task=LoadInputParsing)
        else:
            manual_processing_run.run_task(task=tag_inputs_task(suffix))
            manual_processing_run.run_task(task=ParseL0VispInputData)
            manual_processing_run.run_task(task=SaveInputParsing)

        manual_processing_run.run_task(task=ShowMapMapping)
        manual_processing_run.run_task(task=VispL0QualityMetrics)
        manual_processing_run.run_task(task=ShowPolMode)
        manual_processing_run.run_task(task=ShowExposureTimes)

        if load_dark:
            manual_processing_run.run_task(task=LoadDarkCal)
        else:
            manual_processing_run.run_task(task=DarkCalibration)
            manual_processing_run.run_task(task=SaveDarkCal)

        if load_background:
            manual_processing_run.run_task(task=LoadBackgroundCal)
        else:
            manual_processing_run.run_task(task=BackgroundLightCalibration)
            manual_processing_run.run_task(task=SaveBackgroundCal)

        if load_lamp:
            manual_processing_run.run_task(task=LoadLampCal)
        else:
            manual_processing_run.run_task(task=LampCalibration)
            manual_processing_run.run_task(task=SaveLampCal)

        if load_geometric:
            manual_processing_run.run_task(task=LoadGeometricCal)
        else:
            manual_processing_run.run_task(task=GeometricCalibration)
            manual_processing_run.run_task(task=SaveGeometricCal)

        if load_solar:
            manual_processing_run.run_task(task=LoadSolarCal)
        else:
            manual_processing_run.run_task(task=SolarCalibration)
            manual_processing_run.run_task(task=SaveSolarCal)

        if load_inst_pol:
            manual_processing_run.run_task(task=LoadInstPolCal)
        else:
            manual_processing_run.run_task(task=InstrumentPolarizationCalibration)
            manual_processing_run.run_task(task=SaveInstPolCal)

        manual_processing_run.run_task(task=ScienceCalibration)
        manual_processing_run.run_task(task=VispWriteL1Frame)
        manual_processing_run.run_task(task=QualityL1Metrics)
        manual_processing_run.run_task(task=VispL1QualityMetrics)
        manual_processing_run.run_task(task=SubmitAndExposeQuality)
        manual_processing_run.run_task(task=ValidateL1Output)
        manual_processing_run.run_task(task=MakeVispMovieFrames)
        manual_processing_run.run_task(task=AssembleVispMovie)

        if transfer_trial_data:
            if transfer_trial_data == "default":
                trial_output_dir = (
                    Path(manual_processing_run.workflow_path) / str(recipe_run_id) / "trial_output"
                )
            else:
                trial_output_dir = Path(transfer_trial_data).absolute()

            logger.info(f"Writing trial output to {trial_output_dir}")
            transfer_local_task = transfer_trial_data_locally_task(trial_dir=trial_output_dir)
            manual_processing_run.run_task(transfer_local_task)

        # Test some downstream services
        make_pdf_report(scratch_path, recipe_run_id)
        make_dataset_asdf(recipe_run_id, scratch_path)

        if any([load_dark, load_lamp, load_geometric, load_solar, load_inst_pol]):
            logger.info("NOT counting provenance records because some tasks were skipped")
        else:
            manual_processing_run.count_provenance()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run an end-to-end test of the ViSP DC Science pipeline"
    )
    parser.add_argument("scratch_path", help="Location to use as the DC 'scratch' disk")
    parser.add_argument(
        "-i",
        "--run-id",
        help="Which subdir to use. This will become the recipe run id",
        type=int,
        default=4,
    )
    parser.add_argument("--suffix", help="File suffix to treat as INPUT frames", default="FITS")
    parser.add_argument(
        "-T",
        "--skip-translation",
        help="Skip the translation of raw 122 l0 frames to 214 l0",
        action="store_true",
    )
    parser.add_argument(
        "-t", "--only-translate", help="Do ONLY the translation step", action="store_true"
    )
    parser.add_argument(
        "-X",
        "--transfer-trial-data",
        help="Transfer trial data to a different location.",
        nargs="?",
        const="default",
        default=None,
    )
    parser.add_argument(
        "-I", "--load-input-parsing", help="Load tags on input files", action="store_true"
    )
    parser.add_argument(
        "-D",
        "--load-dark",
        help="Load dark calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-B",
        "--load-background",
        help="Load background light calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-L",
        "--load-lamp",
        help="Load lamp calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-G",
        "--load-geometric",
        help="Load geometric calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-S",
        "--load-solar",
        help="Load solar calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-P",
        "--load-inst-pol",
        help="Load instrument polarization calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument("-A", "--use-apm", help="Send APM spans to SIM", action="store_true")
    args = parser.parse_args()
    sys.exit(
        main(
            scratch_path=args.scratch_path,
            suffix=args.suffix,
            recipe_run_id=args.run_id,
            skip_translation=args.skip_translation,
            only_translate=args.only_translate,
            load_input_parsing=args.load_input_parsing,
            load_dark=args.load_dark,
            load_background=args.load_background,
            load_lamp=args.load_lamp,
            load_geometric=args.load_geometric,
            load_solar=args.load_solar,
            load_inst_pol=args.load_inst_pol,
            use_apm=args.use_apm,
            transfer_trial_data=args.transfer_trial_data,
        )
    )
