import json
from datetime import datetime
from typing import Any

import pytest

from dkist_processing_common.models.parameters import ParameterBase
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin


INPUT_DATASET = [
    {
        "parameterName": "param_name",
        "parameterValues": [
            {
                "parameterValueId": 1,
                "parameterValue": json.dumps([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                "parameterValueStartDate": "2000-01-01",
            }
        ],
    }
]

INPUT_DATASET_PARAMETERS_ONLY_NO_DATE = [
    {
        "parameterName": "param_name",
        "parameterValues": [{"parameterValueId": 1, "parameterValue": json.dumps(4)}],
    }
]

INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES = [
    {
        "parameterName": "param_name",
        "parameterValues": [
            {
                "parameterValueId": 1,
                "parameterValue": json.dumps(4),
                "parameterValueStartDate": "2020-03-13",
            },
            {
                "parameterValueId": 2,
                "parameterValue": json.dumps(6),
                "parameterValueStartDate": "1955-01-02",
            },
            {
                "parameterValueId": 3,
                "parameterValue": json.dumps(5),
                "parameterValueStartDate": "2021-12-15",
            },
        ],
    }
]

INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES_NO_DATE = [
    {
        "parameterName": "param_name",
        "parameterValues": [
            {"parameterValueId": 1, "parameterValue": json.dumps(4)},
            {
                "parameterValueId": 2,
                "parameterValue": json.dumps(6),
                "parameterValueStartDate": "1955-01-02",
            },
        ],
    }
]


class FilledParameters(ParameterBase):
    @property
    def test_parameter(self):
        return self._find_most_recent_past_value("param_name")


class ParameterScienceTask(WorkflowTaskBase, InputDatasetMixin):
    """An example of how parameters will be used in instrument repos"""

    def __init__(self, recipe_run_id: int, workflow_name: str, workflow_version: str):
        super().__init__(recipe_run_id, workflow_name, workflow_version)
        self.parameters = FilledParameters(self.input_dataset_parameters)

    def run(self) -> None:
        pass


@pytest.fixture()
def task_with_parameters(task_with_input_dataset):
    return ParameterScienceTask(
        recipe_run_id=task_with_input_dataset.recipe_run_id,
        workflow_name=task_with_input_dataset.workflow_name,
        workflow_version=task_with_input_dataset.workflow_version,
    )


@pytest.mark.parametrize(
    "input_dataset_parts",
    [pytest.param((INPUT_DATASET, Tag.input_dataset_parameters()), id="INPUT_DATASET")],
)
def test_parameters(task_with_parameters, input_dataset_parts: tuple[Any, str]):
    """
    Given: a ParameterBase subclass with populated parameters
    When: asking for a specific parameter value
    Then: the correct value is returned
    """
    assert task_with_parameters.parameters.test_parameter == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


@pytest.mark.parametrize(
    "input_dataset_parts",
    [pytest.param((INPUT_DATASET, Tag.input_dataset_parameters()), id="INPUT_DATASET")],
)
def test_find_most_recent_date_out_of_range(
    task_with_parameters, input_dataset_parts: tuple[Any, str]
):
    """
    Given: a ParameterBase subclass with populated parameters
    When: asking for a specific parameter value at a time that is too far in the past
    Then: an error is raised
    """
    with pytest.raises(ValueError):
        task_with_parameters.parameters._find_most_recent_past_value(
            "param_name", start_date=datetime(1776, 7, 4)
        )


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param(
            (INPUT_DATASET_PARAMETERS_ONLY_NO_DATE, Tag.input_dataset_parameters()),
            id="INPUT_DATASET_PARAMETERS_ONLY_NO_DATE",
        )
    ],
)
def test_parameters_get_no_startdate(task_with_parameters, input_dataset_parts: tuple[Any, str]):
    """
    Given: a ParameterBase subclass initialized with a parameter with no start_date
    When: asking for that specific parameter
    Then: the correct value is returned
    """
    assert task_with_parameters.parameters.test_parameter == 4


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param(
            (INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES, Tag.input_dataset_parameters()),
            id="INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES",
        )
    ],
)
def test_find_most_recent_multiple_dates(
    task_with_parameters, input_dataset_parts: tuple[Any, str]
):
    """
    Given: a ParameterBase subclass with a parameter with multiple values
    When: asking for that specific parameter
    Then: the correct (i.e., most recent) value is returned
    """
    assert (
        task_with_parameters.parameters._find_most_recent_past_value(
            "param_name", start_date=datetime(2021, 1, 1)
        )
        == 4
    )


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param(
            (INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES_NO_DATE, Tag.input_dataset_parameters()),
            id="INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES_NO_DATE",
        )
    ],
)
def test_parameter_get_multiple_values_no_start_date(
    task_with_parameters, input_dataset_parts: tuple[Any, str]
):
    """
    Given: a ParameterBase subclass with a parameter with multiple values, one of which has no start date
    When: asking for that specific parameter
    Then: the value with *any* date is returned
    """
    assert task_with_parameters.parameters.test_parameter == 6


@pytest.mark.parametrize(
    "input_dataset_parts",
    [pytest.param((INPUT_DATASET, Tag.input_dataset_parameters()), id="INPUT_DATASET")],
)
def test_parameters_on_task(task_with_parameters):
    """
    Given: a Task that inits a ParameterBase subclass
    When: asking for a parameter
    Then: the correct value is returned
    """
    assert task_with_parameters.parameters.test_parameter == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
