import json
from datetime import datetime

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.tasks.gain import CISolarGainCalibration
from dkist_processing_cryonirsp.tasks.gain import LampGainCalibration
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidLampGainFrames
from dkist_processing_cryonirsp.tests.conftest import generate_fits_frame


@pytest.fixture(scope="function", params=[TaskName.lamp_gain.value, TaskName.solar_gain.value])
def ci_gain_calibration_task(
    tmp_path,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
    init_cryonirsp_constants_db,
    mocker,
    request,
):
    number_of_beams = 1
    dataset_shape = (1, 10, 10)
    array_shape = (1, 10, 10)
    intermediate_shape = (10, 10)
    constants_db = CryonirspConstantsDb(NUM_MODSTATES=1, ARM_ID="CI")
    gain_type = request.param
    if gain_type == TaskName.lamp_gain.value:
        this_task = LampGainCalibration
        exposure_time = constants_db.LAMP_GAIN_EXPOSURE_TIMES[0]
    elif gain_type == TaskName.solar_gain.value:
        this_task = CISolarGainCalibration
        exposure_time = constants_db.SOLAR_GAIN_EXPOSURE_TIMES[0]
    else:
        raise ValueError(f"Unknown CI gain type: {request.param}")
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with this_task(
        recipe_run_id=recipe_run_id, workflow_name="ci_gain_calibration", workflow_version="VX.Y"
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            # Need a beam boundary file
            task.intermediate_frame_write_arrays(
                arrays=np.array([0, intermediate_shape[0], 0, intermediate_shape[1]]),
                task_tag=CryonirspTag.task_beam_boundaries(),
                beam=1,
            )
            # Create fake bad pixel map
            task.intermediate_frame_write_arrays(
                arrays=np.zeros(array_shape[1:]), task_tag=CryonirspTag.task_bad_pixel_map()
            )
            dark_signal = 3.0
            start_time = datetime.now()
            # Make intermediate dark frame
            dark_cal = np.ones(intermediate_shape) * dark_signal
            dark_hdul = fits.HDUList([fits.PrimaryHDU(data=dark_cal)])
            # Need a dark for each beam
            for b in range(number_of_beams):
                task.intermediate_frame_write_arrays(
                    arrays=dark_cal,
                    beam=b + 1,
                    task_tag=CryonirspTag.task_dark(),
                    exposure_time=exposure_time,
                )
            ds = CryonirspHeadersValidLampGainFrames(
                dataset_shape=dataset_shape,
                array_shape=array_shape,
                time_delta=10,
                start_time=start_time,
            )
            header_generator = (
                spec122_validator.validate_and_translate_to_214_l0(
                    d.header(), return_type=fits.HDUList
                )[0].header
                for d in ds
            )
            hdul = generate_fits_frame(
                header_generator=header_generator, shape=array_shape
            )  # Tweak data so that beam sides are slightly different
            # Use data != 1 to check normalization in test
            hdul[0].data.fill(1.1)
            tags = [
                CryonirspTag.linearized(),
                CryonirspTag.task(request.param),
                CryonirspTag.modstate(1),
                CryonirspTag.frame(),
                CryonirspTag.exposure_time(exposure_time),
            ]
            task.write(
                data=hdul,
                tags=tags,
                encoder=fits_hdulist_encoder,
            )
            yield task, number_of_beams, gain_type, exposure_time
        finally:
            task._purge()


@pytest.fixture(scope="function")
def sp_lamp_calibration_task(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_cryonirsp_constants_db, mocker
):
    number_of_beams = 2
    exposure_time = 100.0
    dataset_shape = (1, 10, 20)
    array_shape = (1, 10, 20)
    intermediate_shape = (10, 10)
    constants_db = CryonirspConstantsDb(NUM_MODSTATES=1, ARM_ID="SP")
    gain_type = TaskName.lamp_gain.value
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with LampGainCalibration(
        recipe_run_id=recipe_run_id, workflow_name="sp_gain_calibration", workflow_version="VX.Y"
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            # Need a beam boundary file
            task.intermediate_frame_write_arrays(
                arrays=np.array([0, intermediate_shape[0], 0, intermediate_shape[1]]),
                task_tag=CryonirspTag.task_beam_boundaries(),
                beam=1,
            )
            # Create fake bad pixel map
            task.intermediate_frame_write_arrays(
                arrays=np.zeros(array_shape[1:]), task_tag=CryonirspTag.task_bad_pixel_map()
            )
            dark_signal = 3.0
            start_time = datetime.now()
            # Make intermediate dark frame
            dark_cal = np.ones(intermediate_shape) * dark_signal
            dark_hdul = fits.HDUList([fits.PrimaryHDU(data=dark_cal)])
            # Need a dark for each beam
            for b in range(number_of_beams):
                task.intermediate_frame_write_arrays(
                    arrays=dark_cal,
                    beam=b + 1,
                    task_tag=CryonirspTag.task_dark(),
                    exposure_time=exposure_time,
                )
                # Create fake beam border intermediate arrays
                task.intermediate_frame_write_arrays(
                    arrays=np.array([0, 10, (b * 10), 10 + (b * 10)]),
                    task_tag=CryonirspTag.task_beam_boundaries(),
                    beam=b + 1,
                )

                # does this need to be in the beam loop as well?
                ds = CryonirspHeadersValidLampGainFrames(
                    dataset_shape=dataset_shape,
                    array_shape=array_shape,
                    time_delta=10,
                    start_time=start_time,
                )
                header_generator = (
                    spec122_validator.validate_and_translate_to_214_l0(
                        d.header(), return_type=fits.HDUList
                    )[0].header
                    for d in ds
                )
                hdul = generate_fits_frame(
                    header_generator=header_generator, shape=array_shape
                )  # Tweak data so that beam sides are slightly different
                # Use data != 1 to check normalization in test
                hdul[0].data.fill(1.1)
                tags = [
                    CryonirspTag.beam(b + 1),
                    CryonirspTag.linearized(),
                    CryonirspTag.task(gain_type),
                    CryonirspTag.modstate(1),
                    CryonirspTag.frame(),
                    CryonirspTag.exposure_time(exposure_time),
                ]
                task.write(
                    data=hdul,
                    tags=tags,
                    encoder=fits_hdulist_encoder,
                )
            yield task, number_of_beams
        finally:
            task._purge()


def test_ci_gain_calibration_task(ci_gain_calibration_task, mocker):
    """
    Given: A CILampGainCalibration task
    When: Calling the task instance
    Then: The correct number of output lamp gain frames exists, and are tagged correctly
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task, number_of_beams, gain_type, exposure_time = ci_gain_calibration_task
    task()
    # Then
    tags = [
        CryonirspTag.linearized(),
        CryonirspTag.task(gain_type),
        CryonirspTag.modstate(1),
        CryonirspTag.frame(),
        CryonirspTag.exposure_time(exposure_time),
    ]

    assert len(list(task.read(tags=tags))) == number_of_beams

    for j in range(number_of_beams):
        tags = [
            CryonirspTag.task(gain_type),
            CryonirspTag.intermediate(),
            CryonirspTag.frame(),
            CryonirspTag.beam(j + 1),
        ]
        files = list(task.read(tags=tags))
        assert len(files) == 1
        hdu = fits.open(files[0])[0]
        expected_results = np.ones((10, 10))  # Because lamps are normalized
        np.testing.assert_allclose(hdu.data, expected_results)

    tags = [
        CryonirspTag.task(gain_type),
        CryonirspTag.intermediate(),
    ]
    for filepath in task.read(tags=tags):
        assert filepath.exists()

    quality_files = task.read(tags=[CryonirspTag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[CryonirspTag.linearized(), CryonirspTag.frame(), CryonirspTag.task(gain_type)]
            )


def test_sp_lamp_calibration_task(sp_lamp_calibration_task, mocker):
    """
    Given: A SPLampGainCalibration task
    When: Calling the task instance
    Then: The correct number of output lamp gain frames exists, and are tagged correctly
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task, number_of_beams = sp_lamp_calibration_task
    task()
    # Then
    tags = [
        CryonirspTag.task_lamp_gain(),
        CryonirspTag.intermediate(),
    ]
    assert len(list(task.read(tags=tags))) == number_of_beams

    for j in range(number_of_beams):
        tags = [
            CryonirspTag.task_lamp_gain(),
            CryonirspTag.intermediate(),
            CryonirspTag.modstate(1),
            CryonirspTag.beam(j + 1),
        ]
        files = list(task.read(tags=tags))
        assert len(files) == 1
        hdu = fits.open(files[0])[0]
        expected_results = np.ones((10, 10))  # Because lamps are normalized
        np.testing.assert_allclose(hdu.data, expected_results)

    tags = [
        CryonirspTag.task_lamp_gain(),
        CryonirspTag.intermediate(),
    ]
    for filepath in task.read(tags=tags):
        assert filepath.exists()

    quality_files = task.read(tags=[CryonirspTag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task_lamp_gain(),
                ]
            )
