"""Trial tasks"""
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_processing_common.tasks.trial_output_data import TransferTrialDataBase
from dkist_service_configuration import logger


class TransferTestTrialData(TransferTrialDataBase):
    @property
    def intermediate_task_names(self) -> list[str]:
        """Return a list of intermediate tasks we want to transfer.

        Just a dummy task for testing.
        """
        return ["DUMMY"]

    def build_transfer_list(self) -> list[GlobusTransferItem]:
        """
        Build a list containing all files we want to transfer to the trial environment.

        For the purposes of testing we try to exercise all of the provided helper methods.
        """
        transfer_list = []

        transfer_list += self.build_debug_frame_transfer_list()

        transfer_list += self.build_intermediate_frame_transfer_list()

        transfer_list += self.build_output_frame_transfer_list()

        transfer_list += self.build_transfer_list_from_tag_lists([["FOO", "BAR"], ["BAZ"]])

        logger.info(f"{transfer_list = }")

        return transfer_list
