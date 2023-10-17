import os
import shutil
from pathlib import Path

import asdf
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_service_configuration import logger

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.trial_output_data import TransferVispTrialData


class SaveInputParsing(WorkflowTaskBase):
    """Dump redis db to file"""

    @property
    def relative_save_file(self) -> str:
        return "input_parsing_cal.asdf"

    def run(self):
        file_tag_dict = self.get_input_tags()
        constant_dict = self.get_constants()

        full_save_file = self.scratch.workflow_base_path / self.relative_save_file
        tree = {"file_tag_dict": file_tag_dict, "constants_dict": constant_dict}
        af = asdf.AsdfFile(tree)
        af.write_to(full_save_file)
        logger.info(f"Saved input tags to {full_save_file}")

    def get_input_tags(self) -> dict[str, list[str]]:
        file_tag_dict = dict()
        path_list = self.read(tags=[VispTag.input()])
        for p in path_list:
            tags = self.tags(p)
            file_tag_dict[str(p)] = tags

        return file_tag_dict

    def get_constants(self) -> dict[str, str | float | list]:
        constants_dict = dict()
        for c in self.constants._db_dict.keys():
            constants_dict[c] = self.constants._db_dict[c]

        return constants_dict


class LoadInputParsing(WorkflowTaskBase):
    """Load redis db (tags and constants) from a file."""

    @property
    def relative_save_file(self) -> str:
        return "input_parsing_cal.asdf"

    def run(self):
        full_save_file = self.scratch.workflow_base_path / self.relative_save_file
        with asdf.open(full_save_file) as af:
            file_tag_dict = af.tree["file_tag_dict"]
            self.tag_input_files(file_tag_dict)

            constants_dict = af.tree["constants_dict"]
            self.populate_constants(constants_dict)

        logger.info(f"Loaded input tags and constants from")

    def tag_input_files(self, file_tag_dict: dict[str, list[str]]):
        """Do."""
        for f, t in file_tag_dict.items():
            if not os.path.exists(f):
                raise FileNotFoundError(f"Expected to find {f}, but it doesn't exist.")
            self.tag(path=f, tags=t)

    def populate_constants(self, constants_dict: dict[str, str | int | float]) -> None:
        """Do."""
        for c, v in constants_dict.items():
            logger.info(f"Setting value of {c} to {v}")
            self.constants._update({c: v})


class SaveTaskTags(WorkflowTaskBase):
    @property
    def task_str(self) -> str:
        return "TASK"

    @property
    def relative_save_file(self) -> str:
        return "default_sav.asdf"

    def run(self):
        file_tag_dict = dict()
        path_list = self.read(tags=[VispTag.task(self.task_str), VispTag.intermediate()])
        save_dir = self.scratch.workflow_base_path / Path(self.relative_save_file).stem
        save_dir.mkdir(exist_ok=True)
        for p in path_list:
            copied_path = shutil.copy(str(p), save_dir)
            tags = self.tags(p)
            file_tag_dict[copied_path] = tags

        full_save_file = self.scratch.workflow_base_path / self.relative_save_file
        tree = {"file_tag_dict": file_tag_dict}
        af = asdf.AsdfFile(tree)
        af.write_to(full_save_file)
        logger.info(f"Saved {self.task_str} to {full_save_file}")


class LoadTaskTags(WorkflowTaskBase):
    @property
    def relative_save_file(self) -> str:
        return "default_sav.asdf"

    def run(self):
        full_save_file = self.scratch.workflow_base_path / self.relative_save_file
        with asdf.open(full_save_file) as af:
            for f, t in af.tree["file_tag_dict"].items():
                self.tag(path=f, tags=t)
        logger.info(f"Loaded database entries from {full_save_file}")


class SaveGeometricCal(WorkflowTaskBase):
    def run(self) -> None:
        relative_save_file = "geometric_cal.asdf"
        file_tag_dict = dict()
        path_list = list(self.read(tags=[VispTag.task("GEOMETRIC_ANGLE"), VispTag.intermediate()]))
        path_list += list(
            self.read(tags=[VispTag.task("GEOMETRIC_OFFSET"), VispTag.intermediate()])
        )
        path_list += list(
            self.read(tags=[VispTag.task("GEOMETRIC_SPEC_SHIFTS"), VispTag.intermediate()])
        )
        save_dir = self.scratch.workflow_base_path / Path(relative_save_file).stem
        save_dir.mkdir(exist_ok=True)
        for p in path_list:
            copied_path = shutil.copy(str(p), save_dir)
            tags = self.tags(p)
            file_tag_dict[copied_path] = tags

        full_save_file = self.scratch.workflow_base_path / relative_save_file
        tree = {"file_tag_dict": file_tag_dict}
        af = asdf.AsdfFile(tree)
        af.write_to(full_save_file)
        logger.info(f"Saved Geometric Calibration to {full_save_file}")


class LoadGeometricCal(LoadTaskTags):
    @property
    def relative_save_file(self) -> str:
        return "geometric_cal.asdf"


class SaveDarkCal(SaveTaskTags):
    @property
    def task_str(self) -> str:
        return "DARK"

    @property
    def relative_save_file(self) -> str:
        return "dark_cal.asdf"


class LoadDarkCal(LoadTaskTags):
    @property
    def relative_save_file(self) -> str:
        return "dark_cal.asdf"


class SaveBackgroundCal(SaveTaskTags):
    @property
    def task_str(self) -> str:
        return "BACKGROUND"

    @property
    def relative_save_file(self) -> str:
        return "background_cal.asdf"


class LoadBackgroundCal(LoadTaskTags):
    @property
    def relative_save_file(self) -> str:
        return "background_cal.asdf"


class SaveLampCal(SaveTaskTags):
    @property
    def task_str(self) -> str:
        return "LAMP_GAIN"

    @property
    def relative_save_file(self) -> str:
        return "lamp_cal.asdf"


class LoadLampCal(LoadTaskTags):
    @property
    def relative_save_file(self) -> str:
        return "lamp_cal.asdf"


class SaveSolarCal(SaveTaskTags):
    @property
    def task_str(self) -> str:
        return "SOLAR_GAIN"

    @property
    def relative_save_file(self) -> str:
        return "solar_cal.asdf"


class LoadSolarCal(LoadTaskTags):
    @property
    def relative_save_file(self) -> str:
        return "solar_cal.asdf"


class SaveInstPolCal(SaveTaskTags):
    @property
    def task_str(self) -> str:
        return "DEMOD_MATRICES"

    @property
    def relative_save_file(self) -> str:
        return "inst_pol_cal.asdf"


class LoadInstPolCal(LoadTaskTags):
    @property
    def relative_save_file(self) -> str:
        return "inst_pol_cal.asdf"


def transfer_trial_data_locally_task(
    trial_dir: str | Path,
    debug_switch: bool = True,
    intermediate_switch: bool = True,
    output_swtich: bool = True,
    tag_lists: list | None = None,
):
    class LocalTrialData(TransferVispTrialData):
        @property
        def destination_folder(self) -> Path:
            return Path(trial_dir)

        @property
        def debug_frame_switch(self) -> bool:
            return debug_switch

        @property
        def intermediate_frame_switch(self) -> bool:
            return intermediate_switch

        @property
        def output_frame_switch(self) -> bool:
            return output_swtich

        @property
        def specific_frame_tag_lists(self) -> list:
            return tag_lists or []

        def remove_folder_objects(self):
            logger.info("Would have removed folder objects here")

        def globus_transfer_scratch_to_object_store(
            self,
            transfer_items: list[GlobusTransferItem],
            label: str = None,
            sync_level: str = None,
            verify_checksum: bool = True,
        ) -> None:
            if label:
                logger.info(f"Transferring files with {label = }")

            for frame in transfer_items:
                if not frame.destination_path.parent.exists():
                    frame.destination_path.parent.mkdir(parents=True)
                os.system(f"cp {frame.source_path} {frame.destination_path}")

    return LocalTrialData
