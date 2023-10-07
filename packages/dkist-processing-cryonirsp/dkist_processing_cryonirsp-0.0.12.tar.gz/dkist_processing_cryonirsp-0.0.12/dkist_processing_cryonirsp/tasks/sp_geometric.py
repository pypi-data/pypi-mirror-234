"""Cryo SP geometric task."""
import math
from collections.abc import Generator

import numpy as np
import peakutils as pku
import scipy.ndimage as spnd
import skimage.registration as skir
from dkist_processing_math.arithmetic import divide_arrays_by_array
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from logging42 import logger
from scipy.optimize import minimize

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class SPGeometricCalibration(CryonirspTaskBase):
    """Task class for computing the spectral geometry. Geometry is represented by three quantities.

      - angle - The angle (in radians) between slit hairlines and pixel axes. A one dimensional array with two elements- one for each beam.

      - beam offset - The [x, y] shift of beam 2 relative to beam 1 (the reference beam). Two beam offset values are computed.

      - spectral shift - The shift in the spectral dimension for each beam for every spatial position needed to "straighten" the spectra so a single wavelength is at the same pixel for all slit positions.Task class for computing the spectral geometry for a SP CryoNIRSP calibration run.

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
        Run method for the task.

        For each beam.

            - Gather dark corrected frames
            - Calculate spectral tilt (angle)
            - Remove spectral tilt
            - Using the angle corrected array, find the beam offset
            - Write beam offset
            - Calculate the spectral skew and curvature (spectral shifts)
            - Write the spectral skew and curvature


        Returns
        -------
        None

        """
        # The basic corrections are done outside the loop structure below as it makes these loops much
        # simpler than they would be otherwise. See the comments in do_basic_corrections for more details.
        with self.apm_processing_step("Basic corrections"):
            self.do_basic_corrections()

        for beam in range(1, self.constants.num_beams + 1):
            with self.apm_task_step(f"Generating geometric calibrations for {beam = }"):
                with self.apm_processing_step(f"Computing and writing angle for {beam = }"):
                    angle = self.compute_beam_angle(beam=beam)
                    self.write_angle(angle=angle, beam=beam)

                with self.apm_processing_step(f"Removing angle from {beam = }"):
                    angle_corr_array = self.remove_beam_angle(angle=angle, beam=beam)

                with self.apm_processing_step(f"Computing offset for {beam = }"):
                    beam_offset = self.compute_offset(
                        array=angle_corr_array,
                        beam=beam,
                    )
                    self.write_beam_offset(offset=beam_offset, beam=beam)

                with self.apm_processing_step(f"Removing offset for {beam = }"):
                    self.remove_beam_offset(
                        array=angle_corr_array,
                        offset=beam_offset,
                        beam=beam,
                    )

                with self.apm_processing_step(f"Computing spectral shifts for {beam = }"):
                    spec_shifts = self.compute_spectral_shifts(beam=beam)

                with self.apm_writing_step(f"Writing spectral shifts for {beam = }"):
                    self.write_spectral_shifts(shifts=spec_shifts, beam=beam)

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_geo_frames: int = self.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task_solar_gain(),
                ],
            )

            self.quality_store_task_type_counts(
                task_type=TaskName.geometric.value, total_frames=no_of_raw_geo_frames
            )

    def basic_corrected_data(self, beam: int) -> np.ndarray:
        """
        Get dark corrected data array for a single beam.

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        np.ndarray
            Dark corrected data array
        """
        array_generator = self.intermediate_frame_load_intermediate_arrays(
            tags=[CryonirspTag.task("GC_BASIC"), CryonirspTag.beam(beam)]
        )
        return average_numpy_arrays(array_generator)

    def offset_corrected_data(self, beam: int) -> np.ndarray:
        """
        Array for a single beam that has been corrected for the x/y beam offset.

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        np.ndarray
            Offset corrected data array
        """
        array_generator = self.intermediate_frame_load_intermediate_arrays(
            tags=[CryonirspTag.task("GC_OFFSET"), CryonirspTag.beam(beam)]
        )
        return average_numpy_arrays(array_generator)

    def do_basic_corrections(self):
        """Apply dark, bad pixel and lamp gain corrections to all data that will be used for Geometric Calibration."""
        # There is likely only a single exposure time in the list, but we iterate over the list
        # in case there are multiple exposure times. We also need a specific exposure time tag
        # to ensure we get the proper dark arrays to use in the correction.
        for exp_time in self.constants.solar_gain_exposure_times:
            for beam in range(1, self.constants.num_beams + 1):
                logger.info(f"Starting basic reductions for {exp_time = } and {beam = }")
                try:
                    dark_array = self.intermediate_frame_load_dark_array(
                        beam=beam, exposure_time=exp_time
                    )
                except StopIteration as e:
                    raise ValueError(f"No matching dark found for {exp_time = } s") from e

                lamp_gain_array = self.intermediate_frame_load_lamp_gain_array(
                    beam=beam,
                )

                input_solar_arrays = self.linearized_frame_gain_array_generator(
                    gain_type=TaskName.solar_gain.value,
                    beam=beam,
                    exposure_time=exp_time,
                )

                avg_solar_array = average_numpy_arrays(input_solar_arrays)

                dark_corrected_solar_array = next(
                    subtract_array_from_arrays(arrays=avg_solar_array, array_to_subtract=dark_array)
                )

                bad_pixel_map = self.intermediate_frame_load_bad_pixel_map(beam=beam)
                bad_pixel_corrected_array = self.corrections_correct_bad_pixels(
                    dark_corrected_solar_array, bad_pixel_map
                )

                gain_corrected_solar_array = next(
                    divide_arrays_by_array(bad_pixel_corrected_array, lamp_gain_array)
                )
                logger.info(f"Writing gain corrected data for {beam=}")
                self.intermediate_frame_write_arrays(
                    arrays=gain_corrected_solar_array,
                    beam=beam,
                    task="GC_BASIC",
                )

    def compute_beam_angle(self, beam: int) -> float:
        """
        Compute the angle between dispersion and pixel axes for a given beam.

        The algorithm works as follows:

        1. Load the lamp gain array for this beam
        2. Compute a gradient array by shifting the array along the spatial axis (along the slit) and
           calculating a normalized finite difference with the original array.
        3. Compute 2D slices for two strips that are on either side of the spectral center.
        4. Extract the spatial strips as arrays and compute the median values along their spectral axis.
        5. Compute the relative shift of the right strip to the left strip (this is the shift along the spatial axis)
        6. Compute the angular rotation of the beam relative to the array axes from the shift
           and the separation of the strips along the spectral axis

        Returns
        -------
        The beam rotation angle in radians
        """
        # 1.
        lamp_data = self.intermediate_frame_load_lamp_gain_array(beam=beam)
        full_spatial_size, full_spectral_size = lamp_data.shape

        # 2.
        roll_amount = self.parameters.geo_spatial_gradient_displacement
        spatial_gradient = (
            np.roll(lamp_data, roll_amount, axis=0) - np.roll(lamp_data, -roll_amount, axis=0)
        ) / (np.roll(lamp_data, roll_amount, axis=0) + np.roll(lamp_data, -roll_amount, axis=0))

        # 3.
        spatial_strip_slice = self._compute_spatial_strip_slice(full_spatial_size)
        left_spectral_strip_slice, right_spectral_strip_slice = self._compute_spectral_strip_slices(
            full_spectral_size
        )
        logger.info(
            f"Left strip slice: [{spatial_strip_slice.start}:{spatial_strip_slice.stop}, "
            f"{left_spectral_strip_slice.start}:{left_spectral_strip_slice.stop}]"
        )
        logger.info(
            f"Right strip slice: [{spatial_strip_slice.start}:{spatial_strip_slice.stop}, "
            f"{right_spectral_strip_slice.start}:{right_spectral_strip_slice.stop}]"
        )

        # 4.
        left_strip = spatial_gradient[spatial_strip_slice, left_spectral_strip_slice]
        right_strip = spatial_gradient[spatial_strip_slice, right_spectral_strip_slice]

        # "slit_function" AKA a 1D array of flux along the slit
        left_slit_function = np.nanmedian(left_strip, axis=1)
        right_slit_function = np.nanmedian(right_strip, axis=1)

        # 5.
        # Multiply by -1 to convert from correction to measurement
        shift = (
            -1
            * skir.phase_cross_correlation(
                left_slit_function,
                right_slit_function,
                upsample_factor=self.parameters.geo_upsample_factor,
                return_error=False,
            )[0]
        )
        logger.info(f"Measured shift of beam {beam} = {shift}")

        # 6.
        spectral_offset = math.ceil(
            full_spectral_size * self.parameters.geo_strip_spectral_offset_size_fraction
        )
        beam_angle = np.arctan(shift / (2 * spectral_offset))
        logger.info(f"Measured angle for beam {beam} = {np.rad2deg(beam_angle):0.3f} deg")

        return beam_angle

    def _compute_spatial_strip_slice(self, full_spatial_size: int) -> slice:
        """
        Compute a `slice` that defines the spatial extent of the strips used to find the beam angle.

        The strip is forced to be centered at the center of the slit and has a spatial size determined by the
        `geo_strip_spatial_size_fraction` parameter.

        The following diagram shows and example of this. The full spatial axis is shown and the pixels to be sliced
        as part of a strip are shown as # symbols.

                    |
                    |
             ______---
             |      #
             |      #
             |      #
           s-|      .   Spatial center
             |      #
             |      #
             |      #
             ▔▔▔▔▔▔---
                    |
                    |

        Where `s = geo_strip_spatial_size_fraction * full_spatial_size` is the size of the strip in the spatial dimension.
        """
        strip_spatial_size = math.ceil(
            full_spatial_size * self.parameters.geo_strip_spatial_size_fraction
        )
        if not strip_spatial_size % 2 == 0:
            strip_spatial_size += 1

        # Distribute the `// 2` to see why this works
        slice_idx = (np.array([-strip_spatial_size, strip_spatial_size]) + full_spatial_size) // 2

        return slice(*slice_idx)

    def _compute_spectral_strip_slices(self, full_spectral_size: int) -> tuple[slice, slice]:
        """
        Compute a `slice` that defines the spectral extent of two strips used to find the beam angle.

        The two strips have the same spectral size (determined by `geo_strip_spectral_size_fraction`) and are offset
        from the center of the spectral axis by an amount defined by the `geo_strip_spectral_offset_size_fraction`
        parameter.

        The following diagram shows an example of this. The full spectral axis is shown, and the pixels identified with
        the two strips are shown with # symbols.

           lstrip                  rstrip
        --|#######|-------.-------|#######|--
              s       o   |   o       s
                          |
                   Spectral center

        Where `s = geo_strip_spectral_size_fraction * full_spectral_size` is the spectral size of each strip and
        `o = geo_strip_spectral_offset_size_fraction * full_spectral_size` is the offset of each strip from spectral
        center.
        """
        strip_spectral_size = math.ceil(
            full_spectral_size * self.parameters.geo_strip_spectral_size_fraction
        )
        if not strip_spectral_size % 2 == 0:
            strip_spectral_size += 1

        spectral_offset = math.ceil(
            full_spectral_size * self.parameters.geo_strip_spectral_offset_size_fraction
        )

        # Distribute the `// 2` to see why this works
        base_idx = (np.array([-strip_spectral_size, strip_spectral_size]) + full_spectral_size) // 2

        left_idx = base_idx - spectral_offset
        right_idx = base_idx + spectral_offset

        return slice(*left_idx), slice(*right_idx)

    def remove_beam_angle(self, angle: float, beam: int) -> np.ndarray:
        """
        De-rotate the beam array using the measured angle to align the slit with the array axes.

        Parameters
        ----------
        angle : float
            The measured beam rotation angle (in radians)
        beam : int
            The current beam being processed

        Returns
        -------
        np.ndarray
            The corrected array
        """
        rotated_array = self.basic_corrected_data(beam=beam)
        corrected_array = next(self.corrections_correct_geometry(rotated_array, angle=angle))
        return corrected_array

    def compute_offset(self, array: np.ndarray, beam: int) -> np.ndarray:
        """
        Higher-level helper function to compute the (x, y) offset between beams.

        Sets beam 1 as the reference beam or computes the offset of beam 2 relative to beam 1.

        Parameters
        ----------
        array : np.ndarray
            Beam data
        beam : int
            The current beam being processed

        Returns
        -------
        np.ndarray
            (x, y) offset between beams
        """
        if beam == 1:
            self.reference_array = array
            shift = np.zeros(2)
        else:
            shift = self.compute_beam_offset(
                reference_array=self.reference_array,
                array=array,
                upsample_factor=self.parameters.geo_upsample_factor,
            )
        logger.info(f"Offset for {beam = } is {np.array2string(shift, precision=3)}")
        return shift

    def remove_beam_offset(self, array: np.ndarray, offset: np.ndarray, beam: int) -> None:
        """
        Shift an array by some offset (to make it in line with the reference array).

        Parameters
        ----------
        array : np.ndarray
            Beam data
        offset : np.ndarray
            The beam offset for the current beam
        beam : int
            The current beam being processed

        Returns
        -------
        None

        """
        corrected_array = next(self.corrections_correct_geometry(array, shift=offset))
        self.intermediate_frame_write_arrays(arrays=corrected_array, beam=beam, task="GC_OFFSET")

    def compute_spectral_shifts(self, beam: int) -> np.ndarray:
        """
        Compute the spectral 'curvature'.

        I.e., the spectral shift at each slit position needed to have wavelength be constant across a single spatial
        pixel. Generally, the algorithm is:

         1. Identify the reference array spectrum as the center of the slit
         2. For each slit position, make an initial guess of the shift via correlation
         3. Take the initial guesses and use them in a chisq minimizer to refine the shifts
         4. Interpolate over those shifts identified as too large
         5. Remove the mean shift so the total shift amount is minimized

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        np.ndarray
            Spectral shift for a single beam
        """
        logger.info(f"Computing spectral shifts for beam {beam}")
        beam_array = self.offset_corrected_data(beam=beam)
        spatial_size = beam_array.shape[0]

        self.intermediate_frame_write_arrays(
            arrays=beam_array, beam=beam, task="DEBUG_GC_AVG_OFFSET"
        )

        ref_spec = beam_array[spatial_size // 2, :]
        beam_shifts = np.empty(spatial_size) * np.nan
        for i in range(spatial_size):
            target_spec = beam_array[i, :]

            initial_guess = self._compute_initial_spec_shift_guess(
                ref_spec=ref_spec, target_spec=target_spec, beam=beam, pos=i
            )

            shift = self._compute_single_spec_shift(
                ref_spec=ref_spec,
                target_spec=target_spec,
                initial_guess=initial_guess,
                beam=beam,
                pos=i,
            )

            beam_shifts[i] = shift

        # Subtract the average so we shift my a minimal amount
        beam_shifts -= np.nanmean(beam_shifts)

        # Finally, fit the shifts and return the resulting polynomial. Any "bad" fits were set to NaN and will be
        # interpolated over.
        poly_fit_order = self.parameters.geo_poly_fit_order
        nan_idx = np.isnan(beam_shifts)
        poly = np.poly1d(
            np.polyfit(np.arange(spatial_size)[~nan_idx], beam_shifts[~nan_idx], poly_fit_order)
        )

        return poly(np.arange(spatial_size))

    @staticmethod
    def _compute_initial_spec_shift_guess(
        *, ref_spec: np.ndarray, target_spec: np.ndarray, beam: int, pos: int
    ) -> float:
        """
        Make a rough guess for the offset between two spectra.

        A basic correlation is performed and the location of the peak sets the initial guess. If more than one strong
        peak is found then the peak locations are averaged together.
        """
        corr = np.correlate(
            target_spec - np.nanmean(target_spec),
            ref_spec - np.nanmean(ref_spec),
            mode="same",
        )

        # This min_dist ensures we only find a single peak in each correlation signal
        pidx = pku.indexes(corr, min_dist=corr.size)
        initial_guess = 1 * (pidx - corr.size // 2)

        # These edge-cases are very rare, but do happen sometimes
        if initial_guess.size == 0:
            logger.info(
                f"Spatial position {pos} in {beam=} doesn't have a correlation peak. Initial guess set to 0"
            )
            initial_guess = 0.0

        elif initial_guess.size > 1:
            logger.info(
                f"Spatial position {pos} in {beam=} has more than one correlation peak ({initial_guess}). Initial guess set to mean ({np.nanmean(initial_guess)})"
            )
            initial_guess = np.nanmean(initial_guess)

        return initial_guess

    def _compute_single_spec_shift(
        self,
        *,
        ref_spec: np.ndarray,
        target_spec: np.ndarray,
        initial_guess: float,
        beam: int,
        pos: int,
    ) -> float:
        """
        Refine the 1D offset between two spectra.

        A 1-parameter minimization is performed where the goodness-of-fit parameter is simply the Chisq difference
        between the reference spectrum and shifted target spectrum.
        """
        shift = minimize(
            self.shift_chisq,
            np.array([float(initial_guess)]),
            args=(ref_spec, target_spec),
            method="nelder-mead",
        ).x[0]

        max_shift = self.parameters.geo_max_shift
        if np.abs(shift) > max_shift:
            # Didn't find a good peak, probably because of a hairline
            logger.info(
                f"shift in {beam = } at spatial pixel {pos} out of range ({shift} > {max_shift})"
            )
            shift = np.nan

        return shift

    @staticmethod
    def compute_beam_offset(
        reference_array: np.ndarray,
        array: np.ndarray,
        upsample_factor: float = 10.0,
    ) -> np.ndarray:
        """
        Find the (x, y) shift between the current beam and the reference beam.

        The shift is found by fitting the peak of the correlation of the two beams

        Parameters
        ----------
        reference_array
            The array to use as a reference (the beam 1 array)

        array : np.ndarray
            The array for which the offset is to be computed (the beam 2 array)

        upsample_factor
            The upsample factor used in the cross correlation calculation

        Returns
        -------
        numpy.ndarray
            The (x, y) shift between the reference beam and the current beam at hand
        """
        shift = skir.phase_cross_correlation(
            reference_array,
            array,
            return_error=False,
            upsample_factor=upsample_factor,
            # Need this, because 'phase' blows up
            normalization=None,
        )
        # skir.phase_cross_correlation returns the correction
        # We negate it here to return the measured shift offset
        return -shift

    @staticmethod
    def shift_chisq(par: np.ndarray, ref_spec: np.ndarray, spec: np.ndarray) -> float:
        """
        Goodness of fit calculation for a simple shift. Uses simple chisq as goodness of fit.

        Less robust than SPGainCalibration's `refine_shift`, but much faster.

        Parameters
        ----------
        par : np.ndarray
            Spectral shift being optimized

        ref_spec : np.ndarray
            Reference spectra

        spec : np.ndarray
            Spectra being fitted

        Returns
        -------
        float
            Sum of chisquared fit

        """
        shift = par[0]
        shifted_spec = spnd.shift(spec, -shift, mode="constant", cval=np.nan)
        chisq = np.nansum((ref_spec - shifted_spec) ** 2 / ref_spec)
        return chisq

    def write_angle(self, angle: float, beam: int) -> None:
        """
        Write the angle component of the geometric calibration for a single beam.

        Parameters
        ----------
        angle : float
            The beam angle (radians) for the current beam

        beam : int
            The current beam being processed

        Returns
        -------
        None
        """
        array = np.array([angle])
        self.intermediate_frame_write_arrays(
            arrays=array, beam=beam, task_tag=CryonirspTag.task_geometric_angle()
        )

    def write_beam_offset(self, offset: np.ndarray, beam: int) -> None:
        """
        Write the beam offset component of the geometric calibration for a single beam.

        Parameters
        ----------
        offset : np.ndarray
            The beam offset for the current beam

        beam : int
            The current beam being processed

        Returns
        -------
        None

        """
        self.intermediate_frame_write_arrays(
            arrays=offset, beam=beam, task_tag=CryonirspTag.task_geometric_offset()
        )

    def write_spectral_shifts(self, shifts: np.ndarray, beam: int) -> None:
        """
        Write the spectral shift component of the geometric calibration for a single beam.

        Parameters
        ----------
        shifts : np.ndarray
            The spectral shifts for the current beam

        beam : int
            The current beam being processed

        Returns
        -------
        None

        """
        self.intermediate_frame_write_arrays(
            arrays=shifts, beam=beam, task_tag=CryonirspTag.task_geometric_sepectral_shifts()
        )
