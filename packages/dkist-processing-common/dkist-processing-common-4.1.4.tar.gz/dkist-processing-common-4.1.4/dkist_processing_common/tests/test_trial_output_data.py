import json
from pathlib import Path
from uuid import uuid4

import pytest

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_processing_common.tasks.trial_output_data import TransferTrialDataBase


@pytest.fixture
def destination_bucket() -> str:
    return "crazy"


@pytest.fixture
def recipe_run_configuration(custom_root_name, custom_dir_name, destination_bucket):
    class GQLClientWithConfiguration:
        def __init__(self, *args, **kwargs):
            pass

        def execute_gql_query(self, **kwargs):
            query_base = kwargs["query_base"]
            if query_base == "recipeRuns":
                return [
                    RecipeRunResponse(
                        recipeInstanceId=1,
                        recipeInstance=None,
                        configuration=json.dumps(
                            {
                                "trial_root_directory_name": custom_root_name,
                                "trial_directory_name": custom_dir_name,
                                "destination_bucket": destination_bucket,
                            }
                        ),
                    ),
                ]

        @staticmethod
        def execute_gql_mutation(**kwargs):
            ...

    return GQLClientWithConfiguration


@pytest.fixture
def dummy_globus_transfer_item() -> GlobusTransferItem:
    return GlobusTransferItem(source_path="foo", destination_path="bar", recursive=True)


@pytest.fixture
def trial_output_task(dummy_globus_transfer_item):
    class TransferTrialData(TransferTrialDataBase):
        def build_transfer_list(self) -> list[GlobusTransferItem]:

            transfer_list = [dummy_globus_transfer_item]
            return transfer_list

        @property
        def intermediate_task_names(self) -> list[str]:
            return ["FOO"]

    return TransferTrialData


@pytest.fixture
def basic_trial_output_task(
    recipe_run_id, recipe_run_configuration, trial_output_task, tmp_path, mocker
):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=recipe_run_configuration,
    )
    proposal_id = "test_proposal_id"
    with trial_output_task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})
        yield task, proposal_id
        task._purge()


@pytest.fixture
def complete_trial_output_task(
    recipe_run_id, recipe_run_configuration, trial_output_task, tmp_path, mocker
):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=recipe_run_configuration,
    )
    proposal_id = "test_proposal_id"
    with trial_output_task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})

        # Write a debug frame
        debug_file_obj = uuid4().hex.encode("utf8")
        task.write(debug_file_obj, relative_path="debug.ext", tags=[Tag.debug(), Tag.frame()])

        # Write an intermediate frame that we want to transfer
        intermediate_keep_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_keep_file_obj,
            relative_path="intermediate.ext",
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("FOO")],
        )

        # Write an intermediate frame that we don't want to transfer
        intermediate_discard_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_discard_file_obj,
            relative_path="something_else.ext",
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("WHO_CARES")],
        )

        yield task, proposal_id, debug_file_obj, intermediate_keep_file_obj, intermediate_discard_file_obj
        task._purge()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name",
    [
        pytest.param("roor", "foo", id="Custom trial dir name"),
        pytest.param(None, None, id="Default trial dir name"),
    ],
)
def test_format_object_key(basic_trial_output_task, custom_root_name, custom_dir_name):
    """
    :Given: A base task made from TransferTrialDataBase
    :When: Formatting a path into an object key
    :Then: The expected object key is produced and includes a custom dir name if requested
    """
    task, proposal_id = basic_trial_output_task
    expected_root_name = custom_root_name or proposal_id
    expected_dir_name = custom_dir_name or task.constants.dataset_id
    filename = "test_filename.ext"
    path = Path(f"a/b/c/d/{filename}")
    assert task.format_object_key(path) == str(
        Path(expected_root_name, expected_dir_name, filename)
    )


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, None, id="Default trial dir name")]
)
def test_build_transfer_list(complete_trial_output_task, dummy_globus_transfer_item):
    """
    Given: A Task based on TransferTrialDataBase with a defined build_transfer_list
    When: Building the full transfer list
    Then: The expected transfer list is returned
    """
    task, *_ = complete_trial_output_task
    transfer_list = task.build_transfer_list()

    assert len(transfer_list) == 1
    assert transfer_list[0] == dummy_globus_transfer_item


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, "foo", id="Custom trial dir name")]
)
def test_build_debug_transfer_list(complete_trial_output_task, destination_bucket, custom_dir_name):
    """
    Given: A Task based on TransferTrialDataBase with a tagged DEBUG frame
    When: Building the debug transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct frames
    """
    task, proposal_id, debug_file_obj, *_ = complete_trial_output_task

    transfer_list = task.build_debug_frame_transfer_list()

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "debug.ext"
    expected_destination = Path(
        destination_bucket, proposal_id, custom_dir_name or task.constants.dataset_id, "debug.ext"
    )
    assert transfer_item.destination_path == expected_destination
    with transfer_item.source_path.open(mode="rb") as f:
        assert debug_file_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param("root", None, id="Default trial root name")]
)
def test_build_intermediate_transfer_list(
    complete_trial_output_task, destination_bucket, custom_root_name
):
    """
    Given: A Task based on TransferTrialDataBase with tagged INTERMEDIATE frames
    When: Building the intermediate transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct frames
    """
    task, proposal_id, _, intermediate_file_obj, _ = complete_trial_output_task

    transfer_list = task.build_intermediate_frame_transfer_list()
    expected_destination_name = "intermediate.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "intermediate.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert intermediate_file_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, None, id="Default trial dir name")]
)
def test_build_transfer_list_from_tag_list(complete_trial_output_task, destination_bucket):
    """
    Given: A Task based on TransferTrialDataBase with tagged frames
    When: Building a transfer list from lists of tags
    Then: The transfer list is built with correct source and destination paths
    """
    (
        task,
        _,
        debug_file_obj,
        intermediate_file_obj,
        intermediate_file_obj_2,
    ) = complete_trial_output_task

    tag_list_1 = [Tag.frame(), Tag.task("WHO_CARES")]
    tag_list_2 = [Tag.debug()]
    tag_list_3 = [Tag.intermediate()]
    tag_list = [tag_list_1, tag_list_2, tag_list_3]

    transfer_list = task.build_transfer_list_from_tag_lists(tag_list)
    assert len(transfer_list) == 3
    sorted_transfer_list = sorted(transfer_list, key=lambda x: x.source_path.name)

    # This whole structure is nasty. I'm sorry

    # Debug frame
    transfer_item = sorted_transfer_list[0]
    expected_destination_name = "debug.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )
    assert transfer_item.source_path == task.scratch.workflow_base_path / "debug.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert debug_file_obj == f.read()

    # Intermediate frame 1
    transfer_item = sorted_transfer_list[1]
    expected_destination_name = "intermediate.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )
    assert transfer_item.source_path == task.scratch.workflow_base_path / "intermediate.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert intermediate_file_obj == f.read()

    # Intermediate frame 2
    transfer_item = sorted_transfer_list[2]
    expected_destination_name = "something_else.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )
    assert transfer_item.source_path == task.scratch.workflow_base_path / "something_else.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert intermediate_file_obj_2 == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, None, id="Default trial dir name")]
)
def test_build_transfer_list_from_tag_list_single_list(
    complete_trial_output_task, destination_bucket
):
    """
    Given: A Task based on TransferTrialDataBase with tagged frames
    When: Building a transfer list from a single list of tags
    Then: The transfer list is built with correct source and destination paths
    """
    task, _, debug_file_obj, *_ = complete_trial_output_task

    tag_list = [Tag.debug()]

    transfer_list = task.build_transfer_list_from_tag_lists(tag_list)

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    expected_destination_name = "debug.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )
    assert transfer_item.source_path == task.scratch.workflow_base_path / "debug.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert debug_file_obj == f.read()
