"""CryoNIRSP compute beam boundary task."""
from abc import abstractmethod

import numpy as np
from dkist_processing_math.statistics import average_numpy_arrays
from logging42 import logger
from skimage import filters
from skimage import img_as_ubyte
from skimage.exposure import rescale_intensity
from skimage.morphology import disk

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class BeamBoundariesCalibrationBase(CryonirspTaskBase):
    """
    Task class for calculation of the beam boundaries for later use during calibration.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    record_provenance = True

    def run(self):
        """
        Compute the beam boundaries by analyzing a set of solar gain images.

        Steps:
        1. Compute the average gain image
        2. Correct any bad pixels
        3. Smooth the image using a median filter with radius 3
        4. Use a bimodal threshold filter to segment the image into illuminated and non-illuminated regions
        5. Compute the boundaries of the illuminated region
        6. Extract the illuminated portion of the image
        7. Split the beams using a 10% buffer region around the horizontal mid-point
        8. Find the horizontal shift between the two images
        9. Identify the boundaries of the overlap
        10. Save the boundaries as a fits file (json?)


        Returns
        -------
        None

        """
        # Step 1:
        with self.apm_processing_step(f"Compute average solar gain image"):
            average_solar_gain_array = self._compute_average_gain_array()

        # Step 2:
        with self.apm_task_step(f"Retrieve bad pixel map"):
            bad_pixel_map = self.intermediate_frame_load_full_bad_pixel_map()
            corrected_solar_gain_array = self.corrections_correct_bad_pixels(
                average_solar_gain_array, bad_pixel_map
            )

        # Step 3
        with self.apm_processing_step(f"Smooth the array to get good segmentation"):
            smoothed_solar_gain_array = self._smooth_gain_array(corrected_solar_gain_array)

        # Step 4:
        with self.apm_processing_step(
            f"Segment the array into illuminated and non-illuminated pixels"
        ):
            segmented_array = self._segment_array(smoothed_solar_gain_array)

        # Step 5:
        with self.apm_processing_step(
            f"Compute the inscribed rectangular extent of the illuminated portion of the sensor"
        ):
            illuminated_boundaries = self._compute_illuminated_boundaries(segmented_array)

        # Steps 6 - 9:
        with self.apm_processing_step(f"Compute the beam boundaries of the illuminated region"):
            boundaries = self._compute_beam_boundaries(
                smoothed_solar_gain_array, illuminated_boundaries
            )

        # Step 10:
        with self.apm_writing_step("Writing beam boundaries"):
            for beam, array in enumerate(boundaries, start=1):
                self.intermediate_frame_write_arrays(
                    array, task_tag=CryonirspTag.task_beam_boundaries(), beam=beam
                )

    def _compute_average_gain_array(self) -> np.ndarray:
        """
        Compute an average of uncorrected solar gain arrays.

        We are computing the overall illumination pattern for both beams simultaneously,
        so no dark correction is required and no beam splitting is used at this point.
        Solar gain images are used because they have larger flux than the lamp gain images
        and the lamp gain images do not have the same illumination pattern as the solar
        gain images.

        Returns
        -------
        The average gain array
        """
        lin_corr_gain_arrays = self.linearized_frame_full_array_generator(
            tags=[
                CryonirspTag.task_solar_gain(),
                CryonirspTag.linearized(),
                CryonirspTag.frame(),
            ]
        )
        averaged_gain_data = average_numpy_arrays(lin_corr_gain_arrays)
        return averaged_gain_data

    def _smooth_gain_array(self, array: np.ndarray) -> np.ndarray:
        """
        Smooth the input array with morphological filtering using a disk shape.

        The array is smoothed to help eliminate artifacts in the image segmentation step.

        Parameters
        ----------
        array
            The input array to be smoothed

        Returns
        -------
        The smoothed output array
        """
        # skimage.filters requires ubyte arrays and float->ubyte conversion only works with float in range [-1, 1]
        norm_gain = img_as_ubyte(rescale_intensity(array, out_range=(0, 1.0)))

        disk_size = self.parameters.beam_boundaries_smoothing_disk_size
        norm_gain = filters.rank.median(norm_gain, disk(disk_size))
        return norm_gain

    @staticmethod
    def _segment_array(array: np.ndarray) -> np.ndarray:
        """
        Segment the array into illuminated (True) and non-illuminated (False) regions.

        Parameters
        ----------
        array
            The array to be segmented

        Returns
        -------
        The boolean segmented output array
        """
        thresh = filters.threshold_minimum(array)
        logger.info(f"Segmentation threshold = {thresh}")
        segmented_array = (array > thresh).astype(bool)
        return segmented_array

    @abstractmethod
    def _compute_illuminated_boundaries(self, array: np.ndarray) -> list[int]:
        """
        Compute the inscribed rectangular extent of the illuminated portion of the array.

        Parameters
        ----------
        array
            The segmented boolean array over which the illuminated boundaries are to be computed

        Returns
        -------
        The illuminated region boundaries, [y_min, y_max, x_min, x_max]
        """
        pass

    @abstractmethod
    def _compute_beam_boundaries(
        self, smoothed_solar_gain_array: np.ndarray, illuminated_boundaries: list[int]
    ):
        """
        Compute the beam boundaries from the illuminated beam.

        Parameters
        ----------
        smoothed_solar_gain_array
            The smoothed solar gain array, ready for beam identification
        illuminated_boundaries
            The boundaries of the illuminated beam [y_min, y_max, x_min, x_max]

        Returns
        -------
        A list of beam boundary arrays, one for each beam
        """
        pass
