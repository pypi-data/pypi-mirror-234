import json

import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.str import str_encoder
from dkist_processing_common.models.graphql import RecipeRunResponse

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.trial_output_data import TransferVispTrialData


@pytest.fixture
def recipe_run_configuration(debug_switch, intermediate_switch, output_switch, tag_lists):
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
                                "trial_transfer_debug_frames": debug_switch,
                                "trial_transfer_intermediate_frames": intermediate_switch,
                                "trial_transfer_output_frames": output_switch,
                                "trial_transfer_tag_lists": tag_lists,
                            }
                        ),
                    ),
                ]

        @staticmethod
        def execute_gql_mutation(**kwargs):
            ...

    return GQLClientWithConfiguration


intermediate_task_names = [
    "DARK",
    "BACKGROUND",
    "GEOMETRIC_ANGLE",
    "GEOMETRIC_OFFSET",
    "GEOMETRIC_SPEC_SHIFTS",
    "SOLAR_GAIN",
    "DEMOD_MATRICES",
]

tag_lists = [[VispTag.movie()], ["FOO", "BAR"]]


def write_debug_frames_to_task(task: TransferVispTrialData) -> int:
    num_debug = 3
    for _ in range(num_debug):
        task.write(data="123", encoder=str_encoder, tags=[VispTag.frame(), VispTag.debug()])

    return num_debug


def write_intermediate_frames_to_task(task: TransferVispTrialData) -> int:
    for task_name in intermediate_task_names:
        task.write(
            data=task_name,
            encoder=str_encoder,
            tags=[VispTag.frame(), VispTag.intermediate(), VispTag.task(task_name)],
        )

    return len(intermediate_task_names)


def write_output_frames_to_task(task: TransferVispTrialData) -> int:
    num_output = 2
    for i in range(num_output):
        task.write(
            data=f"output_{i}", encoder=str_encoder, tags=[VispTag.frame(), VispTag.output()]
        )

    return num_output


def write_specific_tags_to_task(task: TransferVispTrialData) -> int:
    for tags in tag_lists:
        task.write(data="foo", encoder=str_encoder, tags=tags)

    return len(tag_lists)


def write_unused_frame_to_task(task: TransferVispTrialData) -> int:
    task.write(data="bad", encoder=str_encoder, tags=["FOO"])
    return 1


@pytest.fixture
def transfer_task_with_files(recipe_run_id, recipe_run_configuration, tmp_path, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=recipe_run_configuration,
    )
    proposal_id = "test_proposal_id"
    with TransferVispTrialData(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})
        try:
            num_debug = write_debug_frames_to_task(task)
            num_intermediate = write_intermediate_frames_to_task(task)
            num_output = write_output_frames_to_task(task)
            num_specific = write_specific_tags_to_task(task)
            write_unused_frame_to_task(task)
            yield task, num_debug, num_intermediate, num_output, num_specific

        finally:
            task._purge()


# These test cases come from PICT
@pytest.mark.parametrize(
    "debug_switch, intermediate_switch, output_switch, tag_lists",
    [
        pytest.param(False, False, False, [], id="None"),
        pytest.param(True, True, False, tag_lists, id="Debug, Intermediate, Specific"),
        pytest.param(True, True, True, [], id="Debug, Intermediate, Output"),
        pytest.param(False, True, True, tag_lists, id="Intermediate, Output, Specific"),
        pytest.param(True, False, True, tag_lists, id="Debug, Output, Specific"),
    ],
)
def test_build_transfer_list(
    transfer_task_with_files, debug_switch, intermediate_switch, output_switch, tag_lists
):
    """
    Given: A TransferVispTrialData task with a recipe run configuration (RRC) and a collection of frames
    When: Building the transfer list
    Then: Only the files requested by the RRC switches are collected for transfer
    """
    task, num_debug, num_intermediate, num_output, num_specific = transfer_task_with_files

    expected_num = 0
    if debug_switch:
        expected_num += num_debug
    if intermediate_switch:
        expected_num += num_intermediate
    if output_switch:
        expected_num += num_output
    if tag_lists:
        expected_num += num_specific

    transfer_list = task.build_transfer_list()
    assert len(transfer_list) == expected_num
