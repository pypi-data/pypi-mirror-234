from datetime import datetime
from datetime import timedelta
from itertools import chain

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator.translator import translate_spec122_to_spec214_l0
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_visp.tasks.parse import ParseL0VispInputData
from dkist_processing_visp.tests.conftest import VispHeadersValidDarkFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidLampGainFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidObserveFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidPolcalFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidSolarGainFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters


@pytest.fixture(scope="function")
def parse_inputs_valid_task(tmp_path, recipe_run_id, assign_input_dataset_doc_to_task):
    num_maps = 1
    num_modstates = 2
    num_steps = 3
    with ParseL0VispInputData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            ds1 = VispHeadersValidDarkFrames(
                dataset_shape=(2, 2, 2), array_shape=(1, 2, 2), time_delta=10
            )
            ds2 = VispHeadersValidLampGainFrames(
                dataset_shape=(2, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=10,
                num_modstates=2,
                modstate=1,
            )
            ds3 = VispHeadersValidSolarGainFrames(
                dataset_shape=(2, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=10,
                num_modstates=2,
                modstate=1,
            )
            ds4 = VispHeadersValidPolcalFrames(
                dataset_shape=(2, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=30,
                num_modstates=2,
                modstate=1,
            )
            ds = chain(ds1, ds2, ds3, ds4)
            for d in ds:
                header = d.header()
                translated_header = translate_spec122_to_spec214_l0(header)
                hdu = fits.PrimaryHDU(
                    data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                )
                hdul = fits.HDUList([hdu])
                task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])

            start_time = datetime.now()
            time_delta = timedelta(seconds=10)
            i = 0
            for map_scan in range(1, num_maps + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(num_steps):
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_raster_steps=num_steps,
                            raster_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            polarimeter_mode="observe_polarimetric",
                            start_time=start_time + i * time_delta,
                        )
                        header = next(ds).header()
                        header["CAM__004"] = [0.02, 0.03][m % 2]
                        header["CAM__005"] = [0.04, 0.06][m % 2]
                        translated_header = translate_spec122_to_spec214_l0(header)
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
                        i += 1
            yield task
        except:
            raise
        finally:
            task._purge()


@pytest.fixture
def parse_task_with_multi_num_raster_steps(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task
):
    num_steps = 4
    num_map_scans = 2
    num_modstates = 2
    with ParseL0VispInputData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for map_scan in range(1, num_map_scans + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(num_steps):
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_raster_steps=num_steps,
                            raster_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            polarimeter_mode="observe_polarimetric",
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        translated_header["VSPNSTP"] = s % 3
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
            yield task
        except:
            raise
        finally:
            task._purge()


@pytest.fixture
def parse_task_with_incomplete_final_map(tmp_path, recipe_run_id, assign_input_dataset_doc_to_task):
    num_steps = 4
    num_map_scans = 3
    num_modstates = 2
    with ParseL0VispInputData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for map_scan in range(1, num_map_scans):
                for m in range(1, num_modstates + 1):
                    for s in range(num_steps):
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_raster_steps=num_steps,
                            raster_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            polarimeter_mode="observe_polarimetric",
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
            # Now do the incomplete map
            for map_scan in range(num_map_scans, num_map_scans + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(num_steps - 1):  # One step is missing in the last map
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_raster_steps=num_steps,
                            raster_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            polarimeter_mode="observe_polarimetric",
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
            yield task, num_steps, num_map_scans
        except:
            raise
        finally:
            task._purge()


@pytest.fixture
def parse_task_with_incomplete_raster_scan(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task
):
    num_steps = 4
    num_maps = 1
    num_modstates = 2
    with ParseL0VispInputData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for map_scan in range(1, num_maps + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(num_steps):
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_raster_steps=num_steps,
                            raster_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            polarimeter_mode="observe_polarimetric",
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        translated_header["VSPNSTP"] = num_steps + 10
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
            yield task, num_steps, num_maps
        except:
            raise
        finally:
            task._purge()


@pytest.fixture
def parse_task_with_intensity_observes_and_polarmetric_cals(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task
):
    num_maps = 1
    num_observe_modstates = 1
    num_calibration_modstates = 2
    num_raster_steps = 3
    with ParseL0VispInputData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for map_scan in range(num_maps + 1):
                for raster_step in range(num_raster_steps + 1):
                    for observe_modstate in range(1, num_observe_modstates + 1):
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_modstates=num_observe_modstates,
                            modstate=observe_modstate,
                            num_raster_steps=num_raster_steps,
                            raster_step=raster_step,
                            polarimeter_mode="observe_intensity",
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
                    for calibration_modstate in range(1, num_calibration_modstates + 1):
                        ds = VispHeadersValidLampGainFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_modstates=num_calibration_modstates,
                            modstate=calibration_modstate,
                            polarimeter_mode="dark_polarimetric",
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
            yield task
        except:
            raise
        finally:
            task._purge()


def test_parse_visp_input_data(parse_inputs_valid_task, mocker):
    """
    Given: A ParseVispInputData task
    When: Calling the task instance
    Then: All tagged files exist and individual task tags are applied
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    parse_inputs_valid_task()
    # Then
    translated_input_files = parse_inputs_valid_task.read(tags=[Tag.input(), Tag.frame()])
    for filepath in translated_input_files:
        assert filepath.exists()

    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("DARK")]))
    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("LAMP_GAIN")]))
    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("SOLAR_GAIN")]))
    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("POLCAL")]))
    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("OBSERVE")]))


def test_parse_visp_input_data_constants(parse_inputs_valid_task, mocker):
    """
    Given: A ParseVispInputData task
    When: Calling the task instance
    Then: Constants are in the constants object as expected
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    parse_inputs_valid_task()
    # Then
    assert parse_inputs_valid_task.constants._db_dict["OBS_IP_START_TIME"] == "2022-11-28T13:55:00"
    assert parse_inputs_valid_task.constants._db_dict["NUM_MODSTATES"] == 2
    assert parse_inputs_valid_task.constants._db_dict["NUM_MAP_SCANS"] == 1
    assert parse_inputs_valid_task.constants._db_dict["NUM_RASTER_STEPS"] == 3
    assert parse_inputs_valid_task.constants._db_dict["WAVELENGTH"] == 656.28
    assert parse_inputs_valid_task.constants._db_dict["DARK_EXPOSURE_TIMES"] == [1.0]
    assert parse_inputs_valid_task.constants._db_dict["LAMP_EXPOSURE_TIMES"] == [10.0]
    assert parse_inputs_valid_task.constants._db_dict["SOLAR_EXPOSURE_TIMES"] == [20.0]
    assert parse_inputs_valid_task.constants._db_dict["POLCAL_EXPOSURE_TIMES"] == [0.01]
    assert parse_inputs_valid_task.constants._db_dict["OBSERVE_EXPOSURE_TIMES"] == [0.02, 0.03]
    assert parse_inputs_valid_task.constants._db_dict["DARK_READOUT_EXP_TIMES"] == [2.0]
    assert parse_inputs_valid_task.constants._db_dict["LAMP_READOUT_EXP_TIMES"] == [20.0]
    assert parse_inputs_valid_task.constants._db_dict["SOLAR_READOUT_EXP_TIMES"] == [40.0]
    assert parse_inputs_valid_task.constants._db_dict["POLCAL_READOUT_EXP_TIMES"] == [0.02]
    assert parse_inputs_valid_task.constants._db_dict["OBSERVE_READOUT_EXP_TIMES"] == [0.04, 0.06]


def test_parse_visp_values(parse_inputs_valid_task, mocker):
    """
    :Given: A valid parse input task
    :When: Calling the task instance
    :Then: Values are correctly loaded into the constants mutable mapping
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    parse_inputs_valid_task()
    assert parse_inputs_valid_task.constants.instrument == "VISP"
    assert parse_inputs_valid_task.constants.average_cadence == 10
    assert parse_inputs_valid_task.constants.maximum_cadence == 10
    assert parse_inputs_valid_task.constants.minimum_cadence == 10
    assert parse_inputs_valid_task.constants.variance_cadence == 0


def test_multiple_num_raster_steps_raises_error(parse_task_with_multi_num_raster_steps, mocker):
    """
    :Given: A prase task with data that have inconsistent VSPNSTP values
    :When: Calling the parse task
    :Then: The correct error is raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    with pytest.raises(ValueError, match="Multiple NUM_RASTER_STEPS values found"):
        parse_task_with_multi_num_raster_steps()


def test_incomplete_single_map(parse_task_with_incomplete_raster_scan, mocker):
    """
    :Given: A parse task with data that has an incomplete raster scan
    :When: Calling the parse task
    :Then: The correct number of raster steps are found
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, num_steps, num_map_scans = parse_task_with_incomplete_raster_scan
    task()
    assert task.constants._db_dict["NUM_RASTER_STEPS"] == num_steps
    assert task.constants._db_dict["NUM_MAP_SCANS"] == num_map_scans


def test_incomplete_final_map(parse_task_with_incomplete_final_map, mocker):
    """
    :Given: A parse task with data that has complete raster scans along with an incomplete raster scan
    :When: Calling the parse task
    :Then: The correct number of raster steps and maps are found
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, num_steps, num_map_scans = parse_task_with_incomplete_final_map
    task()
    assert task.constants._db_dict["NUM_RASTER_STEPS"] == num_steps
    assert task.constants._db_dict["NUM_MAP_SCANS"] == num_map_scans - 1


def test_intensity_observes_and_polarmetric_cals(
    parse_task_with_intensity_observes_and_polarmetric_cals, mocker
):
    """
    :Given: Data where the observe frames are in intensity mode and the calibration frames are in polarimetric mode
    :When: Parsing the data
    :Then: All modulator state keys generated for all frames are in the first modulator state
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = parse_task_with_intensity_observes_and_polarmetric_cals
    task()
    assert task.constants._db_dict["NUM_MODSTATES"] == 1
    assert task.constants._db_dict["POLARIMETER_MODE"] == "observe_intensity"
    files = list(task.read(tags=[Tag.input(), Tag.frame()]))
    for file in files:
        assert "MODSTATE_1" in task.scratch.tags(file)
