"""Cryo SP solar gain task."""
import numpy as np
import peakutils
import scipy.ndimage as spnd
import scipy.optimize as spo
import scipy.signal as sps
from dkist_processing_math.arithmetic import divide_arrays_by_array
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from logging42 import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class SPSolarGainCalibration(CryonirspTaskBase):
    """Task class for generating Solar Gain images for each beam/modstate.

    NB: This class does not extend GainCalibrationBase, because it is highly customized
    and incorporates several correction steps as well as solar spectrum removal.

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
        For each beam.

            - Do dark, lamp, and geometric corrections
            - Compute the characteristic spectra
            - Re-apply the spectral curvature to the characteristic spectra
            - Re-apply angle and state offset distortions to the characteristic spectra
            - Remove the distorted characteristic solar spectra from the original spectra
            - Write master solar gain

        Returns
        -------
        None

        """
        target_exposure_times = self.constants.solar_gain_exposure_times

        with self.apm_step(f"Computing SP gain calibrations for {target_exposure_times=}"):
            for exposure_time in target_exposure_times:
                for beam in range(1, self.constants.num_beams + 1):
                    with self.apm_processing_step(
                        f"Initial corrections for {beam = } and {exposure_time = }"
                    ):
                        self.do_initial_corrections(beam=beam, exposure_time=exposure_time)
                    with self.apm_processing_step(
                        f"Computing characteristic spectra for {beam = } and {exposure_time = }"
                    ):
                        char_spec = self.compute_characteristic_spectra(
                            beam=beam, exposure_time=exposure_time
                        )
                        self.intermediate_frame_write_arrays(
                            arrays=char_spec,
                            beam=beam,
                            task="SC_DEBUG_CHAR_SPEC",
                            exposure_time=exposure_time,
                        )

                    with self.apm_processing_step(
                        f"Refining characteristic spectral shifts for {beam = } and {exposure_time = }"
                    ):
                        reshifted_char_spec = self.refine_gain_shifts(
                            char_spec=char_spec,
                            beam=beam,
                            exposure_time=exposure_time,
                        )
                        self.intermediate_frame_write_arrays(
                            arrays=reshifted_char_spec,
                            beam=beam,
                            task="SC_DEBUG_CHAR_SPEC_SHIFT",
                            exposure_time=exposure_time,
                        )
                    with self.apm_processing_step(
                        f"Removing solar signal from {beam = } and {exposure_time = }"
                    ):
                        gain = self.remove_solar_signal(
                            char_solar_spectra=reshifted_char_spec,
                            beam=beam,
                            exposure_time=exposure_time,
                        )
                        self.intermediate_frame_write_arrays(
                            arrays=gain,
                            beam=beam,
                            task="SC_DEBUG_PERFECT_GAIN",
                            exposure_time=exposure_time,
                        )
                    with self.apm_processing_step(
                        f"Reshifting gain spectra for {beam = } and {exposure_time = }"
                    ):
                        spec_shift = self.intermediate_frame_load_spec_shift(beam=beam)
                        reshifted_gain = next(
                            self.corrections_remove_spec_shifts(arrays=gain, spec_shift=-spec_shift)
                        )
                        self.intermediate_frame_write_arrays(
                            arrays=reshifted_gain,
                            beam=beam,
                            task="SC_DEBUG_NEW_GAIN_SPEC_SHIFT",
                            exposure_time=exposure_time,
                        )
                    with self.apm_processing_step(
                        f"Re-distorting characteristic spectra for {beam = } and {exposure_time = }"
                    ):
                        distorted_gain = self.distort_final_gain_array(
                            char_spec=reshifted_gain, beam=beam
                        )
                        self.intermediate_frame_write_arrays(
                            arrays=distorted_gain,
                            beam=beam,
                            task="SC_DEBUG_NEW_GAIN_SHIFT_DISTORT",
                            exposure_time=exposure_time,
                        )

                    with self.apm_writing_step(
                        f"Writing solar gain for {beam = } and {exposure_time = }"
                    ):
                        self.write_solar_gain_calibration(
                            gain_array=distorted_gain,
                            beam=beam,
                            exposure_time=exposure_time,
                        )

            with self.apm_processing_step("Computing and logging quality metrics"):
                no_of_raw_solar_frames: int = self.scratch.count_all(
                    tags=[
                        CryonirspTag.linearized(),
                        CryonirspTag.frame(),
                        CryonirspTag.task_solar_gain(),
                    ],
                )

                self.quality_store_task_type_counts(
                    task_type=TaskName.solar_gain.value, total_frames=no_of_raw_solar_frames
                )

    def geo_corrected_data(self, beam: int, exposure_time: float) -> np.ndarray:
        """
        Array for a single beam that has dark, lamp, and ALL of the geometric corrects.

        Parameters
        ----------
        beam : int
            The beam number for this array

        exposure_time : float
            The exposure time for this array


        Returns
        -------
        np.ndarray
            Array with dark signal, and lamp signal removed, and all geometric corrections made
        """
        array_generator = self.intermediate_frame_load_intermediate_arrays(
            tags=[
                CryonirspTag.task("SC_GEO_ALL"),
                CryonirspTag.beam(beam),
                CryonirspTag.exposure_time(exposure_time),
            ]
        )
        return next(array_generator)

    def unshifted_geo_corrected_data(self, beam: int, exposure_time: float) -> np.ndarray:
        """
        Array for a single beam/modstate that has dark, lamp, angle, and state offset corrections.

        Parameters
        ----------
        beam : int
            The beam number for this array

        exposure_time : float
            The exposure time for this array


        Returns
        -------
        np.ndarray
            Array with dark signal, lamp signal, angle and state offset removed

        """
        array_generator = self.intermediate_frame_load_intermediate_arrays(
            tags=[
                CryonirspTag.task("SC_GEO_NOSHIFT"),
                CryonirspTag.beam(beam),
                CryonirspTag.exposure_time(exposure_time),
            ]
        )
        return next(array_generator)

    def do_initial_corrections(self, beam: int, exposure_time: float) -> None:
        """Do."""
        logger.info(f"Load dark array")
        try:
            dark_array = self.intermediate_frame_load_dark_array(
                beam=beam, exposure_time=exposure_time
            )
        except StopIteration as e:
            raise ValueError(f"No matching dark found for {beam = }, {exposure_time = } s") from e

        logger.info("Load lamp gain array")
        lamp_array = self.intermediate_frame_load_lamp_gain_array(beam=beam)

        logger.info(f"Load input frames for {beam = } with {exposure_time = }")
        linearized_solar_array = self.linearized_frame_gain_array_generator(
            beam=beam, exposure_time=exposure_time, gain_type=TaskName.solar_gain.value
        )

        avg_solar_array = average_numpy_arrays(linearized_solar_array)

        dark_corrected_solar_array = next(subtract_array_from_arrays(avg_solar_array, dark_array))

        bad_pixel_map = self.intermediate_frame_load_bad_pixel_map(beam=beam)
        bad_pixel_corrected_solar_array = self.corrections_correct_bad_pixels(
            dark_corrected_solar_array, bad_pixel_map
        )

        # Save out only-dark-corr objects because these will be used to make the final Solar Gain object
        self.intermediate_frame_write_arrays(
            arrays=bad_pixel_corrected_solar_array,
            beam=beam,
            task="SC_DARK_ONLY",
            exposure_time=exposure_time,
        )

        lamp_corrected_solar_array = next(
            divide_arrays_by_array(bad_pixel_corrected_solar_array, lamp_array)
        )

        angle = self.intermediate_frame_load_angle(beam=beam)
        state_offset = self.intermediate_frame_load_state_offset(beam=beam)
        spec_shift = self.intermediate_frame_load_spec_shift(beam=beam)
        geo_corrected_solar_array = next(
            self.corrections_correct_geometry(lamp_corrected_solar_array, state_offset, -angle)
        )
        # We need unshifted, but geo-corrected arrays for reshifting and normalization
        self.intermediate_frame_write_arrays(
            arrays=geo_corrected_solar_array,
            beam=beam,
            task="SC_GEO_NOSHIFT",
            exposure_time=exposure_time,
        )

        spectral_corrected_solar_array = next(
            self.corrections_remove_spec_shifts(geo_corrected_solar_array, spec_shift)
        )

        self.intermediate_frame_write_arrays(
            arrays=spectral_corrected_solar_array,
            beam=beam,
            task="SC_GEO_ALL",
            exposure_time=exposure_time,
        )

    def compute_characteristic_spectra(self, beam: int, exposure_time: float) -> np.ndarray:
        """
        Compute the characteristic spectra via a moving average along the slit, identify and ignore hairlines.

        Parameters
        ----------
        beam : int
            The beam number for this array

        exposure_time : float
            The exposure time for this array


        Returns
        -------
        np.ndarray
            Characteristic spectra array
        """
        spectral_avg_window = self.parameters.solar_spectral_avg_window
        logger.info(f"Computing characteristic spectra for {beam=} using {spectral_avg_window=}")
        full_spectra = self.geo_corrected_data(beam=beam, exposure_time=exposure_time)

        char_spec = spnd.gaussian_filter1d(full_spectra, spectral_avg_window, axis=0)

        return char_spec

    def refine_gain_shifts(
        self, char_spec: np.ndarray, beam: int, exposure_time: float
    ) -> np.ndarray:
        """
        Refine the spectral shifts when matching characteristic spectra to the rectified input spectra.

        An important detail of this function is that the goodness of fit metric is the final gain image (i.e., raw
        input with solar spectrum removed). We minimize the residuals in the gain image.

        Parameters
        ----------
        char_spec : np.ndarray
            Computed characteristic spectra

        beam : int
            The beam number for this array

        exposure_time : float
            The exposure time for this array


        Returns
        -------
        np.ndarray
            Characteristic spectra array with refined spectral shifts
        """
        # Grab initial guesses
        spec_shifts = self.intermediate_frame_load_spec_shift(beam=beam)
        num_spec = spec_shifts.size

        # Grab initially shifted spectra that will be the shift target
        target_spectra = self.geo_corrected_data(beam=beam, exposure_time=exposure_time)

        logger.info(f"Computing line zones for {beam=}")
        zone_kwargs = {
            "prominence": self.parameters.solar_zone_prominence,
            "width": self.parameters.solar_zone_width,
            "bg_order": self.parameters.solar_zone_bg_order,
            "normalization_percentile": self.parameters.solar_zone_normalization_percentile,
            "rel_height": self.parameters.solar_zone_rel_height,
        }
        zones = self.compute_line_zones(char_spec, **zone_kwargs)
        logger.info(f"Found {zones=} for {beam=} and {exposure_time=}")
        if len(zones) == 0:
            raise ValueError(f"No zones found for {beam=} and {exposure_time=}")

        reshift_char_spec = np.zeros(char_spec.shape)
        logger.info(f"Fitting reshifts for {beam=}")
        for i in range(num_spec):
            ref_spec = target_spectra[i, :]
            spec = char_spec[i, :]
            shift = SPSolarGainCalibration.refine_shift(
                spec,
                ref_spec,
                zones=zones,
                x_init=0.0,
            )
            reshift_char_spec[i, :] = spnd.shift(char_spec[i, :], shift, mode="reflect")

        logger.info(f"Normalizing spectra for {beam=} and {exposure_time=}")
        raw_meds = np.nanmedian(target_spectra, axis=1)
        char_meds = np.nanmedian(reshift_char_spec, axis=1)
        reshift_char_spec *= (raw_meds / char_meds)[:, None]

        return reshift_char_spec

    def remove_solar_signal(
        self, char_solar_spectra: np.ndarray, beam: int, exposure_time: float
    ) -> np.ndarray:
        """
        Remove the distorted characteristic solar spectra from the original spectra.

        Parameters
        ----------
        char_solar_spectra : np.ndarray
            Characteristic solar spectra

        beam : int
            The beam number for this array

        exposure_time : float
            The exposure time for this array


        Returns
        -------
        np.ndarray
            Original spectral array with characteristic solar spectra removed

        """
        logger.info(f"Removing characteristic solar spectra from {beam=} and {exposure_time=}")
        input_gain = self.geo_corrected_data(beam=beam, exposure_time=exposure_time)

        final_gain = input_gain / char_solar_spectra

        return final_gain

    def distort_final_gain_array(self, char_spec: np.ndarray, beam: int) -> np.ndarray:
        """
        Re-apply angle and state offset distortions to the characteristic spectra.

        Parameters
        ----------
        char_spec : np.ndarray
            Computed characteristic spectra


        Returns
        -------
        np.ndarray
            Characteristic spectra array with angle and offset distortions re-applied
        """
        logger.info("Re-distorting characteristic spectra")
        angle = self.intermediate_frame_load_angle(beam=beam)
        state_offset = self.intermediate_frame_load_state_offset(beam=beam)

        distorted_spec = next(
            self.corrections_correct_geometry(char_spec, -1 * state_offset, -1 * angle)
        )

        return distorted_spec

    def write_solar_gain_calibration(
        self, gain_array: np.ndarray, beam: int, exposure_time: float
    ) -> None:
        """
        Write a solar gain array for a single beam.

        Parameters
        ----------
        gain_array: np.ndarray
            Solar gain array

        beam : int
            The beam number for this array

        exposure_time : float
            The exposure time for this array


        Returns
        -------
        None
        """
        logger.info(f"Writing final SolarGain for {beam=}")
        self.intermediate_frame_write_arrays(
            arrays=gain_array,
            beam=beam,
            task_tag=CryonirspTag.task_solar_gain(),
            exposure_time=exposure_time,
        )

        # These lines are here to help debugging and can be removed if really necessary
        filename = next(
            self.read(
                tags=[
                    CryonirspTag.intermediate(),
                    CryonirspTag.beam(beam),
                    CryonirspTag.task_solar_gain(),
                    CryonirspTag.exposure_time(exposure_time),
                ]
            )
        )
        logger.info(f"Wrote solar gain for {beam=} and {exposure_time=} to {filename}")

    @staticmethod
    def compute_line_zones(
        spec_2d: np.ndarray,
        prominence: float = 0.2,
        width: float = 2,
        bg_order: int = 22,
        normalization_percentile: int = 99,
        rel_height: float = 0.97,
    ) -> list[tuple[int, int]]:
        """
        Identify spectral regions around strong spectra features.

        Parameters
        ----------
        spec_2d : np.ndarray
            Data

        prominence : float
            Zone prominence threshold used to identify strong spectral features

        width : float
            Zone width

        bg_order : int
            Order of polynomial fit used to remove continuum when identifying strong spectral features

        normalization_percentile : int
            Compute this percentile of the data along a specified axis

        rel_height
            The relative peak height at which the peak width is computed. 1.0 is the lowest contour, i.e., larger
            values produce larger widths.

        Returns
        -------
        List
            List of regions to remove

        """
        logger.info(
            f"Finding zones using {prominence=}, {width=}, {bg_order=}, {normalization_percentile=}, and {rel_height=}"
        )
        # Compute average along slit to improve signal. Line smearing isn't important here
        avg_1d = np.mean(spec_2d, axis=0)

        # Convert to an emission spectrum and remove baseline continuum so peakutils has an easier time
        em_spec = -1 * avg_1d + avg_1d.max()
        em_spec /= np.nanpercentile(em_spec, normalization_percentile)
        baseline = peakutils.baseline(em_spec, bg_order)
        em_spec -= baseline

        # Find indices of peaks
        peak_idxs = sps.find_peaks(em_spec, prominence=prominence, width=width)[0]

        # Find the rough width based only on the height of the peak
        #  rips and lips are the right and left borders of the region around the peak
        _, _, rips, lips = sps.peak_widths(em_spec, peak_idxs, rel_height=rel_height)

        # Convert to ints so they can be used as indices
        rips = np.floor(rips).astype(int)
        lips = np.ceil(lips).astype(int)

        # Remove any regions that are contained within another region
        ranges_to_remove = SPSolarGainCalibration.identify_overlapping_zones(rips, lips)
        rips = np.delete(rips, ranges_to_remove)
        lips = np.delete(lips, ranges_to_remove)

        return list(zip(rips, lips))

    @staticmethod
    def identify_overlapping_zones(rips: np.ndarray, lips: np.ndarray) -> list[int]:
        """
        Identify line zones that overlap with other zones. Any overlap greater than 1 pixel is flagged.

        Parameters
        ----------
        rips : np.ndarray
            Right borders of the region around the peak

        lips : np.ndarray
            Left borders of the region around the peak

        Returns
        -------
        List
            List of range indexes to be removed
        """
        all_ranges = [np.arange(zmin, zmax) for zmin, zmax in zip(rips, lips)]
        range_indexes_to_remove = []
        for target_range_idx, target_range in enumerate(all_ranges):
            for compare_range_idx, compare_range in enumerate(all_ranges[target_range_idx + 1 :]):
                all_ranges_compare_idx = compare_range_idx + target_range_idx + 1
                compare_range_intersects_target_range = (
                    np.intersect1d(target_range, compare_range).size > 1
                )
                if compare_range_intersects_target_range:
                    target_range_is_bigger = target_range.size > compare_range.size
                    if target_range_is_bigger:
                        range_indexes_to_remove.append(all_ranges_compare_idx)
                        logger.info(
                            f"Zone ({compare_range[0]}, {compare_range[-1]}) inside "
                            f"zone ({target_range[0]}, {target_range[-1]})"
                        )
                    else:
                        range_indexes_to_remove.append(target_range_idx)
                        logger.info(
                            f"Zone ({target_range[0]}, {target_range[-1]}) inside "
                            f"zone ({compare_range[0]}, {compare_range[-1]})"
                        )
        return range_indexes_to_remove

    @staticmethod
    def refine_shift(
        spec: np.ndarray, target_spec: np.ndarray, zones: list[tuple[int, int]], x_init: float
    ) -> float:
        """
        Compute the shift for a single spatial position back from rectified spectra to the original (curved) position.

        Line zones are used to increase the SNR of the chisq and the final shift is the mean of the shifts computed
        for each zone.

        Parameters
        ----------
        spec : np.ndarray
            The 1D spectrum to shift back

        target_spec : np.ndarray
            The reference spectrum. This should be the un-shifted, raw spectrum at the same position as `spec`

        zones : List
            List of zone borders (in px coords)

        x_init: float
            Initial guess for the shift. This is used to shift the zones so it needs to be pretty good, but not perfect.

        Returns
        -------
        float
            The shift value
        """
        shifts = np.zeros(len(zones))
        for i, z in enumerate(zones):
            if z[1] + int(x_init) >= spec.size:
                logger.info(f"Ignoring zone {z} with init {x_init} because it's out of range")
                continue
            idx = np.arange(z[0], z[1]) + int(x_init)
            shift = spo.minimize(
                SPSolarGainCalibration.shift_func,
                np.array([x_init]),
                args=(target_spec, spec, idx),
                method="nelder-mead",
            ).x[0]
            shifts[i] = shift

        return np.mean(shifts)

    @staticmethod
    def shift_func(
        par: list[float], ref_spec: np.ndarray, spec: np.ndarray, idx: np.ndarray
    ) -> float:
        """
        Non-chisq based goodness of fit calculator for computing spectral shifts.

        Instead of chisq, the metric approximates the final Gain image.

        Parameters
        ----------
        par : List
            List of parameters for minimization

        ref_spec : np.ndarray
            Reference spectra

        spec : np.ndarray
            Data

        idx : np.ndarray
            Range of wavelength pixels that will be compared in fit

        Returns
        -------
        float
            Goodness of fit metric

        """
        shift = par[0]
        shifted_spec = spnd.shift(spec, shift, mode="constant", cval=np.nan)
        final_gain = (ref_spec / shifted_spec)[idx]
        slope = (final_gain[-1] - final_gain[0]) / final_gain.size
        bg = slope * np.arange(final_gain.size) + final_gain[0]
        subbed_gain = np.abs(final_gain - bg)
        fit_metric = np.nansum(subbed_gain[np.isfinite(subbed_gain)])
        return fit_metric
