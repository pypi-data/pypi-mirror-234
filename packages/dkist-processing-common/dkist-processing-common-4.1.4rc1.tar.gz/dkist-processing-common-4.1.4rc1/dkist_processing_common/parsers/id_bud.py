"""Base classes for ID bud parsing."""
from typing import Type

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess
from dkist_processing_common.parsers.unique_bud import UniqueBud


class IdBud(UniqueBud):
    """Base class for ID buds."""

    def __init__(self, constant_name, metadata_key):
        super().__init__(constant_name=constant_name, metadata_key=metadata_key)

    def setter(self, fits_obj: L0FitsAccess) -> str | Type[SpilledDirt]:
        """
        Set the id.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The id
        """
        if fits_obj.ip_task_type == "observe":
            return getattr(fits_obj, self.metadata_key)
        return SpilledDirt


class ContributingIdsBud(Stem):
    """Base class for contributing ID buds."""

    def __init__(self, stem_name, metadata_key):
        super().__init__(stem_name=stem_name)
        self.metadata_key = metadata_key

    def setter(self, fits_obj: L0FitsAccess) -> str | Type[SpilledDirt]:
        """
        Set the id for any type of frame.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The id
        """
        return getattr(fits_obj, self.metadata_key)

    def getter(self, key) -> tuple:
        """
        Get all ids seen in non observe frames.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        IDs from non observe frames
        """
        return tuple(set(self.key_to_petal_dict.values()))
