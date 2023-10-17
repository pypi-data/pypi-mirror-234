import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem

from dkist_processing_visp.tasks.l1_output_data import VispSubmitQuality
from dkist_processing_visp.tests.conftest import VispConstantsDb


@pytest.fixture
def plot_data():
    datetimes_a = ["2021-01-01T01:01:01", "2021-01-01T02:01:01"]
    values_a = [3, 4]
    datetimes_b = ["2020-01-01T01:01:01", "2020-01-01T02:01:01"]
    values_b = [1, 2]
    return datetimes_a, values_a, datetimes_b, values_b


@pytest.fixture
def quality_task(tmp_path, recipe_run_id, init_visp_constants_db):
    constants_db = VispConstantsDb(NUM_MODSTATES=2, POLARIMETER_MODE="observe_polarimetric")
    init_visp_constants_db(recipe_run_id, constants_db)
    with VispSubmitQuality(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.scratch.workflow_base_path = tmp_path / str(recipe_run_id)
        yield task
        task._purge()
