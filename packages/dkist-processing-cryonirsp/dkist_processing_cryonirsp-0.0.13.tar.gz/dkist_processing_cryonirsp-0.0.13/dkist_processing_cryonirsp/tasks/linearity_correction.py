"""CryoNIRSP Linearity COrrection Task."""
import sys
from dataclasses import dataclass
from typing import Generator

import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_access_decoder
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin
from dkist_service_configuration import logger
from numba import njit
from numba import prange

from dkist_processing_cryonirsp.models.constants import CryonirspConstants
from dkist_processing_cryonirsp.models.parameters import CryonirspParameters
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspRampFitsAccess


@dataclass
class _RampSet:
    current_ramp_set_num: int
    total_ramp_sets: int
    time_obs: str
    frames_in_ramp: int

    @property
    def is_valid(self):
        return self.frames_in_ramp > 1


class LinearityCorrection(WorkflowTaskBase, InputDatasetMixin):
    """Task class for performing linearity correction on all input frames, regardless of task type."""

    constants: CryonirspConstants

    record_provenance = True

    @property
    def constants_model_class(self):
        """Get CryoNIRSP pipeline constants."""
        return CryonirspConstants

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        self.parameters = CryonirspParameters(
            self.input_dataset_parameters, arm_id=self.constants.arm_id
        )
        self.current_ramp_number = None

    def run(self):
        """Run method for this task.

        Steps to be performed:
            - Iterate through frames by ramp set (identified by date-obs)
                - Gather frame(s) in ramp set
                - Perform linearity correction for frame(s)
                - Collate tags for linearity corrected frame(s)
                - Write linearity corrected frame with updated tags

        Returns
        -------
        None
        """
        for ramp_set in self._identify_ramp_sets():
            with self.apm_task_step(
                f"Processing frames from {ramp_set.time_obs}: ramp set {ramp_set.current_ramp_set_num} of {ramp_set.total_ramp_sets}"
            ):
                self.current_ramp_number = ramp_set.current_ramp_set_num
                ramp_objs = self._gather_inputs_for_ramp_set(ramp_set=ramp_set)
                output_array = self._reduce_ramp_set(
                    ramp_objs=ramp_objs,
                    mode="LookUpTable",
                    camera_readout_mode=self.constants.camera_readout_mode,
                    lin_curve=self.parameters.linearization_polyfit_coeffs,
                    thresholds=self.parameters.linearization_thresholds,
                )
                header, tags = self._generate_output_array_metadata(input_ramp_frame=ramp_objs[-1])
                hdul = fits.HDUList([fits.PrimaryHDU(header=header, data=output_array)])
                self.write(
                    data=hdul,
                    tags=tags,
                    encoder=fits_hdulist_encoder,
                )

    def _identify_ramp_sets(self) -> Generator[_RampSet, None, None]:
        """
        Identify the ramp sets that will be corrected together.

        A ramp is defined as all the files with the same DATE-OBS value.
        The ramp number is not a unique identifier when frames from different subtask
        types are combined in a single scratch dir.

        Returns
        -------
        Generator which yields _RampSet instances
        """
        total_ramp_sets = len(self.constants.time_obs_list)

        for idx, time_obs in enumerate(self.constants.time_obs_list):
            frames_in_ramp = len(list(self.read(CryonirspTag.time_obs(time_obs))))
            ramp_set_num = idx + 1
            ramp_set = _RampSet(
                current_ramp_set_num=ramp_set_num,
                total_ramp_sets=total_ramp_sets,
                time_obs=time_obs,
                frames_in_ramp=frames_in_ramp,
            )
            if ramp_set.is_valid:
                yield ramp_set
            else:
                logger.info(f"Ramp set {ramp_set!r} skipped.")

    def _gather_inputs_for_ramp_set(self, ramp_set: _RampSet) -> list[CryonirspRampFitsAccess]:
        """
        Gather a sorted list of frames for a ramp set where a single time-obs should correspond to a single ramp.

        Parameters
        ----------
        ramp_set
            The common metadata (timestamp) for all frames in the series (ramp)

        Returns
        -------
        None

        """
        ramp_set_tags = [
            CryonirspTag.input(),
            CryonirspTag.frame(),
            CryonirspTag.time_obs(ramp_set.time_obs),
        ]
        inputs_for_ramp_set = self.read(
            tags=ramp_set_tags,
            decoder=fits_access_decoder,
            fits_access_class=CryonirspRampFitsAccess,
        )
        return sorted(inputs_for_ramp_set, key=lambda x: x.curr_frame_in_ramp)

    def _generate_output_array_metadata(
        self, input_ramp_frame: CryonirspRampFitsAccess
    ) -> tuple[fits.HDUList, list[Tag]]:
        """
        Use one of the input frames as the basis for the output array's metadata.

        Parameters
        ----------
        input_ramp_frame
            Input frame to use as the basis for the output array's metadata

        Returns
        -------
        Tuple of the header and tags to use for writing the output frame
        """
        result_tags = list(self.scratch.tags(input_ramp_frame.name))
        result_tags.remove(CryonirspTag.input())
        result_tags.remove(CryonirspTag.curr_frame_in_ramp(input_ramp_frame.curr_frame_in_ramp))
        result_tags.append(CryonirspTag.linearized())
        return input_ramp_frame.header, result_tags

    # The methods below are derived versions of the same codes in Tom Schad's h2rg.py
    @staticmethod
    @njit(parallel=False)
    def _lin_correct(raw_data: np.ndarray, linc: np.ndarray) -> np.ndarray:
        """Perform the linearity fit."""
        return raw_data / (
            linc[0] + raw_data * (linc[1] + raw_data * (linc[2] + raw_data * linc[3]))
        )

    @staticmethod
    @njit(parallel=False)
    def _get_slopes(exptimes: np.ndarray, data: np.ndarray, thresholds: np.ndarray):
        """Compute the slopes."""
        num_x, num_y, num_ramps = data.shape
        num_pix = num_x * num_y
        slopes = np.zeros(num_pix)
        raveled_data = data.reshape((num_pix, num_ramps))
        raveled_thresholds = thresholds.ravel()

        for i in prange(num_pix):
            px_data = raveled_data[i, :]
            weights = np.sqrt(px_data)
            weights[px_data > raveled_thresholds[i]] = 0.0

            # If there are more than 2 NDRs that are below the threshold
            if np.sum(weights > 0) >= 2:
                weight_sum = np.sum(weights)

                exp_time_weighted_mean = np.dot(weights, exptimes) / weight_sum
                px_data_weighted_mean = np.dot(weights, px_data) / weight_sum

                corrected_exp_times = exptimes - exp_time_weighted_mean
                corrected_px_data = px_data - px_data_weighted_mean

                weighted_exp_times = weights * corrected_exp_times
                slopes[i] = np.dot(weighted_exp_times, corrected_px_data) / np.dot(
                    weighted_exp_times, corrected_exp_times
                )

        return slopes.reshape((num_x, num_y))

    def _reduce_ramp_set_for_lookup_table_and_fast_up_the_ramp(
        self,
        ramp_objs: list[CryonirspRampFitsAccess],
        lin_curve: np.ndarray = None,
        thresholds: np.ndarray = None,
    ) -> np.ndarray:
        """Process a single ramp from a set of input frames whose mode is 'LookUpTable' and camera readout mode is 'FastUpTheRamp'."""
        # drop first frame in FastUpTheRamp
        ramp_objs = ramp_objs[1:]
        exptimes = np.array([obj.fpa_exposure_time_ms for obj in ramp_objs]).astype(np.float32)

        # Create a 3D stack of the ramp frames that has shape (x, y, num_ramps)
        raw_data = np.zeros((ramp_objs[0].data.shape + (len(ramp_objs),)), dtype=np.float32)
        logger.info(
            f"Size of ramp data cube for ramp {self.current_ramp_number} is {sys.getsizeof(raw_data)} bytes"
        )
        for n, obj in enumerate(ramp_objs):
            raw_data[:, :, n] = obj.data

        # support for single hardware ROI
        # NB: The threshold table is originally constructed for the full sensor size (2k x 2k)
        #     The code below extracts the portion of the thresholds that map to the actual
        #     data size from the camera
        roi_1_origin_x = self.constants.roi_1_origin_x
        roi_1_origin_y = self.constants.roi_1_origin_y
        roi_1_size_x = self.constants.roi_1_size_x
        roi_1_size_y = self.constants.roi_1_size_y
        thres_roi = thresholds[
            roi_1_origin_y : (roi_1_origin_y + roi_1_size_y),
            roi_1_origin_x : (roi_1_origin_x + roi_1_size_x),
        ]
        # correct the whole data first using the curve derived from the on Sun data
        raw_data = self._lin_correct_by_row(raw_data, lin_curve)
        slopes = self._get_slopes(exptimes, raw_data, thres_roi)
        # Scale the slopes by the exposure time to convert to counts
        processed_frame = slopes * np.nanmax(exptimes)

        return processed_frame

    def _reduce_ramp_set(
        self,
        ramp_objs: list[CryonirspRampFitsAccess],
        mode: str = None,
        camera_readout_mode: str = None,
        lin_curve: np.ndarray = None,
        thresholds: np.ndarray = None,
    ) -> np.ndarray:
        """
        Process a single ramp from a set of input frames.

        mode:
        Parameters
        ----------
        ramp_objs
            List of input frames from a common ramp set

        mode
            'LookUpTable','FastCDS','FitUpTheRamp' (ignored if data is line by line)

        camera_readout_mode
            ‘FastUpTheRamp, ‘SlowUpTheRamp’, or 'LineByLine’

        lin_curve
            TODO

        thresholds
            TODO

        Returns
        -------
        processed array
        """
        if mode == "LookUpTable" and camera_readout_mode == "FastUpTheRamp":
            return self._reduce_ramp_set_for_lookup_table_and_fast_up_the_ramp(
                ramp_objs=ramp_objs,
                lin_curve=lin_curve,
                thresholds=thresholds,
            )
        raise ValueError(
            f"Linearization mode {mode} and camera readout mode {camera_readout_mode} is currently not supported."
        )

    def _lin_correct_by_row(self, raw_data: np.ndarray, linc: np.ndarray) -> np.ndarray:
        """
        Perform linearity correction on the data cube one row at a time.

        The cube of cryonirsp ramp data can be very large (2k x 2k x 100+ elements) and so to
        better constrain memory only one row-based-slice of the cube is corrected at any given time.
        :return:
        """
        for j in range(raw_data.shape[0]):
            raw_data[j, :] = self._lin_correct(raw_data[j, :], linc)
        return raw_data
