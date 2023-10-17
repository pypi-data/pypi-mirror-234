"""Module for parsing IP task related things."""
from typing import Type

from dkist_processing_common.models.fits_access import FitsAccessBase


def passthrough_header_ip_task(fits_obj: Type[FitsAccessBase]) -> str:
    """
    Simply read the IP task directly from the header.

    AKA, default behavior.
    """
    return fits_obj.ip_task_type
