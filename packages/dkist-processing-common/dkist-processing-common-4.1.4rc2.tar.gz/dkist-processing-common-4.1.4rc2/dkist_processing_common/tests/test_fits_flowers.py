import pytest
from astropy.io import fits

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.fits_access import FitsAccessBase
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.parsers.cs_step import CSStepFlower
from dkist_processing_common.parsers.cs_step import NumCSStepBud
from dkist_processing_common.parsers.dsps_repeat import DspsRepeatNumberFlower
from dkist_processing_common.parsers.proposal_id_bud import ProposalIdBud
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)
from dkist_processing_common.parsers.time import AverageCadenceBud
from dkist_processing_common.parsers.time import ExposureTimeFlower
from dkist_processing_common.parsers.time import MaximumCadenceBud
from dkist_processing_common.parsers.time import MinimumCadenceBud
from dkist_processing_common.parsers.time import ReadoutExpTimeFlower
from dkist_processing_common.parsers.time import TaskExposureTimesBud
from dkist_processing_common.parsers.time import TaskReadoutExpTimesBud
from dkist_processing_common.parsers.time import VarianceCadenceBud
from dkist_processing_common.parsers.unique_bud import UniqueBud


class FitsReader(FitsAccessBase):
    def __init__(self, hdu, name):
        super().__init__(hdu, name)
        self.thing_id: int = self.header["id_key"]
        self.constant_thing: float = self.header["constant"]
        self.name = name
        self.proposal_id: str = self.header.get("ID___013")
        self.ip_task_type: str = self.header.get("DKIST004")
        self.fpa_exposure_time_ms: float = self.header.get("XPOSURE")
        self.sensor_readout_exposure_time_ms: float = self.header.get("TEXPOSUR")
        self.num_raw_frames_per_fpa: int = self.header.get("NSUMEXP")
        self.num_dsps_repeats: int = self.header["DSPSREPS"]
        self.current_dsps_repeat: int = self.header["DSPSNUM"]
        self.time_obs: str = self.header["DATE-OBS"]


@pytest.fixture()
def basic_header_objs():
    header_dict = {
        "thing0": fits.header.Header(
            {
                "id_key": 0,
                "constant": 6.28,
                "DKIST004": "observe",
                "ID___013": "proposal_id_1",
                "XPOSURE": 0.0013000123,
                "TEXPOSUR": 10.0,
                "NSUMEXP": 3,
                "DSPSNUM": 1,
                "DSPSREPS": 2,
                "DATE-OBS": "2022-06-17T22:00:00.000",
            }
        ),
        "thing1": fits.header.Header(
            {
                "id_key": 1,
                "constant": 6.28,
                "DKIST004": "observe",
                "ID___013": "proposal_id_1",
                "XPOSURE": 0.0013000987,
                "TEXPOSUR": 10.0,
                "NSUMEXP": 3,
                "DSPSNUM": 1,
                "DSPSREPS": 2,
                "DATE-OBS": "2022-06-17T22:00:01.000",
            }
        ),
        "thing2": fits.header.Header(
            {
                "id_key": 2,
                "constant": 6.28,
                "DKIST004": "dark",
                "ID___013": "proposal_id_2",
                "XPOSURE": 12.345,
                "TEXPOSUR": 1.123456789,
                "NSUMEXP": 1,
                "DSPSNUM": 2,
                "DSPSREPS": 2,
                "DATE-OBS": "2022-06-17T22:00:02.000",
            }
        ),
        "thing3": fits.header.Header(
            {
                "id_key": 0,
                "constant": 6.28,
                "DKIST004": "observe",
                "ID___013": "proposal_id_1",
                "XPOSURE": 100.0,
                "TEXPOSUR": 11.0,
                "NSUMEXP": 4,
                "DSPSNUM": 2,
                "DSPSREPS": 2,
                "DATE-OBS": "2022-06-17T22:00:03.000",
            }
        ),
    }
    return (FitsReader.from_header(header, name=path) for path, header in header_dict.items())


@pytest.fixture()
def bad_header_objs():
    bad_headers = {
        "thing0": fits.header.Header(
            {
                "id_key": 0,
                "constant": 6.28,
                "DSPSREPS": 2,
                "DSPSNUM": 2,
                "DATE-OBS": "2022-06-17T22:00:00.000",
            }
        ),
        "thing1": fits.header.Header(
            {
                "id_key": 1,
                "constant": 3.14,
                "DSPSREPS": 2,
                "DSPSNUM": 2,
                "DATE-OBS": "2022-06-17T22:00:03.000",
            }
        ),
    }
    return (FitsReader.from_header(header, name=path) for path, header in bad_headers.items())


def test_unique_bud(basic_header_objs):
    """
    Given: A set of headers with a constant value header key
    When: Ingesting headers with a UniqueRock and asking for the value
    Then: The Rock's value is the header constant value
    """
    bud = UniqueBud(
        constant_name="constant",
        metadata_key="constant_thing",
    )
    assert bud.stem_name == "constant"
    for fo in basic_header_objs:
        key = fo.name
        bud.update(key, fo)

    petal = list(bud.petals)
    assert len(petal) == 1
    assert petal[0].value == 6.28


def test_unique_bud_non_unique_inputs(bad_header_objs):
    """
    Given: A set of headers with a non-constant header key that is expected to be constant
    When: Ingesting headers with a UniqueRock and asking for the value
    Then: An error is raised
    """
    rock = UniqueBud(
        constant_name="constant",
        metadata_key="constant_thing",
    )
    assert rock.stem_name == "constant"
    for fo in bad_header_objs:
        key = fo.name
        rock.update(key, fo)

    with pytest.raises(ValueError):
        assert next(rock.petals)


def test_single_value_single_key_flower(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with a single key that has a limited set of values
    When: Ingesting with a SingleValueSingleKeyFlower and asking for the grouping
    Then: The filepaths are grouped correctly based on the header key value
    """
    flower = SingleValueSingleKeyFlower(tag_stem_name="id", metadata_key="thing_id")
    assert flower.stem_name == "id"
    for fo in basic_header_objs:
        key = fo.name
        flower.update(key, fo)

    petals = sorted(list(flower.petals), key=lambda x: x.value)
    assert len(petals) == 3
    assert petals[0].value == 0
    assert petals[0].keys == ["thing0", "thing3"]
    assert petals[1].value == 1
    assert petals[1].keys == ["thing1"]
    assert petals[2].value == 2
    assert petals[2].keys == ["thing2"]


def test_cs_step_flower(grouped_cal_sequence_headers, non_polcal_headers, max_cs_step_time_sec):
    """
    Given: A set of PolCal headers, non-PolCal headers, and the CSStepFlower
    When: Updating the CSStepFlower with all headers
    Then: The flower correctly organizes the PolCal frames and ignores the non-PolCal frames
    """
    cs_step_flower = CSStepFlower(max_cs_step_time_sec=max_cs_step_time_sec)
    for step, headers in grouped_cal_sequence_headers.items():
        for i, h in enumerate(headers):
            key = f"step_{step}_file_{i}"
            cs_step_flower.update(key, h)

    for h in non_polcal_headers:
        cs_step_flower.update("non_polcal", h)

    assert len(list(cs_step_flower.petals)) == len(list(grouped_cal_sequence_headers.keys()))
    for step_petal in cs_step_flower.petals:
        assert sorted(step_petal.keys) == [
            f"step_{step_petal.value}_file_{i}" for i in range(len(step_petal.keys))
        ]


def test_num_cs_step_bud(grouped_cal_sequence_headers, non_polcal_headers, max_cs_step_time_sec):
    """
    Given: A set of PolCal headers, non-PolCal headers, and the NumCSStepRock
    When: Updating the NumCSStepRock with all headers
    Then: The rock reports the correct number of CS Steps (thus ignoring the non-PolCal frames)
    """
    num_cs_bud = NumCSStepBud(max_cs_step_time_sec=max_cs_step_time_sec)
    for step, headers in grouped_cal_sequence_headers.items():
        for h in headers:
            num_cs_bud.update(step, h)

    for h in non_polcal_headers:
        num_cs_bud.update("foo", h)

    bud = list(num_cs_bud.petals)
    assert len(bud) == 1
    assert bud[0].value == len(grouped_cal_sequence_headers.keys())


def test_proposal_id_bud(basic_header_objs):
    bud = ProposalIdBud()
    assert bud.stem_name == "PROPOSAL_ID"
    for fo in basic_header_objs:
        key = fo.name
        bud.update(key, fo)

    petal = list(bud.petals)
    assert len(petal) == 1
    assert petal[0].value == "proposal_id_1"


def test_exp_time_flower(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with XPOSURE keywords
    When: Ingesting with an ExposureTimeFlower
    Then: The filepaths are grouped correctly based on their exposure time
    """
    flower = ExposureTimeFlower()
    assert flower.stem_name == StemName.exposure_time.value
    for fo in basic_header_objs:
        key = fo.name
        flower.update(key, fo)

    petals = sorted(list(flower.petals), key=lambda x: x.value)
    assert len(petals) == 3
    assert petals[0].value == 0.0013
    assert petals[0].keys == ["thing0", "thing1"]
    assert petals[1].value == 12.345
    assert petals[1].keys == ["thing2"]
    assert petals[2].value == 100.0
    assert petals[2].keys == ["thing3"]


def test_readout_exp_time_flower(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with TEXPOSUR keywords
    When: Ingesting with an ReadoutExpTimeFlower
    Then: The filepaths are grouped correctly based on their readout exposure time
    """
    flower = ReadoutExpTimeFlower()
    assert flower.stem_name == StemName.readout_exp_time.value
    for fo in basic_header_objs:
        key = fo.name
        flower.update(key, fo)

    petals = sorted(list(flower.petals), key=lambda x: x.value)
    assert len(petals) == 3
    assert petals[0].value == 1.123457
    assert petals[0].keys == ["thing2"]
    assert petals[1].value == 10.0
    assert petals[1].keys == ["thing0", "thing1"]
    assert petals[2].value == 11.0
    assert petals[2].keys == ["thing3"]


def test_fpa_exp_times_bud(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with XPOSURE keywords
    When: Ingesting with a TaskExposureTimesBud
    Then: All (rounded) exposure times are accounted for in the resulting tuple
    """
    dark_bud = TaskExposureTimesBud(stem_name=BudName.dark_exposure_times, ip_task_type="DARK")
    obs_bud = TaskExposureTimesBud(stem_name="obs_exp_times", ip_task_type="OBSERVE")
    assert dark_bud.stem_name == BudName.dark_exposure_times.value
    for fo in basic_header_objs:
        key = fo.name
        dark_bud.update(key, fo)
        obs_bud.update(key, fo)

    dark_petal = list(dark_bud.petals)
    assert len(dark_petal) == 1
    assert type(dark_petal[0].value) is tuple
    assert tuple(sorted(dark_petal[0].value)) == (12.345,)

    obs_petal = list(obs_bud.petals)
    assert len(obs_petal) == 1
    assert type(obs_petal[0].value) is tuple
    assert tuple(sorted(obs_petal[0].value)) == (0.0013, 100.0)


def test_readout_exp_times_bud(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with TEXPOSUR keywords
    When: Ingesting with a TaskReadoutExpTimesBud
    Then: All (rounded) exposure times are accounted for in the resulting tuple
    """
    dark_bud = TaskReadoutExpTimesBud(stem_name=BudName.dark_exposure_times, ip_task_type="DARK")
    obs_bud = TaskReadoutExpTimesBud(stem_name="obs_exp_times", ip_task_type="OBSERVE")
    assert dark_bud.stem_name == BudName.dark_exposure_times.value
    for fo in basic_header_objs:
        key = fo.name
        dark_bud.update(key, fo)
        obs_bud.update(key, fo)

    dark_petal = list(dark_bud.petals)
    assert len(dark_petal) == 1
    assert type(dark_petal[0].value) is tuple
    assert tuple(sorted(dark_petal[0].value)) == (1.123457,)

    obs_petal = list(obs_bud.petals)
    assert len(obs_petal) == 1
    assert type(obs_petal[0].value) is tuple
    assert tuple(sorted(obs_petal[0].value)) == (10.0, 11.0)


def test_dsps_flower(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with DSPS keywords
    When: Ingesting with a DspsRepeatNumber Flower
    Then: The correct values are returned
    """
    flower = DspsRepeatNumberFlower()
    assert flower.stem_name == StemName.dsps_repeat.value
    for fo in basic_header_objs:
        key = fo.name
        flower.update(key, fo)

    petals = sorted(list(flower.petals), key=lambda x: x.value)
    assert len(petals) == 2
    assert petals[0].value == 1
    assert petals[0].keys == ["thing0", "thing1"]
    assert petals[1].value == 2
    assert petals[1].keys == ["thing3"]


def test_average_cadence_bud(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with DATE-OBS keywords
    When: Ingesting with the AverageCadenceBud
    Then: The correct values are returned
    """
    bud = AverageCadenceBud()
    assert bud.stem_name == BudName.average_cadence.value
    for fo in basic_header_objs:
        key = fo.name
        bud.update(key, fo)

    petal = list(bud.petals)
    assert len(petal) == 1

    # Because there are 3 observe frames in `basic_header_objs` spaced 1, and 2 seconds apart.
    assert petal[0].value == 1.5


def test_max_cadence_bud(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with DATE-OBS keywords
    When: Ingesting with the MaxCadenceBud
    Then: The correct values are returned
    """
    bud = MaximumCadenceBud()
    assert bud.stem_name == BudName.maximum_cadence.value
    for fo in basic_header_objs:
        key = fo.name
        bud.update(key, fo)

    petal = list(bud.petals)
    assert len(petal) == 1

    # Because there are 3 observe frames in `basic_header_objs` spaced 1, and 2 seconds apart.
    assert petal[0].value == 2


def test_minimum_cadence_bud(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with DATE-OBS keywords
    When: Ingesting with the MinimumCadenceBud
    Then: The correct values are returned
    """
    bud = MinimumCadenceBud()
    assert bud.stem_name == BudName.minimum_cadence.value
    for fo in basic_header_objs:
        key = fo.name
        bud.update(key, fo)

    petal = list(bud.petals)
    assert len(petal) == 1

    # Because there are 3 observe frames in `basic_header_objs` spaced 1, and 2 seconds apart.
    assert petal[0].value == 1


def test_variance_cadence_bud(basic_header_objs):
    """
    Given: A set of filepaths and associated headers with DATE-OBS keywords
    When: Ingesting with the VarianceCadenceBud
    Then: The correct values are returned
    """
    bud = VarianceCadenceBud()
    assert bud.stem_name == BudName.variance_cadence.value
    for fo in basic_header_objs:
        key = fo.name
        bud.update(key, fo)

    petal = list(bud.petals)
    assert len(petal) == 1

    # Because there are 3 observe frames in `basic_header_objs` spaced 1, and 2 seconds apart.
    assert petal[0].value == 0.25


# TODO: test new stems that have been added to parse_l0_input_data
