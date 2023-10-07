"""CryoNIRSP dark calibration task."""
from dkist_processing_math.statistics import average_numpy_arrays
from logging42 import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class DarkCalibration(CryonirspTaskBase):
    """Task class for calculation of the averaged dark frame for a CryoNIRSP calibration run.

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

        - Gather input dark frames
        - Calculate average dark
        - Write average dark
        - Record quality metrics

        Returns
        -------
        None

        """
        target_exp_times = self.constants.non_dark_task_exposure_times

        logger.info(f"{target_exp_times = }")
        with self.apm_task_step(
            f"Calculating dark frames for {self.constants.num_beams} beams and {len(target_exp_times)} exp times"
        ):
            total_dark_frames_used = 0
            for exp_time in target_exp_times:
                for beam in range(1, self.constants.num_beams + 1):
                    logger.info(f"Gathering input dark frames for {exp_time = } and {beam = }")
                    dark_tags = [
                        CryonirspTag.linearized(),
                        CryonirspTag.frame(),
                        CryonirspTag.task_dark(),
                        CryonirspTag.exposure_time(exp_time),
                    ]
                    current_exp_dark_count = self.scratch.count_all(tags=dark_tags)
                    if current_exp_dark_count == 0:
                        raise ValueError(f"Could not find any darks for {exp_time = }")
                    total_dark_frames_used += current_exp_dark_count
                    linearized_dark_arrays = self.linearized_frame_dark_array_generator(
                        exposure_time=exp_time, beam=beam
                    )

                    with self.apm_processing_step(
                        f"Calculating dark for {exp_time = } and {beam = }"
                    ):
                        averaged_dark_array = average_numpy_arrays(linearized_dark_arrays)

                    with self.apm_writing_step(f"Writing dark for {exp_time = } {beam = }"):
                        self.intermediate_frame_write_arrays(
                            averaged_dark_array,
                            beam=beam,
                            task_tag=CryonirspTag.task_dark(),
                            exposure_time=exp_time,
                        )

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_dark_frames: int = self.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task_dark(),
                ],
            )
            unused_count = int(
                no_of_raw_dark_frames - (total_dark_frames_used // self.constants.num_beams)
            )
            self.quality_store_task_type_counts(
                task_type=TaskName.dark.value,
                total_frames=no_of_raw_dark_frames,
                frames_not_used=unused_count,
            )
