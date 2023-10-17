"""Tasks for transferring scratch data to custom location for post-pipeline analysis."""
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_processing_common.tasks.trial_output_data import TransferTrialDataBase


class TransferVispTrialData(TransferTrialDataBase):
    """Transfer DEBUG, Intermediate, and/or output data to the trial location."""

    @property
    def intermediate_task_names(self) -> list[str]:
        """Grab all the Calibration products used to calibrate science data."""
        return [
            "DARK",
            "BACKGROUND",
            "LAMP_GAIN",
            "GEOMETRIC_ANGLE",
            "GEOMETRIC_OFFSET",
            "GEOMETRIC_SPEC_SHIFTS",
            "SOLAR_GAIN",
            "DEMOD_MATRICES",
        ]

    def build_transfer_list(self) -> list[GlobusTransferItem]:
        """
        Build a list containing all files we want to transfer to the trial environment.

        The classes of/specific files to transfer are defined in the switches that look at the recipe run configuration.
        """
        transfer_list = []

        if self.debug_frame_switch:
            transfer_list += self.build_debug_frame_transfer_list()

        if self.intermediate_frame_switch:
            transfer_list += self.build_intermediate_frame_transfer_list()

        if self.output_frame_switch:
            transfer_list += self.build_output_frame_transfer_list()

        if self.specific_frame_tag_lists:
            transfer_list += self.build_transfer_list_from_tag_lists(self.specific_frame_tag_lists)

        return transfer_list
