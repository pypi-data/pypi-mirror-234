import pytest
from astropy.io import fits

from dkist_processing_common.models.fits_access import FitsAccessBase
from dkist_processing_common.parsers.task import passthrough_header_ip_task


class DummyFitsAccess(FitsAccessBase):
    def __init__(
        self,
        hdu: fits.ImageHDU | fits.PrimaryHDU | fits.CompImageHDU,
        name: str | None = None,
        auto_squeeze: bool = False,  # Because L1 data should always have the right form, right?
    ):
        super().__init__(hdu=hdu, name=name, auto_squeeze=auto_squeeze)

        self.ip_task_type: str = self.header["IPTASK"]


@pytest.fixture
def fits_obj_with_task_type():

    task = "A_TASK"
    header = fits.Header({"IPTASK": task})
    hdu = fits.PrimaryHDU(data=None, header=header)
    return DummyFitsAccess(hdu=hdu), task


def test_passthrough_header_ip_task(fits_obj_with_task_type):
    """
    Given: A FitsAccess object with an ip task type property
    When: Parsing the task with the default parser
    Then: The raw task from the header is returned
    """
    fits_obj, task = fits_obj_with_task_type

    assert passthrough_header_ip_task(fits_obj) == task
