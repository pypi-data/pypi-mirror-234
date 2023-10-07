"""Cryo SP science calibration task."""
from collections import defaultdict

import numpy as np
from astropy.io import fits
from dkist_processing_math.statistics import average_numpy_arrays
from logging42 import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess
from dkist_processing_cryonirsp.tasks.science_base import CalibrationCollection
from dkist_processing_cryonirsp.tasks.science_base import ScienceCalibrationBase


class SPScienceCalibration(ScienceCalibrationBase):
    """Task class for SP Cryo science calibration of polarized and non-polarized data."""

    def calibrate_and_write_frames(self, calibrations: CalibrationCollection):
        """
        Top-level method to collect frame groupings (map_scan, scan_step, etc.) and send them to be calibrated.

        Then write the calibrated arrays.

        This is also where the polarimetric/non-polarimetric split is made.
        """
        for exp_time in self.constants.observe_exposure_times:
            for map_scan in range(1, self.constants.num_map_scans + 1):
                for scan_step in range(1, self.constants.num_scan_steps + 1):
                    for meas_num in range(1, self.constants.num_meas + 1):
                        if self.constants.correct_for_polarization:
                            calibrated_object = self.calibrate_polarimetric_beams(
                                exp_time=exp_time,
                                map_scan=map_scan,
                                scan_step=scan_step,
                                meas_num=meas_num,
                                calibrations=calibrations,
                            )
                        else:
                            calibrated_object = self.calibrate_intensity_only_beams(
                                exp_time=exp_time,
                                map_scan=map_scan,
                                scan_step=scan_step,
                                meas_num=meas_num,
                                calibrations=calibrations,
                            )

                        logging_str = (
                            f"{exp_time = }, {map_scan = }, {scan_step = } and {meas_num = }"
                        )
                        logger.info(f"Writing calibrated array for {logging_str}")
                        self.write_calibrated_object(
                            calibrated_object,
                            map_scan=map_scan,
                            scan_step=scan_step,
                            meas_num=meas_num,
                        )

    def calibrate_polarimetric_beams(
        self,
        *,
        exp_time: float,
        map_scan: int,
        scan_step: int,
        meas_num: int,
        calibrations: CalibrationCollection,
    ) -> CryonirspL0FitsAccess:
        """
        Completely calibrate polarimetric science frames.

        - Apply dark and gain corrections
        - Demodulate
        - Apply geometric correction
        - Apply telescope correction
        - Combine beams
        """
        beam_storage = dict()
        header_storage = dict()
        logging_str = f"{exp_time = }, {map_scan = }, {scan_step = }, {meas_num = }"
        for beam in range(1, self.constants.num_beams + 1):
            logger.info(f"Processing polarimetric observe frames from {logging_str} and {beam = }")
            intermediate_array, intermediate_header = self.correct_and_demodulate(
                beam=beam,
                meas_num=meas_num,
                scan_step=scan_step,
                map_scan=map_scan,
                exp_time=exp_time,
                calibrations=calibrations,
            )

            geo_corrected_array = self.apply_geometric_correction(
                array=intermediate_array, beam=beam, calibrations=calibrations
            )

            beam_storage[CryonirspTag.beam(beam)] = geo_corrected_array
            header_storage[CryonirspTag.beam(beam)] = intermediate_header

        logger.info(f"Combining beams for {logging_str}")
        combined = self.combine_beams_into_fits_access(beam_storage, header_storage)

        logger.info(f"Correcting telescope polarization for {logging_str}")
        calibrated = self.telescope_polarization_correction(combined)
        calibrated = self.remove_crosstalk(calibrated)

        return calibrated

    def calibrate_intensity_only_beams(
        self,
        *,
        exp_time: float,
        map_scan: int,
        scan_step: int,
        meas_num: int,
        calibrations: CalibrationCollection,
    ) -> CryonirspL0FitsAccess:
        """
        Completely calibrate non-polarimetric science frames.

        - Apply all dark and gain corrections
        - Apply geometric correction
        - Combine beams
        """
        beam_storage = dict()
        header_storage = dict()
        for beam in range(1, self.constants.num_beams + 1):
            logging_str = f"{exp_time = }, {map_scan = }, {scan_step = }, {meas_num = }"
            logger.info(f"Processing Stokes-I observe frames from {logging_str} and {beam = }")
            intermediate_array, intermediate_header = self.apply_basic_corrections(
                beam=beam,
                modstate=1,
                meas_num=meas_num,
                scan_step=scan_step,
                map_scan=map_scan,
                exp_time=exp_time,
                calibrations=calibrations,
            )
            intermediate_header = self._compute_date_keys(intermediate_header)

            intermediate_array = self._add_stokes_dimension_to_intensity_only_array(
                intermediate_array
            )

            geo_corrected_array = self.apply_geometric_correction(
                array=intermediate_array, beam=beam, calibrations=calibrations
            )

            beam_storage[CryonirspTag.beam(beam)] = geo_corrected_array
            header_storage[CryonirspTag.beam(beam)] = intermediate_header

        logger.info(f"Combining beams for {logging_str}")
        calibrated = self.combine_beams_into_fits_access(beam_storage, header_storage)

        return calibrated

    def apply_geometric_correction(
        self, array: np.ndarray, beam: int, calibrations: CalibrationCollection
    ) -> np.ndarray:
        """
        Apply rotation, x/y shift, and spectral shift corrections to an array.

        The input array needs to have a final dimension that corresponds to Stokes parameters (even if it's only length
        1 for I-only).
        """
        corrected_array = np.zeros_like(array)
        num_stokes = array.shape[-1]

        for i in range(num_stokes):
            geo_corrected_array = next(
                self.corrections_correct_geometry(
                    array[:, :, i],
                    calibrations.state_offset[CryonirspTag.beam(beam)],
                    calibrations.angle[CryonirspTag.beam(beam)],
                )
            )

            spectral_corrected_array = next(
                self.corrections_remove_spec_shifts(
                    geo_corrected_array,
                    calibrations.spec_shift[CryonirspTag.beam(beam)],
                )
            )
            # Insert the result into the fully corrected array stack
            corrected_array[:, :, i] = spectral_corrected_array

        return corrected_array

    def combine_beams_into_fits_access(
        self, array_dict: dict, header_dict: dict
    ) -> CryonirspL0FitsAccess:
        """
        Average all beams together.

        Also complain if the inputs are strange.
        """
        headers = list(header_dict.values())
        if len(headers) == 0:
            raise ValueError("No headers provided")
        for h in headers[1:]:
            if fits.HeaderDiff(headers[0], h):
                raise ValueError("Headers are different! This should NEVER happen!")

        array_list = []
        for beam in range(1, self.constants.num_beams + 1):
            array_list.append(array_dict[CryonirspTag.beam(beam)])

        avg_array = average_numpy_arrays(array_list)

        obj = self._wrap_array_and_header_in_fits_access(avg_array, headers[0])

        return obj

    @staticmethod
    def remove_crosstalk(fits_obj: CryonirspL0FitsAccess) -> CryonirspL0FitsAccess:
        """Remove the continuum from QUV (remove cross-talk)."""
        array_stack = fits_obj.data
        array_header = fits_obj.header
        for i in range(1, 4):
            array_stack[:, :, i] = (
                array_stack[:, :, i]
                - np.nanmedian(array_stack[:, :, i] / array_stack[:, :, 0], axis=1)[:, None]
                * array_stack[:, :, 0]
            )
        hdu = fits.ImageHDU(data=array_stack, header=array_header)
        obj = CryonirspL0FitsAccess(hdu=hdu, auto_squeeze=False)
        return obj

    def collect_calibration_objects(self) -> CalibrationCollection:
        """
        Collect *all* calibration for all modstates, and exposure times.

        Doing this once here prevents lots of reads as we reduce the science data.
        """
        dark_dict = defaultdict(dict)
        solar_dict = dict()
        angle_dict = dict()
        state_offset_dict = dict()
        spec_shift_dict = dict()
        demod_dict = dict() if self.constants.correct_for_polarization else None

        for beam in range(1, self.constants.num_beams + 1):
            # Load the dark arrays
            for exp_time in self.constants.observe_exposure_times:
                dark_array = self.intermediate_frame_load_dark_array(
                    beam=beam, exposure_time=exp_time
                )
                dark_dict[CryonirspTag.beam(beam)][
                    CryonirspTag.exposure_time(exp_time)
                ] = dark_array

            # Load the gain arrays
            solar_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_solar_gain_array(
                beam=beam,
            )

            # Load the angle arrays
            angle_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_angle(beam=beam)

            # Load the state offsets
            state_offset_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_state_offset(
                beam=beam
            )

            # Load the spectral shifts
            spec_shift_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_spec_shift(
                beam=beam
            )

            # Load the demod matrices
            if self.constants.correct_for_polarization:
                demod_dict[CryonirspTag.beam(beam)] = self.intermediate_frame_load_demod_matrices(
                    beam=beam
                )

        return CalibrationCollection(
            dark=dark_dict,
            solar_gain=solar_dict,
            angle=angle_dict,
            state_offset=state_offset_dict,
            spec_shift=spec_shift_dict,
            demod_matrices=demod_dict,
        )
