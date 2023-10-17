import json
from dataclasses import dataclass

import numpy as np
import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tests.conftest import FakeGQLClient
from dkist_processing_math import transform

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.geometric import GeometricCalibration
from dkist_processing_visp.tests.conftest import generate_214_l0_fits_frame
from dkist_processing_visp.tests.conftest import VispConstantsDb
from dkist_processing_visp.tests.conftest import VispHeadersValidLampGainFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidSolarGainFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters


@dataclass
class VispGeoTestingParameters30(VispTestingParameters):
    visp_beam_border: int = 30


@pytest.fixture(scope="function")
def geometric_calibration_task_that_completes(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db
):
    # This fixture makes data that look enough like real data that all of the feature detection stuff at least runs
    # through (mostly this is an issue for the angle calculation). It would be great to contrive data that
    # produce a geometric calibration with real numbers that can be checked, but for now we'll rely on the grogu
    # tests for that. In other words, this fixture just tests if the machinery of the task completes and some object
    # (ANY object) is written correctly.
    number_of_modstates = 3
    number_of_beams = 2
    solar_exp_time = 40.0  # From VispHeadersValidSolarGainFrames fixture
    lamp_exp_time = 20.0  # From VispHeadersValidLampGainFrames fixture
    intermediate_shape = (30, 100)
    array_shape = (1, 60, 100)
    dataset_shape = array_shape
    constants_db = VispConstantsDb(
        NUM_MODSTATES=number_of_modstates,
        SOLAR_READOUT_EXP_TIMES=(solar_exp_time,),
        LAMP_READOUT_EXP_TIMES=(lamp_exp_time,),
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with GeometricCalibration(
        recipe_run_id=recipe_run_id, workflow_name="geometric_calibration", workflow_version="VX.Y"
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispGeoTestingParameters30())
            task.angles = np.array([0.01, -0.01])
            task.offsets = np.zeros((number_of_beams, number_of_modstates, 2))
            task.shifts = np.zeros(intermediate_shape[0])
            for beam in range(1, number_of_beams + 1):

                dark_cal = np.ones(intermediate_shape) * 3.0
                task.intermediate_frame_helpers_write_arrays(
                    arrays=dark_cal, beam=beam, task="DARK", readout_exp_time=solar_exp_time
                )

                task.intermediate_frame_helpers_write_arrays(
                    arrays=dark_cal, beam=beam, task="DARK", readout_exp_time=lamp_exp_time
                )

                for modstate in range(1, number_of_modstates + 1):
                    solar_ds = VispHeadersValidSolarGainFrames(
                        dataset_shape=dataset_shape,
                        array_shape=array_shape,
                        time_delta=10,
                        num_modstates=number_of_modstates,
                        modstate=modstate,
                    )
                    solar_header = solar_ds.header()
                    solar_num_raw_per_fpa = solar_header["CAM__014"]
                    true_solar = 10 * (np.ones(array_shape[1:]) + modstate + beam)
                    translated_solar = next(
                        transform.translate_arrays(
                            arrays=true_solar, translation=task.offsets[beam - 1][modstate - 1]
                        )
                    )
                    translated_solar[translated_solar == 0] = 10 * (modstate + beam + 1)

                    # Hairlines
                    translated_solar[:, 30] = 5.0
                    translated_solar[:, 70] = 5.0
                    distorted_solar = next(
                        transform.rotate_arrays_about_point(
                            arrays=translated_solar, angle=task.angles[beam - 1]
                        )
                    )
                    raw_dark = np.concatenate((dark_cal, dark_cal))
                    raw_solar = (distorted_solar + raw_dark) * solar_num_raw_per_fpa
                    solar_hdul = generate_214_l0_fits_frame(
                        data=raw_solar, s122_header=solar_header
                    )
                    task.fits_data_write(
                        hdu_list=solar_hdul,
                        tags=[
                            VispTag.input(),
                            VispTag.task("SOLAR_GAIN"),
                            VispTag.modstate(modstate),
                            VispTag.frame(),
                            VispTag.beam(beam),
                            VispTag.readout_exp_time(solar_exp_time),
                        ],
                    )

                    lamp_ds = VispHeadersValidLampGainFrames(
                        dataset_shape=dataset_shape,
                        array_shape=array_shape,
                        time_delta=10,
                        num_modstates=number_of_modstates,
                        modstate=modstate,
                    )
                    lamp_header = lamp_ds.header()
                    lamp_num_raw_per_fpa = lamp_header["CAM__014"]
                    true_lamp = 10 * (np.ones(array_shape[1:]) + modstate + beam)
                    translated_lamp = next(
                        transform.translate_arrays(
                            arrays=true_lamp, translation=task.offsets[beam - 1][modstate - 1]
                        )
                    )
                    translated_lamp[translated_lamp == 0] = 10 * (modstate + beam + 1)

                    # Hairlines
                    translated_lamp[:, 30] = 5.0
                    translated_lamp[:, 70] = 5.0
                    # Chop out part of the second hairline so the fitter has to skip over these pixels
                    translated_lamp[5:9, 70] = 10 * (modstate + beam + 1)
                    distorted_lamp = next(
                        transform.rotate_arrays_about_point(
                            arrays=translated_lamp, angle=task.angles[beam - 1]
                        )
                    )
                    raw_lamp = (distorted_lamp + raw_dark) * lamp_num_raw_per_fpa
                    lamp_hdul = generate_214_l0_fits_frame(data=raw_lamp, s122_header=lamp_header)
                    task.fits_data_write(
                        hdu_list=lamp_hdul,
                        tags=[
                            VispTag.input(),
                            VispTag.task("LAMP_GAIN"),
                            VispTag.modstate(modstate),
                            VispTag.frame(),
                            VispTag.beam(beam),
                            VispTag.readout_exp_time(lamp_exp_time),
                        ],
                    )

            yield task
        except:
            raise
        finally:
            task._purge()


@dataclass
class VispGeoTestingParameters10(VispTestingParameters):
    visp_beam_border: int = 10


@pytest.fixture(scope="function")
def geometric_calibration_task_with_simple_raw_data(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db
):
    number_of_modstates = 3
    number_of_beams = 2
    solar_exp_time = 40.0  # From VispHeadersValidSolarGainFrames fixture
    lamp_exp_time = 20.0  # From VispHeadersValidLampGainFrames fixture
    data_shape_int = (10, 10)
    data_shape_raw = (20, 10)
    constants_db = VispConstantsDb(
        NUM_MODSTATES=number_of_modstates,
        SOLAR_READOUT_EXP_TIMES=(solar_exp_time,),
        LAMP_READOUT_EXP_TIMES=(lamp_exp_time,),
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with GeometricCalibration(
        recipe_run_id=recipe_run_id, workflow_name="geometric_calibration", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        assign_input_dataset_doc_to_task(task, VispGeoTestingParameters10())

        # Create the intermediate frames needed
        for beam in range(1, number_of_beams + 1):

            dark_cal = np.ones(data_shape_int) * 3.0
            task.intermediate_frame_helpers_write_arrays(
                arrays=dark_cal, beam=beam, task="DARK", readout_exp_time=solar_exp_time
            )

            task.intermediate_frame_helpers_write_arrays(
                arrays=dark_cal, beam=beam, task="DARK", readout_exp_time=lamp_exp_time
            )

            # Let's write a dark with the wrong exposure time, just to make sure it doesn't get used
            task.intermediate_frame_helpers_write_arrays(
                arrays=np.ones(data_shape_int) * 1e6,
                beam=beam,
                task="DARK",
                readout_exp_time=solar_exp_time**2,
            )

        # Create the raw data, which is based on two beams per frame
        beam1 = 1
        beam2 = 2
        dark_cal_two_beams = np.concatenate((dark_cal, dark_cal))
        for modstate in range(1, number_of_modstates + 1):

            # Solar
            solar_ds = VispHeadersValidSolarGainFrames(
                dataset_shape=(1,) + data_shape_raw,
                array_shape=(1,) + data_shape_raw,
                time_delta=10,
                num_modstates=number_of_modstates,
                modstate=modstate,
            )
            solar_header = solar_ds.header()
            solar_num_raw_per_fpa = solar_header["CAM__014"]
            true_solar = np.ones(data_shape_raw) + modstate
            # Now add the beam number to each beam in the array
            true_solar[: task.parameters.beam_border, :] += beam1
            true_solar[task.parameters.beam_border :, :] += beam2
            raw_solar = (true_solar + dark_cal_two_beams) * solar_num_raw_per_fpa
            solar_hdul = generate_214_l0_fits_frame(data=raw_solar, s122_header=solar_header)
            task.fits_data_write(
                hdu_list=solar_hdul,
                tags=[
                    VispTag.input(),
                    VispTag.task("SOLAR_GAIN"),
                    VispTag.modstate(modstate),
                    VispTag.frame(),
                    VispTag.readout_exp_time(solar_exp_time),
                ],
            )

            # Lamp
            lamp_ds = VispHeadersValidLampGainFrames(
                dataset_shape=(1,) + data_shape_raw,
                array_shape=(1,) + data_shape_raw,
                time_delta=10,
                num_modstates=number_of_modstates,
                modstate=modstate,
            )
            lamp_header = lamp_ds.header()
            lamp_num_raw_per_fpa = lamp_header["CAM__014"]
            true_lamp = np.ones(data_shape_raw) + modstate
            # Now add the beam number to each beam in the array
            true_lamp[: task.parameters.beam_border, :] += beam1
            true_lamp[task.parameters.beam_border :, :] += beam2
            raw_lamp = (true_lamp + dark_cal_two_beams) * lamp_num_raw_per_fpa
            lamp_hdul = generate_214_l0_fits_frame(data=raw_lamp, s122_header=lamp_header)
            task.fits_data_write(
                hdu_list=lamp_hdul,
                tags=[
                    VispTag.input(),
                    VispTag.task("LAMP_GAIN"),
                    VispTag.modstate(modstate),
                    VispTag.frame(),
                    VispTag.readout_exp_time(lamp_exp_time),
                ],
            )

        yield task
        task._purge()


def test_geometric_task(geometric_calibration_task_that_completes, mocker):
    """
    Given: A set of raw solar gain images and necessary intermediate calibrations
    When: Running the geometric task
    Then: The damn thing runs and makes outputs that at least are the right type
    """
    # See the note in the fixture above: this test does NOT test for accuracy of the calibration
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = geometric_calibration_task_that_completes
    task()
    for beam in range(1, task.constants.num_beams + 1):
        assert type(task.intermediate_frame_helpers_load_angle(beam=beam)) is np.float64
        assert task.intermediate_frame_helpers_load_spec_shift(beam=beam).shape == (100,)
        for modstate in range(1, task.constants.num_modstates + 1):
            assert task.intermediate_frame_helpers_load_state_offset(
                beam=beam, modstate=modstate
            ).shape == (2,)

    quality_files = task.read(tags=[Tag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[VispTag.input(), VispTag.frame(), VispTag.task("SOLAR_GAIN")]
            )


def test_basic_corrections(geometric_calibration_task_with_simple_raw_data):
    """
    Given: A set of raw solar gain images and necessary intermediate calibrations
    When: Doing basic dark and lamp gain corrections
    Then: The corrections are applied correctly
    """
    task = geometric_calibration_task_with_simple_raw_data
    task.do_basic_corrections()
    for beam in range(1, task.constants.num_beams + 1):
        for modstate in range(1, task.constants.num_modstates + 1):
            expected = np.ones((10, 10)) + modstate + beam
            solar_array = task.basic_corrected_solar_data(beam=beam, modstate=modstate)
            lamp_array = task.basic_corrected_lamp_data(beam=beam, modstate=modstate)
            np.testing.assert_equal(expected, solar_array)
            np.testing.assert_equal(expected, lamp_array)
