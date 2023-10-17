import numpy as np
import pytest
from astropy.io import fits

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.fits_access import FitsAccessBase
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin


class FitsTask(WorkflowTaskBase, FitsDataMixin):
    def run(self) -> None:
        pass


class DummyFitsAccess(FitsAccessBase):
    def __init__(
        self,
        hdu: fits.ImageHDU | fits.PrimaryHDU | fits.CompImageHDU,
        name: str | None = None,
        auto_squeeze: bool = True,
    ):
        super().__init__(hdu=hdu, name=name, auto_squeeze=auto_squeeze)
        self.bar: str = self.header["FOO"]


@pytest.fixture
def fits_task(tmp_path, recipe_run_id):
    with FitsTask(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        yield task
    task._purge()


@pytest.fixture()
def random_data() -> np.ndarray:
    return np.ones(10) * np.random.random()


@pytest.fixture()
def dummy_header() -> fits.Header:
    return fits.Header({"FOO": "BAR"})


@pytest.fixture()
def fits_task_with_tagged_fits_file(fits_task, random_data, dummy_header, compressed):

    if compressed:
        hdul = fits.HDUList(
            [fits.PrimaryHDU(), fits.CompImageHDU(random_data, header=dummy_header)]
        )
    else:
        hdul = fits.HDUList([fits.PrimaryHDU(random_data, header=dummy_header)])
    filename = fits_task.scratch.workflow_base_path / "foo.fits"
    hdul.writeto(filename)
    fits_task.tag(filename, [Tag.task("FOO")])

    return fits_task, filename


@pytest.mark.parametrize(
    "compressed", [pytest.param(False, id="Uncompressed"), pytest.param(True, id="Compressed")]
)
def test_fits_data_read_hdu(fits_task_with_tagged_fits_file, random_data):
    """
    Given: A task with the FitsDataMixin and a FITS file in scratch
    When: Reading a fits file with fits_data_read_hdu
    Then: The correct HDU (i.e., the one with data) is returned
    """
    task, _ = fits_task_with_tagged_fits_file

    res_list = list(task.fits_data_read_hdu(tags=[Tag.task("FOO")]))
    assert len(res_list) == 1
    res = res_list[0]
    assert np.array_equal(res.data, random_data)


@pytest.mark.parametrize(
    "compressed", [pytest.param(False, id="Uncompressed"), pytest.param(True, id="Compressed")]
)
def test_fits_data_read_fits_access(fits_task_with_tagged_fits_file, random_data):
    """
    Given: A task with the FitsDataMixin and a FITS file in scratch
    When: Reading a fits file with fits_data_read_fits_access
    Then: A FitsAccess object with the correct header and data is returned
    """
    task, filename = fits_task_with_tagged_fits_file

    res_list = list(task.fits_data_read_fits_access(tags=[Tag.task("FOO")], cls=DummyFitsAccess))
    assert len(res_list) == 1
    res = res_list[0]
    assert isinstance(res, DummyFitsAccess)
    assert res.name == str(filename)
    assert np.array_equal(res.data, random_data)
    assert res.bar == "BAR"


@pytest.mark.parametrize(
    "overwrite", [pytest.param(True, id="Overwrite"), pytest.param(False, id="No Overwrite")]
)
def test_fits_data_write(fits_task, random_data, dummy_header, overwrite):
    """
    Given: A task with the FitsDataMixin
    When: Writing an HDUList to scratch with fits_data_write
    Then: The file is correctly written
    """
    expected_data = random_data
    hdul = fits.HDUList([fits.PrimaryHDU(random_data, header=dummy_header)])
    filename = "foo.fits"
    fits_task.fits_data_write(hdu_list=hdul, tags=[Tag.intermediate()], relative_path=filename)

    hdul2 = fits.HDUList([fits.PrimaryHDU(random_data * 2, header=dummy_header)])
    if overwrite:
        expected_data = random_data * 2
        fits_task.fits_data_write(
            hdu_list=hdul2, tags=[Tag.intermediate()], relative_path=filename, overwrite=True
        )
    else:
        with pytest.raises(FileExistsError):
            fits_task.fits_data_write(
                hdu_list=hdul2, tags=[Tag.intermediate()], relative_path=filename, overwrite=False
            )

    res_list = list(fits_task.read([Tag.intermediate()]))
    assert len(res_list) == 1
    res = res_list[0]
    assert res.name == filename
    res_hdul = fits.open(res)
    assert len(res_hdul) == 1
    assert np.array_equal(res_hdul[0].data, expected_data)
    assert res_hdul[0].header["FOO"] == "BAR"
