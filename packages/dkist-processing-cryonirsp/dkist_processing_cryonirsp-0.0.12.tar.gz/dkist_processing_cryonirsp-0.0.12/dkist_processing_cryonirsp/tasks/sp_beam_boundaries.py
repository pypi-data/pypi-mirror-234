"""Cryonirsp SP beam boundaries task."""
import largestinteriorrectangle as lir
import numpy as np
from logging42 import logger
from skimage.registration import phase_cross_correlation

from dkist_processing_cryonirsp.tasks.beam_boundaries_base import BeamBoundariesCalibrationBase


class SPBeamBoundariesCalibration(BeamBoundariesCalibrationBase):
    """Task class for calculation of the SP beam boundaries for later use during calibration."""

    def _compute_beam_boundaries(
        self, smoothed_solar_gain_array: np.ndarray, illuminated_boundaries: list[int]
    ):
        """
        Compute the SP beam boundaries from the illuminated beam and save them as a file.

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
        illuminated_array = smoothed_solar_gain_array[
            illuminated_boundaries[0] : illuminated_boundaries[1],
            illuminated_boundaries[2] : illuminated_boundaries[3],
        ]

        # Step 7:
        # Split the beams
        split_boundary = self._compute_split_boundary(illuminated_array)
        left_beam, right_beam = self._split_beams(illuminated_array, split_boundary)

        # Step 8:
        shift = self._compute_spectral_shift(left_beam, right_beam)

        # Step 9:
        beam_1_boundaries, beam_2_boundaries = self._compute_sp_beam_overlap_boundaries(
            illuminated_boundaries, split_boundary, shift
        )
        return [beam_1_boundaries, beam_2_boundaries]

    def _compute_illuminated_boundaries(self, array: np.ndarray) -> list[int]:
        """
        Compute the inscribed rectangular extent of the illuminated portion of the array for SP.

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

        original_spectral_size = array.shape[1]
        x_min, x_max = self._ensure_even_spectra_slice(x_min, x_max, original_spectral_size)

        logger.info(f"Illuminated boundaries: [{y_min}:{y_max}, {x_min}:{x_max}]")
        return [y_min, y_max, x_min, x_max]

    def _compute_split_boundary(self, illuminated_array: np.ndarray) -> list[int]:
        """
        Compute the split boundary for the illuminated region.

        The split boundary is a region in the middle of the illuminated region where the transition between the beams
        occurs and is not used for processing

        Parameters
        ----------
        illuminated_array
            The array containing the illuminated region of the image

        Returns
        -------
        list[region_start, region_end]
        """
        spectral_center = illuminated_array.shape[1] // 2
        transition_region_size = round(
            illuminated_array.shape[1]
            * self.parameters.beam_boundaries_sp_beam_transition_region_size_fraction
        )

        split_boundary = [
            spectral_center - transition_region_size,
            spectral_center + transition_region_size,
        ]
        return split_boundary

    def _compute_spectral_shift(self, left_beam: np.ndarray, right_beam: np.ndarray) -> int:
        """
        Compute the spectral shift between the two beams using a cross correlation.

        Parameters
        ----------
        left_beam
            The coarse left beam image

        right_beam
            The coarse right beam image

        Returns
        -------
        horizontal pixel index shift required to align the beams
        """
        # NOTE: We only compute a spectral shift right now, but if we ever need both spatial and spectral then this
        # is the place to do it (`shifts` contains both).
        upsample_factor = self.parameters.beam_boundaries_upsample_factor
        shifts = phase_cross_correlation(
            left_beam, right_beam, upsample_factor=upsample_factor, return_error=False
        )
        # Round to int because this is an index/pixel shift
        spectral_shift = round(shifts[1])
        logger.info(f"{spectral_shift = }")

        return spectral_shift

    @staticmethod
    def _ensure_even_spectra_slice(min_idx, max_idx, full_size):
        """
        Adjust spectral beam boundary so that the resulting illuminated region has an even number of spectral pixels.

        We need this because the rough beam-separation first divides the spectral region in 2, and we need the resulting
        arrays to have the same size.

        If the initial region does not have an even number of spectral pixels then a single pixel is taken from whatever
        side of the region is closest to the chip edge.

        In other words, we only even remove a single pixel and we always *remove* an illuminated pixel (never add a
        non-illuminated pixel).
        """
        illuminated_size = max_idx - min_idx

        if not illuminated_size % 2 == 0:
            min_side_unilluminated_size = min_idx - 1
            max_side_unilluminated_size = full_size - max_idx

            # Remove an illuminated pixel from the limit has the smaller unilluminated region
            if min_side_unilluminated_size > max_side_unilluminated_size:
                max_idx -= 1
            else:
                min_idx += 1

        return min_idx, max_idx

    @staticmethod
    def _split_beams(array: np.ndarray, split_boundary: list[int]) -> tuple[np.ndarray, np.ndarray]:
        """
        Split the beams coarsely along the horizontal axis in preparation for alignment.

        Parameters
        ----------
        array
            The array to be split

        split_boundary
            The split boundary locations [left_max, right_min]

        Returns
        -------
        tuple containing the split beams
        """
        left_beam = array[:, : split_boundary[0]]
        right_beam = array[:, split_boundary[1] :]
        return left_beam, right_beam

    @staticmethod
    def _compute_sp_beam_overlap_boundaries(
        illuminated_boundaries: list[int], split_boundary: list[int], shift: float
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Compute the final boundaries to be used when extracting beams from the original input images.

        Parameters
        ----------
        illuminated_boundaries
            The boundaries of the illuminated portion of the image (includes both beams)

        split_boundary
            The central region to be unused, where the split occurs

        shift
            The horizontal shift required to align the two beam images

        Returns
        -------
        (beam_1_boundaries, beam_2_boundaries), where each beam boundary is defined as:
        np.array([spatial_min, spatial_max, spectral_min, spectral_max]
        """
        spatial_min, spatial_max, spectral_min, spectral_max = illuminated_boundaries

        # The values computed here are to be used relative to the *uncorrected* full-size input images
        # The split boundaries are relative to the extracted illuminated beam, not the original beam
        if shift < 0:
            beam_1_spectral_min = spectral_min
            beam_1_spectral_max = spectral_min + split_boundary[0] + shift
            beam_2_spectral_min = spectral_min + split_boundary[1] - shift
            beam_2_spectral_max = spectral_max
        else:
            beam_1_spectral_min = spectral_min + shift
            beam_1_spectral_max = spectral_min + split_boundary[0]
            beam_2_spectral_min = spectral_min + split_boundary[1]
            beam_2_spectral_max = spectral_max - shift

        # For now, spatial_min and spatial_max are the same for both beams. This may change in the future.
        beam_1_boundaries = np.array(
            [spatial_min, spatial_max, beam_1_spectral_min, beam_1_spectral_max], dtype=int
        )
        beam_2_boundaries = np.array(
            [spatial_min, spatial_max, beam_2_spectral_min, beam_2_spectral_max], dtype=int
        )
        logger.info(f"{beam_1_boundaries = }")
        logger.info(f"{beam_2_boundaries = }")

        # NB: The upper bounds are exclusive, ready to be used in array slicing
        return beam_1_boundaries, beam_2_boundaries
