"""Base tasks to support transferring an arbitrary collection of files to a customizable post-run location."""
import logging
from abc import ABC
from abc import abstractmethod
from functools import cached_property
from pathlib import Path

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.mixin.globus import GlobusMixin
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_processing_common.tasks.output_data_base import TransferDataBase

logger = logging.getLogger(__name__)


class TransferTrialDataBase(TransferDataBase, GlobusMixin, ABC):
    """
    Base class for transferring data to a customizable post-run location.

    Provides the basic framework of locating and transferring data, but the specific files to be transferred must be
    identified by subclasses.

    Some helper methods that support common conventions are provided:

    o `build_debug_frame_transfer_list` - Transfer all frames tagged with DEBUG

    o `build_intermediate_frame_transfer_list` - Transfer subsets of frames tagged with INTERMEDIATE
    """

    def transfer_objects(self) -> None:
        """Collect transfer items and send them to Globus for transfer."""
        with self.apm_task_step("Build transfer list"):
            transfer_manifest = self.build_transfer_list()

        with self.apm_task_step("Send transfer manifest to globus"):
            self.transfer_all_trial_frames(transfer_manifest)

    @cached_property
    def destination_bucket(self) -> str:
        """Get the destination bucket with a trial default."""
        return self.metadata_store_recipe_run_configuration().get("destination_bucket", "etc")

    @property
    def destination_root_folder(self) -> Path:
        """Format the destination root folder with a value that can be set in the recipe run configuration."""
        root_name_from_configuration = self.metadata_store_recipe_run_configuration().get(
            "trial_root_directory_name"
        )
        root_name = Path(root_name_from_configuration or super().destination_root_folder)

        return root_name

    @property
    def destination_folder(self) -> Path:
        """Format the destination folder with a parent that can be set by the recipe run configuration."""
        dir_name = self.metadata_store_recipe_run_configuration().get(
            "trial_directory_name"
        ) or Path(self.constants.dataset_id)
        return self.destination_root_folder / dir_name

    @property
    def debug_frame_switch(self) -> bool:
        """Switch to turn on/off the transfer of DEBUG frames to the trial location."""
        return self.metadata_store_recipe_run_configuration().get(
            "trial_transfer_debug_frames", True
        )

    @property
    def intermediate_frame_switch(self) -> bool:
        """Switch to turn on/off the transfer of INTERMEDIATE frames to the trial location."""
        return self.metadata_store_recipe_run_configuration().get(
            "trial_transfer_intermediate_frames", True
        )

    @property
    def output_frame_switch(self) -> bool:
        """Switch to turn on/off the transfer of OUTPUT frames to the trial location."""
        return self.metadata_store_recipe_run_configuration().get(
            "trial_transfer_output_frames", True
        )

    @property
    def specific_frame_tag_lists(self) -> list:
        """Return list of tag lists that define specific files we want to transfer to the trial location."""
        return self.metadata_store_recipe_run_configuration().get("trial_transfer_tag_lists", [])

    @abstractmethod
    def build_transfer_list(self) -> list[GlobusTransferItem]:
        """Build a list of all items on scratch to transfer to the trial location."""
        pass

    def build_transfer_list_from_tag_lists(
        self, tag_lists: list[str] | list[list[str]]
    ) -> list[GlobusTransferItem]:
        """
        Build a transfer list containing all files that are tagged with any of the sets of input tags.

        For example, if `tag_lists` is [list1, list2,... listn] then the resulting transfer list will contain:

        ALL(list1) + ALL(list2) + ... + ALL(listn)

        Parameters
        ----------
        tag_lists
            Each element is a list of tags for a single type of file we want to transfer. A single list for a single
            type of file is also acceptable.
        """
        if len(tag_lists) == 0:
            return []

        if isinstance(tag_lists[0], str):
            tag_lists = [tag_lists]

        transfer_items = []
        for tag_set in tag_lists:

            paths = self.read(tags=tag_set)
            for p in paths:
                destination_object_key = self.format_object_key(p)
                destination_path = Path(self.destination_bucket, destination_object_key)
                item = GlobusTransferItem(
                    source_path=p,
                    destination_path=destination_path,
                )
                transfer_items.append(item)

        return list(set(transfer_items))

    def build_debug_frame_transfer_list(self) -> list[GlobusTransferItem]:
        """Build a transfer list containing all frames tagged with DEBUG."""
        transfer_items = self.build_transfer_list_from_tag_lists(
            tag_lists=[Tag.debug(), Tag.frame()]
        )
        return transfer_items

    @property
    def intermediate_task_names(self) -> list[str]:
        """List specifying which TASK types to build when selecting INTERMEDIATE frames."""
        return []

    def build_intermediate_frame_transfer_list(self) -> list[GlobusTransferItem]:
        """
        Build a transfer list containing a subset of frames tagged with INTERMEDIATE.

        More specifically, the intersection of INTERMEDIATE and the tasks defined in `intermediate_task_names`.
        """
        tag_lists = [[Tag.intermediate(), Tag.task(task)] for task in self.intermediate_task_names]
        transfer_items = self.build_transfer_list_from_tag_lists(tag_lists=tag_lists)
        return transfer_items

    def transfer_all_trial_frames(self, transfer_items: list[GlobusTransferItem]) -> None:
        """Send a list of transfer items to Globus for transfer."""
        logger.info(
            f"Preparing globus transfer {len(transfer_items)} items: "
            f"recipe_run_id={self.recipe_run_id}. "
            f"transfer_items={transfer_items[:3]}..."
        )

        self.globus_transfer_scratch_to_object_store(
            transfer_items=transfer_items,
            label=f"Transfer frames for trial run of recipe_run_id {self.recipe_run_id}",
        )
