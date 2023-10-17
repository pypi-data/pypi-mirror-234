import json

import numpy as np
import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tests.conftest import FakeGQLClient
from dkist_processing_math import transform

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.sp_geometric import SPGeometricCalibration
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidSPSolarGainFrames
from dkist_processing_cryonirsp.tests.conftest import generate_214_l0_fits_frame


@pytest.fixture(scope="function")
def geometric_calibration_task_that_completes(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_cryonirsp_constants_db
):
    # This fixture makes data that look enough like real data that all of the feature detection stuff at least runs
    # through (mostly this is an issue for the angle calculation). It would be great to contrive data that
    # produce a geometric calibration with real numbers that can be checked, but for now we'll rely on the grogu
    # tests for that. In other words, this fixture just tests if the machinery of the task completes and some object
    # (ANY object) is written correctly.
    number_of_modstates = 1
    number_of_beams = 2
    exposure_time = 20.0  # From CryonirspHeadersValidSolarGainFrames fixture
    intermediate_shape = (30, 30)
    array_shape = (1, 30, 60)
    dataset_shape = array_shape
    constants_db = CryonirspConstantsDb(
        NUM_MODSTATES=number_of_modstates, SOLAR_GAIN_EXPOSURE_TIMES=(exposure_time,), ARM_ID="SP"
    )
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPGeometricCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="sp_geometric_calibration",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            task.angles = np.array([0.0, 0.0])
            task.offsets = np.zeros((number_of_beams, 2))
            task.shifts = np.zeros(intermediate_shape[0])
            # Create fake bad pixel map
            task.intermediate_frame_write_arrays(
                arrays=np.zeros(array_shape[1:]),
                task_tag=CryonirspTag.task_bad_pixel_map(),
            )
            for beam in range(1, number_of_beams + 1):
                dark_cal = np.ones(intermediate_shape) * 3.0
                task.intermediate_frame_write_arrays(
                    arrays=dark_cal,
                    beam=beam,
                    task_tag=CryonirspTag.task_dark(),
                    exposure_time=exposure_time,
                )

                # Need a lamp for each beam
                lamp_gain = np.ones(intermediate_shape)
                task.intermediate_frame_write_arrays(
                    arrays=lamp_gain,
                    beam=beam,
                    task_tag=CryonirspTag.task_lamp_gain(),
                    exposure_time=exposure_time,
                )

                # And a beam border intermediate array
                task.intermediate_frame_write_arrays(
                    arrays=np.array([0, 30, ((beam - 1) * 30), (30 + (beam - 1) * 30)]),
                    task_tag=CryonirspTag.task_beam_boundaries(),
                    beam=beam,
                )

                ds = CryonirspHeadersValidSPSolarGainFrames(
                    dataset_shape=dataset_shape,
                    array_shape=array_shape,
                    time_delta=10,
                )
                header = ds.header()
                true_solar = 10 * (np.ones(array_shape[1:]) + beam)
                translated = next(
                    transform.translate_arrays(
                        arrays=true_solar, translation=task.offsets[beam - 1]
                    )
                )
                translated[translated == 0] = 10 * (beam + 1)
                translated[10, :] = 5.0
                distorted_solar = next(
                    transform.rotate_arrays_about_point(
                        arrays=translated, angle=task.angles[beam - 1]
                    )
                )
                raw_dark = np.concatenate((dark_cal, dark_cal), axis=1)
                raw_solar = distorted_solar + raw_dark
                solar_hdul = generate_214_l0_fits_frame(data=raw_solar, s122_header=header)
                task.write(
                    data=solar_hdul,
                    tags=[
                        CryonirspTag.linearized(),
                        CryonirspTag.task_solar_gain(),
                        CryonirspTag.frame(),
                        CryonirspTag.beam(beam),
                        CryonirspTag.exposure_time(exposure_time),
                    ],
                    encoder=fits_hdulist_encoder,
                )

            yield task
        finally:
            task._purge()


@pytest.fixture(scope="function")
def geometric_calibration_task_with_simple_raw_data(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_cryonirsp_constants_db
):
    number_of_modstates = 1
    number_of_beams = 2
    exposure_time = 20.0  # From CryonirspHeadersValidSolarGainFrames fixture
    data_shape_int = (30, 30)
    data_shape_raw = (30, 60)
    constants_db = CryonirspConstantsDb(
        NUM_MODSTATES=number_of_modstates, SOLAR_GAIN_EXPOSURE_TIMES=(exposure_time,), ARM_ID="SP"
    )
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPGeometricCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="sp_geometric_calibration",
        workflow_version="VX.Y",
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
        assign_input_dataset_doc_to_task(task, param_class())

        # Create the intermediate frames needed
        # Create a fake bad pixel map
        task.intermediate_frame_write_arrays(
            arrays=np.zeros(data_shape_raw),
            task_tag=CryonirspTag.task_bad_pixel_map(),
        )
        for beam in range(1, number_of_beams + 1):
            dark_cal = np.ones(data_shape_int) * 3.0
            task.intermediate_frame_write_arrays(
                arrays=dark_cal,
                beam=beam,
                task_tag=CryonirspTag.task_dark(),
                exposure_time=exposure_time,
            )

            # Need a lamp for each beam
            lamp_gain = np.ones(data_shape_int)
            task.intermediate_frame_write_arrays(
                arrays=lamp_gain,
                beam=beam,
                task_tag=CryonirspTag.task_lamp_gain(),
                exposure_time=exposure_time,
            )

            # And a beam border intermediate array
            task.intermediate_frame_write_arrays(
                arrays=np.array([0, 30, ((beam - 1) * 30), (30 + (beam - 1) * 30)]),
                task_tag=CryonirspTag.task_beam_boundaries(),
                beam=beam,
            )

            # Let's write a dark with the wrong exposure time, just to make sure it doesn't get used
            task.intermediate_frame_write_arrays(
                arrays=np.ones(data_shape_int) * 1e6,
                beam=beam,
                task_tag=CryonirspTag.task_dark(),
                exposure_time=exposure_time**2,
            )

        # Create the raw data, which is based on two beams per frame
        beam1 = 1
        beam2 = 2
        dark_cal_two_beams = np.concatenate((dark_cal, dark_cal), axis=1)
        ds = CryonirspHeadersValidSPSolarGainFrames(
            dataset_shape=(1,) + data_shape_raw,
            array_shape=(1,) + data_shape_raw,
            time_delta=10,
        )
        header = ds.header()
        true_solar = np.ones(data_shape_raw)
        # Now add the beam number to each beam in the array
        true_solar[:, 0:30] += beam1
        true_solar[:, 30:60] += beam2
        raw_solar = true_solar + dark_cal_two_beams
        solar_hdul = generate_214_l0_fits_frame(data=raw_solar, s122_header=header)
        task.write(
            data=solar_hdul,
            tags=[
                CryonirspTag.linearized(),
                CryonirspTag.task_solar_gain(),
                CryonirspTag.frame(),
                CryonirspTag.exposure_time(exposure_time),
            ],
            encoder=fits_hdulist_encoder,
        )

        yield task
        task._purge()


def test_geometric_task(geometric_calibration_task_that_completes, mocker):
    """
    Given: A set of raw solar gain images and necessary intermediate calibrations
    When: Running the geometric task
    Then: The damn thing runs and makes outputs that at least are the right type
    """
    # See the note in the fixture above: this test does NOT test for accuracy of the calibration
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = geometric_calibration_task_that_completes
    task()
    for beam in range(1, task.constants.num_beams + 1):
        assert type(task.intermediate_frame_load_angle(beam=beam)) is float
        assert task.intermediate_frame_load_spec_shift(beam=beam).shape == (30,)
        assert task.intermediate_frame_load_state_offset(beam=beam).shape == (2,)

    quality_files = task.read(tags=[CryonirspTag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task_solar_gain(),
                ]
            )


def test_basic_corrections(geometric_calibration_task_with_simple_raw_data):
    """
    Given: A set of raw solar gain images and necessary intermediate calibrations
    When: Doing basic dark and lamp gain corrections
    Then: The corrections are applied correctly
    """
    task = geometric_calibration_task_with_simple_raw_data
    task.do_basic_corrections()
    for beam in range(1, task.constants.num_beams + 1):
        expected = np.ones((30, 30)) + beam
        array = task.basic_corrected_data(beam=beam)
        np.testing.assert_equal(expected, array)
