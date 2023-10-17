from dataclasses import dataclass
from datetime import datetime
from unittest.mock import ANY
from unittest.mock import patch

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.tests.conftest import FakeGQLClient
from dkist_processing_pac.fitter.polcal_fitter import PolcalFitter
from dkist_processing_pac.input_data.dresser import Dresser

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.instrument_polarization import InstrumentPolarizationCalibration
from dkist_processing_visp.tests.conftest import generate_fits_frame
from dkist_processing_visp.tests.conftest import VispConstantsDb
from dkist_processing_visp.tests.conftest import VispHeadersValidPolcalFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters


class DummyPolcalFitter(PolcalFitter):
    def __init__(
        self,
        *,
        local_dresser: Dresser,
        global_dresser: Dresser,
        fit_mode: str,
        init_set: str,
        fit_TM: bool = False,
        threads: int = 1,
        super_name: str = "",
        _dont_fit: bool = False,
        **fit_kwargs,
    ):
        with patch("dkist_processing_pac.fitter.polcal_fitter.FitObjects"):
            super().__init__(
                local_dresser=local_dresser,
                global_dresser=global_dresser,
                fit_mode="use_M12",
                init_set="OCCal_VIS",
                _dont_fit=True,
            )

        self.num_modstates = local_dresser.nummod

    @property
    def demodulation_matrices(self) -> np.ndarray:
        return np.ones((1, 1, 4, self.num_modstates))


@dataclass
class VispInstPolCalTestingParameters(VispTestingParameters):
    visp_beam_border: int = 10


@pytest.fixture(scope="function")
def instrument_polarization_calibration_task(
    tmp_path,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
    init_visp_constants_db,
    mocker,
    background_on,
):
    num_beams = 2
    num_modstates = 2
    num_cs_steps = 2
    readout_exp_time = 0.02  # From VispHeadersValidPolcalFrames fixture
    intermediate_shape = (10, 10)
    dataset_shape = (num_cs_steps, 20, 10)
    array_shape = (1, 20, 10)
    spatial_size = array_shape[-1]
    spectral_size = array_shape[-2] // 2  # Divide by two for a single beam
    constants_db = VispConstantsDb(
        POLARIMETER_MODE="observe_polarimetric",
        NUM_MODSTATES=num_modstates,
        NUM_BEAMS=num_beams,
        NUM_CS_STEPS=num_cs_steps,
        POLCAL_READOUT_EXP_TIMES=(readout_exp_time,),
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with InstrumentPolarizationCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="instrument_polarization_calibration",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            assign_input_dataset_doc_to_task(
                task, VispInstPolCalTestingParameters(visp_background_on=background_on)
            )
            all_zeros = np.zeros(intermediate_shape)
            all_ones = np.ones(intermediate_shape)
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )

            mocker.patch(
                "dkist_processing_visp.tasks.instrument_polarization.PolcalFitter",
                new=DummyPolcalFitter,
            )

            # Don't test place-holder QA stuff for now
            quality_metric_mocker = mocker.patch(
                "dkist_processing_visp.tasks.instrument_polarization.InstrumentPolarizationCalibration.quality_store_polcal_results"
            )
            # Create fake geometric objects
            angle = np.array([0.0])
            offset = np.array([0.0, 0.0])
            spec_shift = np.zeros(intermediate_shape[0])
            for beam in range(1, num_beams + 1):
                task.intermediate_frame_helpers_write_arrays(
                    arrays=angle, beam=beam, task="GEOMETRIC_ANGLE"
                )
                task.intermediate_frame_helpers_write_arrays(
                    arrays=spec_shift, beam=beam, task="GEOMETRIC_SPEC_SHIFTS"
                )
                for modstate in range(1, num_modstates + 1):
                    task.intermediate_frame_helpers_write_arrays(
                        arrays=offset, beam=beam, modstate=modstate, task="GEOMETRIC_OFFSET"
                    )

            # Create fake dark and background intermediate arrays
            for beam in range(1, num_beams + 1):
                task.intermediate_frame_helpers_write_arrays(
                    all_zeros, beam=beam, task="DARK", readout_exp_time=readout_exp_time
                )

                if background_on:
                    # BackgroundLight object
                    task.intermediate_frame_helpers_write_arrays(
                        arrays=all_zeros, beam=beam, task="BACKGROUND"
                    )

            for beam in range(1, num_beams + 1):
                # Create fake lamp and solar gain arrays for this beam and modstate
                for modstate in range(1, num_modstates + 1):
                    gain_hdul = fits.HDUList([fits.PrimaryHDU(data=all_ones)])
                    task.fits_data_write(
                        hdu_list=gain_hdul,
                        tags=[
                            VispTag.intermediate(),
                            VispTag.frame(),
                            VispTag.task("SOLAR_GAIN"),
                            VispTag.beam(beam),
                            VispTag.modstate(modstate),
                            VispTag.readout_exp_time(readout_exp_time),
                        ],
                    )

            start_time = datetime.now()
            for modstate in range(1, num_modstates + 1):
                # Create polcal input frames for this modstate
                ds = VispHeadersValidPolcalFrames(
                    dataset_shape=dataset_shape,
                    array_shape=array_shape,
                    time_delta=10,
                    num_modstates=num_modstates,
                    modstate=modstate,
                    start_time=start_time,
                )
                header_generator = (
                    spec122_validator.validate_and_translate_to_214_l0(
                        d.header(), return_type=fits.HDUList
                    )[0].header
                    for d in ds
                )
                # cs_step does not map to a single keyword, so not needed in the fake headers
                for cs_step in range(num_cs_steps):
                    hdul = generate_fits_frame(header_generator=header_generator, shape=array_shape)
                    task.fits_data_write(
                        hdu_list=hdul,
                        tags=[
                            VispTag.task("POLCAL"),
                            VispTag.modstate(modstate),
                            VispTag.cs_step(cs_step),
                            VispTag.input(),
                            VispTag.frame(),
                            VispTag.readout_exp_time(readout_exp_time),
                        ],
                    )

            yield task, quality_metric_mocker, spectral_size, spatial_size, num_modstates
        except:
            raise
        finally:
            task._purge()


@pytest.fixture(scope="function")
def instrument_polarization_calibration_task_with_no_data(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db
):
    init_visp_constants_db(recipe_run_id, VispConstantsDb())
    with InstrumentPolarizationCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="instrument_polarization_calibration",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            assign_input_dataset_doc_to_task(task, VispInstPolCalTestingParameters())
            yield task
        except:
            raise
        finally:
            task._purge()


@pytest.fixture()
def full_beam_shape() -> tuple[int, int]:
    return (100, 256)


@pytest.fixture()
def single_demodulation_matrix() -> np.ndarray:
    return np.arange(40).reshape(1, 1, 4, 10)


@pytest.fixture()
def multiple_demodulation_matrices() -> np.ndarray:
    return np.arange(2 * 3 * 4 * 10).reshape(2, 3, 4, 10)


@pytest.fixture()
def full_spatial_beam_shape() -> tuple[int, int]:
    return (1, 256)


@pytest.fixture()
def spatially_binned_demodulation_matrices(full_spatial_beam_shape) -> np.ndarray:
    num_bins = full_spatial_beam_shape[1] // 4
    return np.arange(1 * num_bins * 4 * 10).reshape(1, num_bins, 4, 10)


@pytest.mark.parametrize(
    "background_on",
    [pytest.param(True, id="Background on"), pytest.param(False, id="Background off")],
)
def test_instrument_polarization_calibration_task(instrument_polarization_calibration_task, mocker):
    """
    Given: An InstrumentPolarizationCalibration task
    When: Calling the task instance
    Then: A demodulation matrix for each beam is produced and the correct call to the quality storage system was made
    """

    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )

    # When
    (
        task,
        quality_mocker,
        spectral_size,
        spatial_size,
        num_mod,
    ) = instrument_polarization_calibration_task
    task()

    # Then
    for beam in [1, 2]:
        tags = [
            VispTag.intermediate(),
            VispTag.task("DEMOD_MATRICES"),
            VispTag.beam(beam),
        ]
        file_list = list(task.read(tags=tags))
        assert len(file_list) == 1
        hdul = fits.open(file_list[0])
        assert len(hdul) == 1
        data = hdul[0].data
        assert data.shape == (spectral_size, spatial_size, 4, num_mod)

        quality_mocker.assert_any_call(
            polcal_fitter=ANY,
            label=f"Beam {beam}",
            bins_1=1,
            bins_2=task.parameters.polcal_num_spatial_bins,
            bin_1_type="spectral",
            bin_2_type="spatial",
            skip_recording_constant_pars=beam == 2,
        )


def test_smooth_demod_matrices(
    instrument_polarization_calibration_task_with_no_data,
    spatially_binned_demodulation_matrices,
    full_spatial_beam_shape,
):
    """
    Given: An InstrumentPolarizationCalibration task and a set of demod matrices binned in the spatial dimension
    When: Smooth the demodulation matrices
    Then: Smoothing doesn't fail and the result fully samples the full spatial dimension
    """
    instrument_polarization_calibration_task_with_no_data.single_beam_shape = (
        full_spatial_beam_shape
    )
    result = instrument_polarization_calibration_task_with_no_data.smooth_demod_matrices(
        spatially_binned_demodulation_matrices
    )
    assert result.shape == full_spatial_beam_shape + (4, 10)


def test_reshape_demod_matrices(
    instrument_polarization_calibration_task_with_no_data,
    multiple_demodulation_matrices,
    full_beam_shape,
):
    """
    Given: An InstrumentPolarizationCalibration task and a set of demodulation matrices sampled over the full FOV
    When: Up-sampling the demodulation matrices
    Then: The final set of demodulation matrices has the correct, full-FOV shape
    """
    instrument_polarization_calibration_task_with_no_data.single_beam_shape = full_beam_shape
    result = instrument_polarization_calibration_task_with_no_data.reshape_demod_matrices(
        multiple_demodulation_matrices
    )
    assert result.shape == full_beam_shape + (4, 10)


def test_reshape_single_demod_matrix(
    instrument_polarization_calibration_task_with_no_data,
    single_demodulation_matrix,
    full_beam_shape,
):
    """
    Given: An InstrumentPolarizationCalibration task and a single demodulation matrix for the whole FOV
    When: Up-sampling the demodulation matrices
    Then: The final set of demodulation matrices still only has a single matrix
    """
    instrument_polarization_calibration_task_with_no_data.single_beam_shape = full_beam_shape
    result = instrument_polarization_calibration_task_with_no_data.reshape_demod_matrices(
        single_demodulation_matrix
    )
    assert result.shape == (4, 10)
