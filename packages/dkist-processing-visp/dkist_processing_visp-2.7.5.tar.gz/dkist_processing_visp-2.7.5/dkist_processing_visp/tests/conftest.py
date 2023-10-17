import json
import uuid
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import is_dataclass
from random import choice
from random import randint
from typing import Iterable

import numpy as np
import pytest
from astropy.io import fits
from astropy.wcs import WCS
from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_header_validator import spec122_validator
from dkist_header_validator.translator import sanitize_to_spec214_level1
from dkist_header_validator.translator import translate_spec122_to_spec214_l0

from dkist_processing_visp.models.constants import VispConstants
from dkist_processing_visp.models.parameters import VispParameters
from dkist_processing_visp.models.tags import VispTag


class VispHeaders(Spec122Dataset):
    def __init__(
        self,
        dataset_shape: tuple[int, ...],
        array_shape: tuple[int, ...],
        time_delta: 10,
        instrument: str = "visp",
        polarimeter_mode: str = "observe_polarimetric",
        **kwargs,
    ):
        super().__init__(
            dataset_shape=dataset_shape,
            array_shape=array_shape,
            time_delta=time_delta,
            instrument=instrument,
            **kwargs,
        )
        self.add_constant_key("WAVELNTH", 656.30)
        self.add_constant_key("VISP_010", 2)
        self.add_constant_key("ID___013", "TEST_PROPOSAL_ID")
        self.add_constant_key("VISP_006", polarimeter_mode)
        self.add_constant_key("PAC__005", "0")
        self.add_constant_key("PAC__007", "10")
        self.add_constant_key("FILE_ID", uuid.uuid4().hex)

    @key_function("VISP_011")
    def date(self, key: str):
        return choice([1, 2])

    @property
    def fits_wcs(self):
        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.array_shape[2] / 2, self.array_shape[1] / 2, 1
        w.wcs.crval = 0, 656.30, 0
        w.wcs.cdelt = 1, 0.2, 1
        w.wcs.cunit = "arcsec", "nm", "arcsec"
        w.wcs.ctype = "HPLT-TAN", "AWAV", "HPLN-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w


class VispHeadersValidDarkFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: tuple[int, ...],
        array_shape: tuple[int, ...],
        time_delta: float,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.add_constant_key("DKIST004", "dark")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("DKIST011", "2022-11-28T13:44:00")
        self.add_constant_key("DKIST012", "2022-11-28T13:45:00")
        self.add_constant_key("VISP_019", 1)
        self.add_constant_key("VISP_020", 1)
        self.add_constant_key("ID___004")
        self.add_constant_key(
            "WAVELNTH", 0.0
        )  # Intentionally bad to make sure it doesn't get parsed
        self.add_constant_key("CAM__004", 1.0)
        self.add_constant_key("CAM__005", 2.0)
        self.add_constant_key("CAM__014", 10)


class VispHeadersValidLampGainFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: tuple[int, ...],
        array_shape: tuple[int, ...],
        time_delta: float,
        num_modstates: int,
        modstate: int,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.add_constant_key("DKIST004", "gain")
        self.add_constant_key("PAC__002", "lamp")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("DKIST011", "2022-11-28T13:46:00")
        self.add_constant_key("DKIST012", "2022-11-28T13:47:00")
        self.add_constant_key("VISP_019", 1)
        self.add_constant_key("VISP_020", 1)
        self.add_constant_key("PAC__003", "on")
        self.add_constant_key("ID___004")
        self.add_constant_key("VISP_010", num_modstates)
        self.add_constant_key("VISP_011", modstate)
        self.add_constant_key("CAM__004", 10.0)
        self.add_constant_key("CAM__005", 20.0)
        self.add_constant_key("CAM__014", 10)


class VispHeadersValidSolarGainFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: tuple[int, ...],
        array_shape: tuple[int, ...],
        time_delta: float,
        num_modstates: int,
        modstate: int,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.add_constant_key("DKIST004", "gain")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("DKIST011", "2022-11-28T13:48:00")
        self.add_constant_key("DKIST012", "2022-11-28T13:49:00")
        self.add_constant_key("VISP_019", 1)
        self.add_constant_key("VISP_020", 1)
        self.add_constant_key("PAC__002", "clear")
        self.add_constant_key("TELSCAN", "Raster")
        self.add_constant_key("ID___004")
        self.add_constant_key("VISP_010", num_modstates)
        self.add_constant_key("VISP_011", modstate)
        self.add_constant_key("CAM__004", 20.0)
        self.add_constant_key("CAM__005", 40.0)
        self.add_constant_key("CAM__014", 10)


class VispHeadersValidPolcalFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: tuple[int, ...],
        array_shape: tuple[int, ...],
        time_delta: float,
        num_modstates: int,
        modstate: int,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.add_constant_key("DKIST004", "polcal")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("DKIST011", "2022-11-28T13:50:00")
        self.add_constant_key("DKIST012", "2022-11-28T13:51:00")
        self.add_constant_key("VISP_019", 1)
        self.add_constant_key("VISP_020", 1)
        self.add_constant_key("TELSCAN", "Raster")
        self.add_constant_key("ID___004")
        self.add_constant_key("PAC__004", "Sapphire Polarizer")
        self.add_constant_key("PAC__005", "60.")
        self.add_constant_key("PAC__006", "clear")
        self.add_constant_key("PAC__007", "0.0")
        self.add_constant_key("PAC__008", "FieldStop (5arcmin)")
        self.add_constant_key("VISP_010", num_modstates)
        self.add_constant_key("VISP_011", modstate)
        self.add_constant_key("CAM__004", 0.01)
        self.add_constant_key("CAM__005", 0.02)
        self.add_constant_key("CAM__014", 10)


class VispHeadersValidObserveFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: tuple[int, ...],
        array_shape: tuple[int, ...],
        time_delta: float,
        num_raster_steps: int,
        raster_step: int,
        num_modstates: int,
        modstate: int,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.num_raster_steps = num_raster_steps
        self.add_constant_key("DKIST004", "observe")
        self.add_constant_key("DKIST011", "2022-11-28T13:55:00")
        self.add_constant_key("DKIST012", "2022-11-28T13:56:00")
        self.add_constant_key("VISP_019", num_raster_steps)
        self.add_constant_key("VISP_020", raster_step)
        self.add_constant_key("ID___004")
        self.add_constant_key("VISP_010", num_modstates)
        self.add_constant_key("VISP_011", modstate)
        self.add_constant_key("WAVELNTH", 656.28)
        self.add_constant_key("EXPER_ID", "EXPERIMENT ID")
        self.add_constant_key("CAM__014", 10)


def generate_fits_frame(header_generator: Iterable, shape=None) -> fits.HDUList:
    shape = shape or (1, 10, 10)
    generated_header = next(header_generator)
    translated_header = translate_spec122_to_spec214_l0(generated_header)
    del translated_header["COMMENT"]
    hdu = fits.PrimaryHDU(data=np.ones(shape=shape) * 150, header=fits.Header(translated_header))
    return fits.HDUList([hdu])


def generate_full_visp_fits_frame(
    header_generator: Iterable, data: np.ndarray | None = None
) -> fits.HDUList:
    if data is None:
        data = np.ones(shape=(1, 2000, 2560))
    data[0, 1000:, :] *= np.arange(1000)[:, None][::-1, :]  # Make beam 2 different and flip it
    generated_header = next(header_generator)
    translated_header = translate_spec122_to_spec214_l0(generated_header)
    del translated_header["COMMENT"]
    hdu = fits.PrimaryHDU(data=data, header=fits.Header(translated_header))
    return fits.HDUList([hdu])


def generate_214_l0_fits_frame(
    s122_header: fits.Header, data: np.ndarray | None = None
) -> fits.HDUList:
    """Convert S122 header into 214 L0"""
    if data is None:
        data = np.ones((1, 10, 10))
    translated_header = translate_spec122_to_spec214_l0(s122_header)
    del translated_header["COMMENT"]
    hdu = fits.PrimaryHDU(data=data, header=fits.Header(translated_header))
    return fits.HDUList([hdu])


def generate_214_l1_fits_frame(
    s122_header: fits.Header, data: np.ndarray | None = None
) -> fits.HDUList:
    """Convert S122 header into 214 L1 only.

    This does NOT include populating all L1 headers, just removing 214 L0 only headers

    NOTE: The stuff you care about will be in hdulist[1]
    """
    l0_s214_hdul = generate_214_l0_fits_frame(s122_header, data)
    l0_header = l0_s214_hdul[0].header
    l0_header["DNAXIS"] = 5
    l0_header["DAAXES"] = 2
    l0_header["DEAXES"] = 3
    l1_header = sanitize_to_spec214_level1(input_headers=l0_header)
    hdu = fits.CompImageHDU(header=l1_header, data=l0_s214_hdul[0].data)

    return fits.HDUList([fits.PrimaryHDU(), hdu])


class Visp122ObserveFrames(VispHeaders):
    def __init__(
        self,
        array_shape: tuple[int, ...],
        num_steps: int = 4,
        num_exp_per_step: int = 1,
        num_map_scans: int = 5,
    ):
        super().__init__(
            array_shape=array_shape,
            time_delta=10,
            dataset_shape=(num_exp_per_step * num_steps * num_map_scans,) + array_shape[-2:],
        )
        self.add_constant_key("DKIST004", "observe")


@pytest.fixture()
def init_visp_constants_db():
    def constants_maker(recipe_run_id: int, constants_obj):
        if is_dataclass(constants_obj):
            constants_obj = asdict(constants_obj)
        constants = VispConstants(recipe_run_id=recipe_run_id, task_name="test")
        constants._update(constants_obj)
        return

    return constants_maker


@dataclass
class VispConstantsDb:
    POLARIMETER_MODE: str = "observe_polarimetric"
    OBS_IP_START_TIME: str = "2022-11-28T13:54:00"
    NUM_MODSTATES: int = 10
    NUM_MAP_SCANS: int = 2
    NUM_RASTER_STEPS: int = 3
    NUM_BEAMS: int = 2
    NUM_CS_STEPS: int = 18
    NUM_SPECTRAL_BINS: int = 1
    NUM_SPATIAL_BINS: int = 1
    INSTRUMENT: str = "VISP"
    AVERAGE_CADENCE: float = 10.0
    MINIMUM_CADENCE: float = 10.0
    MAXIMUM_CADENCE: float = 10.0
    VARIANCE_CADENCE: float = 0.0
    WAVELENGTH: float = 588.0
    LAMP_EXPOSURE_TIMES: tuple[float] = (100.0,)
    SOLAR_EXPOSURE_TIMES: tuple[float] = (1.0,)
    OBSERVE_EXPOSURE_TIMES: tuple[float] = (0.01,)
    POLCAL_EXPOSURE_TIMES: tuple[float] = ()
    LAMP_READOUT_EXP_TIMES: tuple[float] = (200.0,)
    SOLAR_READOUT_EXP_TIMES: tuple[float] = (2.0,)
    OBSERVE_READOUT_EXP_TIMES: tuple[float] = (0.02,)
    POLCAL_READOUT_EXP_TIMES: tuple[float] = ()
    SPECTRAL_LINE: str = "VISP Ca II H"
    STOKES_PARAMS: tuple[str] = (
        "I",
        "Q",
        "U",
        "V",
    )  # A tuple because lists aren't allowed on dataclasses
    CONTRIBUTING_PROPOSAL_IDS: tuple[str] = (
        "PROPID1",
        "PROPID2",
    )
    CONTRIBUTING_EXPERIMENT_IDS: tuple[str] = (
        "EXPERID1",
        "EXPERID2",
        "EXPERID3",
    )
    AXIS_1_TYPE: str = "HPLT-TAN"
    AXIS_2_TYPE: str = "AWAV"
    AXIS_3_TYPE: str = "HPLN-TAN"


@pytest.fixture()
def recipe_run_id():
    return randint(0, 99999)


@pytest.fixture()
def visp_dataset() -> fits.Header:
    """
    A header with some common by-frame keywords
    """
    ds = VispHeaders(dataset_shape=(2, 10, 10), array_shape=(1, 10, 10), time_delta=1)
    header_list = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]

    return header_list[0]


@pytest.fixture()
def calibrated_visp_dataset(visp_dataset) -> fits.Header:
    """
    Same as visp_dataset but with a DATE-END key.

    Because now that's added during ScienceCal
    """
    visp_dataset["DATE-END"] = "2000-01-01T12:00:00.000000"

    return visp_dataset


@dataclass
class WavelengthParameter:
    values: tuple
    wavelength: tuple = (397.0, 588.0, 630.0, 854.0)  # This must always be in order

    def __hash__(self):
        return hash((self.values, self.wavelength))


@dataclass
class VispTestingParameters:
    visp_beam_border: int = 1000
    visp_background_on: bool = True
    visp_background_num_spatial_bins: WavelengthParameter = WavelengthParameter(values=(1, 4, 1, 1))
    visp_background_wavelength_subsample_factor: WavelengthParameter = WavelengthParameter(
        values=(10, 7, 10, 10)
    )
    visp_background_num_fit_iterations: WavelengthParameter = WavelengthParameter(
        values=(20, 100, 20, 20)
    )
    visp_background_continuum_index: WavelengthParameter = WavelengthParameter(
        values=(list(range(190)), list(range(190)), list(range(190)), list(range(190)))
    )
    visp_hairline_median_spatial_smoothing_width_px: int = 30
    visp_hairline_fraction: float = 0.11
    visp_hairline_mask_spatial_smoothing_width_px: float = 1.0
    visp_hairline_mask_gaussian_peak_cutoff_fraction: float = 0.02
    visp_geo_binary_opening_diameter: int = 21
    visp_geo_hairline_flat_id_threshold: float = 0.9
    visp_geo_hairline_fit_width_px: int = 10
    visp_geo_hairline_angle_fit_sig_clip: float = 3.0
    visp_geo_max_beam_2_angle_refinement: float = np.deg2rad(0.1)
    visp_geo_upsample_factor: float = 10.0
    visp_geo_max_shift: float = 40.0
    visp_geo_poly_fit_order: int = 3
    visp_solar_spectral_avg_window: WavelengthParameter = WavelengthParameter(
        values=(800, 800, 800, 800)
    )
    visp_solar_characteristic_spatial_normalization_percentile: float = 90.0
    visp_solar_zone_prominence: WavelengthParameter = WavelengthParameter(
        values=(0.2, 0.2, 0.3, 0.2)
    )
    visp_solar_zone_width: WavelengthParameter = WavelengthParameter(values=(7, 2, 3, 2))
    visp_solar_zone_bg_order: WavelengthParameter = WavelengthParameter(values=(21, 22, 11, 22))
    visp_solar_zone_normalization_percentile: WavelengthParameter = WavelengthParameter(
        values=(90, 99, 90, 90)
    )
    visp_solar_zone_rel_height: float = 0.97
    visp_max_cs_step_time_sec: float = 180.0
    visp_polcal_spatial_median_filter_width_px: int = 10
    visp_polcal_num_spatial_bins: int = 10
    visp_polcal_demod_spatial_smooth_fit_order: int = 17
    visp_polcal_demod_spatial_smooth_min_samples: float = 0.9
    visp_polcal_demod_upsample_order: int = 3
    visp_pac_remove_linear_I_trend: bool = True
    visp_pac_fit_mode: str = "use_M12_I_sys_per_step"
    visp_pac_init_set: str = "OCCal_VIS"


@pytest.fixture(scope="session")
def testing_wavelength() -> float:
    return 588.0


@pytest.fixture(scope="session")
def testing_obs_ip_start_time() -> str:
    return "1946-11-20T12:34:56"


@pytest.fixture(scope="session")
def input_dataset_document_simple_parameters_part():
    def get_input_dataset_parameters_part(parameters: VispTestingParameters):
        parameters_list = []
        value_id = randint(1000, 2000)
        for pn, pv in asdict(parameters).items():
            if type(pv) is WavelengthParameter:
                pv = asdict(pv)
            values = [
                {
                    "parameterValueId": value_id,
                    "parameterValue": json.dumps(pv),
                    "parameterValueStartDate": "1946-11-20",  # Remember Duane Allman
                }
            ]
            parameter = {"parameterName": pn, "parameterValues": values}
            parameters_list.append(parameter)
        return parameters_list

    return get_input_dataset_parameters_part


@pytest.fixture(scope="session")
def assign_input_dataset_doc_to_task(
    input_dataset_document_simple_parameters_part, testing_obs_ip_start_time, testing_wavelength
):
    def update_task(task, parameters):
        doc_path = task.scratch.workflow_base_path / "dataset_parameters.json"
        with open(doc_path, "w") as f:
            f.write(json.dumps(input_dataset_document_simple_parameters_part(parameters)))
        task.tag(doc_path, VispTag.input_dataset_parameters())
        task.parameters = VispParameters(
            task.input_dataset_parameters,
            obs_ip_start_time=testing_obs_ip_start_time,
            wavelength=testing_wavelength,
        )

    return update_task
