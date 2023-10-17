import json

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.dark import DarkCalibration
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidDarkFrames
from dkist_processing_cryonirsp.tests.conftest import generate_fits_frame

# from dkist_processing_common.models.tags import Tag


@pytest.fixture(scope="function")
def sp_dark_calibration_task(
    tmp_path, assign_input_dataset_doc_to_task, init_cryonirsp_constants_db, recipe_run_id
):
    constants_db = CryonirspConstantsDb(
        LAMP_GAIN_EXPOSURE_TIMES=(100.0,),
        SOLAR_GAIN_EXPOSURE_TIMES=(1.0,),
        OBSERVE_EXPOSURE_TIMES=(0.01,),
        POLCAL_EXPOSURE_TIMES=(),
        ARM_ID="SP",
    )
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with DarkCalibration(
        recipe_run_id=recipe_run_id, workflow_name="dark_calibration", workflow_version="VX.Y"
    ) as task:
        beam_boundary_spacing = (6, 4)
        num_beams = 2
        exp_times = [1.0, 100.0, 0.01]
        unused_time = 200.0
        num_exp_time = len(exp_times)
        num_frames_per = 3
        array_shape = (1, 10, 20)
        dataset_shape = ((num_exp_time + 1) * num_frames_per, 20, 10)
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())

            # Create fake beam border intermediate arrays
            for beam in range(1, num_beams + 1):
                task.intermediate_frame_write_arrays(
                    arrays=np.array([3, 9, 5 + ((beam - 1) * 10), 9 + ((beam - 1) * 10)]),
                    task_tag=CryonirspTag.task_beam_boundaries(),
                    beam=beam,
                )

            # beam_border = task.parameters.beam_border
            ds = CryonirspHeadersValidDarkFrames(
                dataset_shape=dataset_shape,
                array_shape=array_shape,
                time_delta=10,
            )
            header_generator = (
                spec122_validator.validate_and_translate_to_214_l0(
                    d.header(), return_type=fits.HDUList
                )[0].header
                for d in ds
            )

            for e in exp_times + [unused_time]:  # Make some darks we won't use
                for _ in range(num_frames_per):
                    hdul = generate_fits_frame(header_generator=header_generator, shape=array_shape)
                    # hdul[0].data *= 0
                    # data are 1s to start...
                    hdul[0].data.fill(e)
                    # Create combined 2-beam array
                    # beam = 1
                    # hdul[0].data[0, :beam_border, :] = beam * e
                    # beam = 2
                    # hdul[0].data[0, beam_border:, :] = beam * e
                    task.write(
                        data=hdul,
                        tags=[
                            CryonirspTag.linearized(),
                            CryonirspTag.frame(),
                            CryonirspTag.task_dark(),
                            CryonirspTag.exposure_time(e),
                        ],
                        encoder=fits_hdulist_encoder,
                    )
            yield task, num_beams, exp_times, unused_time, beam_boundary_spacing
        finally:
            task._purge()


@pytest.fixture(scope="function")
def ci_dark_calibration_task(
    tmp_path, assign_input_dataset_doc_to_task, init_cryonirsp_constants_db, recipe_run_id
):
    constants_db = CryonirspConstantsDb(
        LAMP_GAIN_EXPOSURE_TIMES=(100.0,),
        SOLAR_GAIN_EXPOSURE_TIMES=(1.0,),
        OBSERVE_EXPOSURE_TIMES=(0.01,),
        POLCAL_EXPOSURE_TIMES=(),
        ARM_ID="CI",
    )
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with DarkCalibration(
        recipe_run_id=recipe_run_id, workflow_name="dark_calibration", workflow_version="VX.Y"
    ) as task:
        exp_times = [1.0, 100.0, 0.01]
        unused_time = 200.0
        num_exp_time = len(exp_times)
        num_frames_per = 3
        array_shape = (1, 10, 10)
        dataset_shape = ((num_exp_time + 1) * num_frames_per, 20, 10)
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            # Need a beam boundary file
            task.intermediate_frame_write_arrays(
                arrays=np.array([0, 10, 0, 10]),
                task_tag=CryonirspTag.task_beam_boundaries(),
                beam=1,
            )

            ds = CryonirspHeadersValidDarkFrames(
                dataset_shape=dataset_shape,
                array_shape=array_shape,
                time_delta=10,
            )
            header_generator = (
                spec122_validator.validate_and_translate_to_214_l0(
                    d.header(), return_type=fits.HDUList
                )[0].header
                for d in ds
            )
            for e in exp_times + [unused_time]:  # Make some darks we won't use
                for _ in range(num_frames_per):
                    hdul = generate_fits_frame(header_generator=header_generator, shape=array_shape)
                    # data are 1s to start...
                    hdul[0].data.fill(e)
                    task.write(
                        data=hdul,
                        tags=[
                            CryonirspTag.linearized(),
                            CryonirspTag.frame(),
                            CryonirspTag.task_dark(),
                            CryonirspTag.exposure_time(e),
                        ],
                        encoder=fits_hdulist_encoder,
                    )
            yield task, exp_times, unused_time
        finally:
            task._purge()


def test_sp_dark_calibration_task(sp_dark_calibration_task, mocker):
    """
    Given: A DarkCalibration task with multiple task exposure times
    When: Calling the task instance
    Then: Only one average intermediate dark frame exists for each exposure time and unused times are not made
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task, num_beams, exp_times, unused_time, beam_boundary_spacing = sp_dark_calibration_task
    task()
    # Then
    for e in exp_times:
        for b in range(num_beams):
            files = list(
                task.read(
                    tags=[
                        CryonirspTag.task_dark(),
                        CryonirspTag.intermediate(),
                        CryonirspTag.frame(),
                        CryonirspTag.beam(b + 1),
                        CryonirspTag.exposure_time(e),
                    ]
                )
            )
            assert len(files) == 1
            expected = np.ones(beam_boundary_spacing) * e
            hdul = fits.open(files[0])
            np.testing.assert_equal(expected, hdul[0].data)
            hdul.close()

    unused_time_read = task.read(
        tags=[
            CryonirspTag.task_dark(),
            CryonirspTag.intermediate(),
            CryonirspTag.frame(),
            CryonirspTag.exposure_time(unused_time),
        ]
    )
    assert len(list(unused_time_read)) == 0

    quality_files = task.read(tags=[CryonirspTag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[CryonirspTag.linearized(), CryonirspTag.frame(), CryonirspTag.task_dark()]
            )
            assert data["frames_not_used"] == 3


def test_ci_dark_calibration_task(ci_dark_calibration_task, mocker):
    """
    Given: A DarkCalibration task with multiple task exposure times
    When: Calling the task instance
    Then: Only one average intermediate dark frame exists for each exposure time and unused times are not made
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task, exp_times, unused_time = ci_dark_calibration_task
    task()
    # Then
    for e in exp_times:
        files = list(
            task.read(
                tags=[
                    CryonirspTag.task_dark(),
                    # CryonirspTag.linearized(),
                    CryonirspTag.beam(1),
                    CryonirspTag.intermediate(),
                    CryonirspTag.frame(),
                    CryonirspTag.exposure_time(e),
                ]
            )
        )
        assert len(files) == 1
        expected = np.ones((10, 10)) * e
        hdul = fits.open(files[0])
        np.testing.assert_equal(expected, hdul[0].data)
        hdul.close()

    unused_time_read = task.read(
        tags=[
            CryonirspTag.task_dark(),
            CryonirspTag.intermediate(),
            CryonirspTag.frame(),
            CryonirspTag.exposure_time(unused_time),
        ]
    )
    assert len(list(unused_time_read)) == 0

    quality_files = task.read(tags=[CryonirspTag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[CryonirspTag.linearized(), CryonirspTag.frame(), CryonirspTag.task_dark()]
            )
            assert data["frames_not_used"] == 3
