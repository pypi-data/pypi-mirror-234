"""CryoNIRSP additions to common constants."""
from enum import Enum

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.constants import ConstantsBase


class CryonirspBudName(Enum):
    """Names to be used for CryoNIRSP buds."""

    arm_id = "ARM_ID"
    num_beams = "NUM_BEAMS"
    num_scan_steps = "NUM_SCAN_STEPS"
    num_map_scans = "NUM_MAP_SCANS"
    num_modstates = "NUM_MODSTATES"
    wavelength = "WAVELENGTH"
    camera_readout_mode = "CAM_READOUT_MODE"
    num_meas = "NUM_MEAS"
    time_obs_list = "TIME_OBS_LIST"
    lamp_gain_exposure_times = "LAMP_GAIN_EXPOSURE_TIMES"
    solar_gain_exposure_times = "SOLAR_GAIN_EXPOSURE_TIMES"
    polcal_exposure_times = "POLCAL_EXPOSURE_TIMES"
    observe_exposure_times = "OBSERVE_EXPOSURE_TIMES"
    non_dark_task_exposure_times = "NON_DARK_TASK_EXPOSURE_TIMES"
    modulator_spin_mode = "MODULATOR_SPIN_MODE"
    axis_1_type = "AXIS_1_TYPE"
    axis_2_type = "AXIS_2_TYPE"
    axis_3_type = "AXIS_3_TYPE"
    roi_1_origin_x = "ROI_1_ORIGIN_X"
    roi_1_origin_y = "ROI_1_ORIGIN_Y"
    roi_1_size_x = "ROI_1_SIZE_X"
    roi_1_size_y = "ROI_1_SIZE_Y"


class CryonirspConstants(ConstantsBase):
    """CryoNIRSP specific constants to add to the common constants."""

    @property
    def arm_id(self) -> str:
        """Arm used to record the data, SP or CI."""
        return self._db_dict[CryonirspBudName.arm_id.value]

    @property
    def num_beams(self) -> int:
        """Determine the number of beams present in the data."""
        if self.arm_id == "SP":
            return 2
        else:
            return 1

    @property
    def num_scan_steps(self) -> int:
        """Determine the number of scan steps."""
        return self._db_dict[CryonirspBudName.num_scan_steps.value]

    @property
    def num_map_scans(self) -> int:
        """Determine the number of scan steps."""
        return self._db_dict[CryonirspBudName.num_map_scans.value]

    @property
    def wavelength(self) -> float:
        """Wavelength."""
        return self._db_dict[CryonirspBudName.wavelength.value]

    @property
    def camera_readout_mode(self) -> str:
        """Determine the readout mode of the camera."""
        return self._db_dict[CryonirspBudName.camera_readout_mode.value]

    @property
    def num_meas(self) -> int:
        """Determine the number of measurements in dataset."""
        return self._db_dict[CryonirspBudName.num_meas.value]

    @property
    def time_obs_list(self) -> tuple[str]:
        """Construct a sorted tuple of all the dateobs for this dataset."""
        return self._db_dict[CryonirspBudName.time_obs_list.value]

    @property
    def lamp_gain_exposure_times(self) -> [float]:
        """Construct a list of lamp gain exposure times for the dataset."""
        return self._db_dict[CryonirspBudName.lamp_gain_exposure_times.value]

    @property
    def solar_gain_exposure_times(self) -> [float]:
        """Construct a list of solar gain exposure times for the dataset."""
        return self._db_dict[CryonirspBudName.solar_gain_exposure_times.value]

    @property
    def polcal_exposure_times(self) -> [float]:
        """Construct a list of polcal exposure times for the dataset."""
        if self.correct_for_polarization:
            return self._db_dict[CryonirspBudName.polcal_exposure_times.value]
        else:
            return []

    @property
    def observe_exposure_times(self) -> [float]:
        """Construct a list of observe exposure times."""
        return self._db_dict[CryonirspBudName.observe_exposure_times.value]

    @property
    def non_dark_task_exposure_times(self) -> [float]:
        """Return a list of all exposure times required for all tasks other than dark."""
        exposure_times = list()
        exposure_times.extend(self.lamp_gain_exposure_times)
        exposure_times.extend(self.solar_gain_exposure_times)
        exposure_times.extend(self.observe_exposure_times)
        exposure_times = list(set(exposure_times))
        return exposure_times

    @property
    def num_modstates(self) -> int:
        """Find the number of modulation states."""
        return self._db_dict[CryonirspBudName.num_modstates.value]

    @property
    def num_cs_steps(self) -> int:
        """Find the number of calibration sequence steps."""
        return self._db_dict[BudName.num_cs_steps.value]

    @property
    def stokes_I_list(self) -> [str]:
        """List containing only the Stokes-I parameter."""
        return ["I"]

    @property
    def correct_for_polarization(self) -> bool:
        """Correct for polarization."""
        return self.num_modstates > 1 and self._db_dict[
            CryonirspBudName.modulator_spin_mode.value
        ] in ["Continuous", "Stepped"]

    @property
    def axis_1_type(self) -> str:
        """Find the type of the first array axis."""
        return self._db_dict[CryonirspBudName.axis_1_type.value]

    @property
    def axis_2_type(self) -> str:
        """Find the type of the second array axis."""
        return self._db_dict[CryonirspBudName.axis_2_type.value]

    @property
    def axis_3_type(self) -> str:
        """Find the type of the third array axis."""
        return self._db_dict[CryonirspBudName.axis_3_type.value]

    @property
    def roi_1_origin_x(self) -> int:
        """Get the ROI #1 x origin."""
        return self._db_dict[CryonirspBudName.roi_1_origin_x.value]

    @property
    def roi_1_origin_y(self) -> int:
        """Get the ROI #1 y origin."""
        return self._db_dict[CryonirspBudName.roi_1_origin_y.value]

    @property
    def roi_1_size_x(self) -> int:
        """Get the ROI #1 x size."""
        return self._db_dict[CryonirspBudName.roi_1_size_x.value]

    @property
    def roi_1_size_y(self) -> int:
        """Get the ROI #1 y size."""
        return self._db_dict[CryonirspBudName.roi_1_size_y.value]
