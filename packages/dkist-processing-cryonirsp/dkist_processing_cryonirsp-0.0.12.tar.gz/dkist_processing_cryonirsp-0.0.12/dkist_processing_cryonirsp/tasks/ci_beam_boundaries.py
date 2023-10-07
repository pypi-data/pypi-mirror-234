"""Cryonirsp CI beam boundaries task."""
import largestinteriorrectangle as lir
import numpy as np
from logging42 import logger

from dkist_processing_cryonirsp.tasks.beam_boundaries_base import BeamBoundariesCalibrationBase


class CIBeamBoundariesCalibration(BeamBoundariesCalibrationBase):
    """Task class for calculation of the CI beam boundaries for later use during calibration."""

    def _compute_beam_boundaries(
        self, smoothed_solar_gain_array: np.ndarray, illuminated_boundaries: list[int]
    ):
        """
        Compute the CI beam boundaries from the illuminated beam.

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
        beam_boundaries = np.array(illuminated_boundaries)
        return [beam_boundaries]

    def _compute_illuminated_boundaries(self, array: np.ndarray) -> list[int]:
        """
        Compute the inscribed rectangular extent of the illuminated portion of the array for CI.

        Parameters
        ----------
        array
            The segmented boolean array over which the illuminated boundaries are to be computed

        Returns
        -------
        The illuminated region boundaries, [y_min, y_max, x_min, x_max]
        """
        inscribed_rect = lir.lir(array)

        # Compute the new image bounds, the maximums are exclusive and can be used in slices
        y_min = inscribed_rect[1]
        y_max = y_min + inscribed_rect[3]
        x_min = inscribed_rect[0]
        x_max = x_min + inscribed_rect[2]

        # Make sure all pixels are 1s
        if not np.all(array[y_min:y_max, x_min:x_max]):
            raise RuntimeError("Unable to compute illuminated image boundaries")

        logger.info(f"Illuminated boundaries: [{y_min}:{y_max}, {x_min}:{x_max}]")
        return [y_min, y_max, x_min, x_max]
