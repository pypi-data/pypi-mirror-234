"""Cryo gain task."""
from abc import abstractmethod
from typing import Callable

import numpy as np
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from logging42 import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class GainCalibrationBase(CryonirspTaskBase):
    """
    Base task class for calculation of average lamp or solar gains for CI and average lamp gains for SP.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    @abstractmethod
    def gain_type(self) -> str:
        """Return the gain type, SOLAR_GAIN or LAMP_GAIN."""
        pass

    @property
    @abstractmethod
    def exposure_times(self) -> [float]:
        """Return the exposure times list."""
        pass

    @property
    @abstractmethod
    def gain_array_generator(self) -> Callable:
        """Return the gain array generator to use based on the gain type."""
        pass

    record_provenance = True

    def run(self):
        """
        Execute the task.

        For each exposure time and beam:
            - Gather input gain and averaged dark arrays
            - Calculate average array
            - Normalize average array
            - Write average gain array
            - Record quality metrics

        Returns
        -------
        None

        """
        with self.apm_task_step(
            f"Generate {self.gain_type} for {len(self.exposure_times)} exposure times"
        ):
            for exp_time in self.exposure_times:
                # NB: By using num_beams = 1 for CI, this method works for both CI and SP
                for beam in range(1, self.constants.num_beams + 1):
                    apm_str = f"{beam = } and {exp_time = }"
                    with self.apm_processing_step(f"Remove dark signal for {apm_str}"):
                        dark_array = self.intermediate_frame_load_dark_array(
                            beam=beam, exposure_time=exp_time
                        )

                        avg_gain_array = self.compute_average_gain_array(
                            beam=beam, exp_time=exp_time
                        )

                        dark_corrected_gain_array = next(
                            subtract_array_from_arrays(avg_gain_array, dark_array)
                        )

                    with self.apm_processing_step(f"Correct bad pixels for {apm_str}"):
                        bad_pixel_map = self.intermediate_frame_load_bad_pixel_map(beam=beam)
                        bad_pixel_corrected_array = self.corrections_correct_bad_pixels(
                            dark_corrected_gain_array, bad_pixel_map
                        )

                    with self.apm_processing_step(f"Normalize final gain for {apm_str}"):
                        normalized_gain_array = self.normalize_gain(bad_pixel_corrected_array)

                    with self.apm_writing_step(
                        f"Writing gain array for {beam = } and {exp_time = }"
                    ):
                        self.intermediate_frame_write_arrays(
                            normalized_gain_array,
                            beam=beam,
                            task=self.gain_type,
                            modstate=1,
                        )

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_gain_frames: int = self.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task(self.gain_type),
                ],
            )

            self.quality_store_task_type_counts(
                task_type=self.gain_type, total_frames=no_of_raw_gain_frames
            )

    def compute_average_gain_array(
        self,
        beam: int,
        exp_time: float,
    ) -> np.ndarray:
        """
        Compute average gain array for a given exp time and beam.

        Parameters
        ----------
        beam : int
            The number of the beam

        exp_time : float
            Exposure time

        Returns
        -------
        np.ndarray
        """
        linearized_gain_arrays = self.gain_array_generator(beam=beam, exposure_time=exp_time)
        averaged_gain_data = average_numpy_arrays(linearized_gain_arrays)
        return averaged_gain_data

    @staticmethod
    def normalize_gain(gain_array: np.ndarray) -> np.ndarray:
        """
        Normalize gain to a mean of 1.

        Find any residual pixels that are zero valued and set them to 1.

        Parameters
        ----------
        gain_array : np.ndarray
            Dark corrected gain array

        Returns
        -------
        np.ndarray
            Normalized dark-corrected gain array

        """
        avg = np.nanmean(gain_array)
        gain_array /= avg
        # Find and fix any residual zeros that slipped through the bad pixel corrections.
        # zeros = np.where(gain_array == 0.0)
        # gain_array[zeros] = 1.0

        return gain_array


class LampGainCalibration(GainCalibrationBase):
    """
    Task class for calculation of an average lamp gain frame for a CryoNIRSP CI or SP calibration run.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    def gain_type(self) -> str:
        """Return the gain type, SOLAR_GAIN or LAMP_GAIN."""
        return TaskName.lamp_gain.value

    @property
    def exposure_times(self) -> [float]:
        """Return the exposure times list."""
        return self.constants.lamp_gain_exposure_times

    @property
    def gain_array_generator(self) -> Callable:
        """Return the gain array generator to use based on the gain type."""
        return self.linearized_frame_lamp_gain_array_generator


class CISolarGainCalibration(GainCalibrationBase):
    """
    Task class for calculation of an average solar gain frame for a CryoNIRSP CI calibration run.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    def gain_type(self) -> str:
        """Return the gain type, SOLAR_GAIN or LAMP_GAIN."""
        return TaskName.solar_gain.value

    @property
    def exposure_times(self) -> [float]:
        """Return the exposure times list."""
        return self.constants.solar_gain_exposure_times

    @property
    def gain_array_generator(self) -> Callable:
        """Return the gain array generator to use based on the gain type."""
        return self.linearized_frame_solar_gain_array_generator
