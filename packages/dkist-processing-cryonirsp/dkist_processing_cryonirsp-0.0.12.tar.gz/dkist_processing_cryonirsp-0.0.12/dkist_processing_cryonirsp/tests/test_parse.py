from datetime import datetime
from datetime import timedelta
from itertools import chain

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator.translator import translate_spec122_to_spec214_l0
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspLinearizedData
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspRampData
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidCISolarGainFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidDarkFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidLampGainFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidNonLinearizedFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidObserveFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidPolcalFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidSPSolarGainFrames

# from dkist_processing_common.models.tags import Tag


@pytest.fixture(scope="function")
def parse_non_linearized_valid_task(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, request
):
    arm_id = "SP"
    camera_readout_mode = "FastUpTheRamp"
    with ParseL0CryonirspRampData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryonirsp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            start_time = datetime(1946, 11, 20).isoformat("T")
            ds = CryonirspHeadersValidNonLinearizedFrames(
                arm_id=arm_id,
                camera_readout_mode=camera_readout_mode,
                dataset_shape=(2, 2, 2),
                array_shape=(1, 2, 2),
                time_delta=10,
                roi_x_origin=0,
                roi_y_origin=0,
                roi_x_size=2,
                roi_y_size=2,
                date_obs=start_time,
                exposure_time=0.01,
            )
            # Initial header creation...
            counter = 0
            for d in ds:
                header = d.header()
                translated_header = translate_spec122_to_spec214_l0(header)
                # Set the integrated exposure time for this NDR
                # This is a range from 0 to 90 in 10 steps
                translated_header["XPOSURE"] = 100 * counter * 0.01
                # Set the frame in ramp
                translated_header["CNCNDR"] = counter + 1
                counter += 1
                hdu = fits.PrimaryHDU(
                    data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                )
                hdul = fits.HDUList([hdu])
                task.write(
                    data=hdul,
                    tags=[
                        CryonirspTag.input(),
                        CryonirspTag.frame(),
                        CryonirspTag.curr_frame_in_ramp(translated_header["CNCNDR"]),
                        # All frames in a ramp have the same date-obs
                        CryonirspTag.time_obs(str(start_time)),
                    ],
                    encoder=fits_hdulist_encoder,
                )
            yield task
        finally:
            task._purge()


@pytest.fixture(scope="function", params=["CI", "SP"])
def parse_linearized_valid_task(tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, request):
    arm_id = request.param
    num_maps = 1
    num_modstates = 2
    num_steps = 3
    with ParseL0CryonirspLinearizedData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryonirsp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            task.constants._update({CryonirspBudName.arm_id.value: arm_id})
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            ds1 = CryonirspHeadersValidDarkFrames(
                dataset_shape=(2, 2, 2), array_shape=(1, 2, 2), time_delta=10
            )
            ds2 = CryonirspHeadersValidLampGainFrames(
                dataset_shape=(2, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=10,
            )
            if arm_id == "CI":
                ds3 = CryonirspHeadersValidCISolarGainFrames(
                    dataset_shape=(2, 2, 2),
                    array_shape=(2, 2, 1),
                    time_delta=10,
                )
            elif arm_id == "SP":
                ds3 = CryonirspHeadersValidSPSolarGainFrames(
                    dataset_shape=(2, 2, 2),
                    array_shape=(2, 2, 1),
                    time_delta=10,
                )
            ds4 = CryonirspHeadersValidPolcalFrames(
                dataset_shape=(2, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=30,
                num_modstates=2,
                modstate=1,
            )
            ds = chain(ds1, ds2, ds3, ds4)
            for d in ds:
                header = d.header()
                translated_header = translate_spec122_to_spec214_l0(header)
                hdu = fits.PrimaryHDU(
                    data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                )
                hdul = fits.HDUList([hdu])
                task.write(
                    data=hdul,
                    tags=[CryonirspTag.linearized(), CryonirspTag.frame()],
                    encoder=fits_hdulist_encoder,
                )

            start_time = datetime.now()
            time_delta = timedelta(seconds=10)
            i = 0
            for map_scan in range(1, num_maps + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(1, num_steps + 1):
                        ds = CryonirspHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_scan_steps=num_steps,
                            scan_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            num_map_scans=1,
                            map_scan=1,
                            num_meas=1,
                            meas_num=1,
                            start_time=start_time + i * time_delta,
                            arm_id=arm_id,
                        )
                        header = next(ds).header()
                        header["CAM__004"] = [0.02, 0.03][m % 2]
                        translated_header = translate_spec122_to_spec214_l0(header)
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.write(
                            data=hdul,
                            tags=[CryonirspTag.linearized(), CryonirspTag.frame()],
                            encoder=fits_hdulist_encoder,
                        )
                        i += 1
            yield task
        finally:
            task._purge()


@pytest.fixture(scope="function", params=["CI", "SP"])
def parse_task_with_multi_num_scan_steps(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, request
):
    arm_id = request.param
    num_steps = 4
    num_map_scans = 2
    num_modstates = 2
    with ParseL0CryonirspLinearizedData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryonirsp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            for map_scan in range(1, num_map_scans + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(1, num_steps + 1):
                        ds = CryonirspHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_scan_steps=num_steps,
                            scan_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            num_map_scans=1,
                            map_scan=1,
                            num_meas=1,
                            meas_num=1,
                            arm_id=arm_id,
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        translated_header["CNNUMSCN"] = s % 3
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.write(
                            data=hdul,
                            tags=[CryonirspTag.linearized(), CryonirspTag.frame()],
                            encoder=fits_hdulist_encoder,
                        )
            yield task
        finally:
            task._purge()


@pytest.fixture(scope="function", params=["CI", "SP"])
def parse_task_with_incomplete_final_map(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, request
):
    arm_id = request.param
    num_steps = 4
    num_map_scans = 3
    num_modstates = 2
    num_sub_repeats = 2
    with ParseL0CryonirspLinearizedData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryonirsp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            for map_scan in range(1, num_map_scans):
                for m in range(1, num_modstates + 1):
                    for s in range(1, num_steps + 1):
                        for r in range(1, num_sub_repeats + 1):
                            ds = CryonirspHeadersValidObserveFrames(
                                dataset_shape=(2, 2, 2),
                                array_shape=(1, 2, 2),
                                time_delta=10,
                                num_scan_steps=num_steps,
                                scan_step=s,
                                num_modstates=num_modstates,
                                modstate=m,
                                num_map_scans=num_map_scans,
                                map_scan=map_scan,
                                num_meas=1,
                                meas_num=1,
                                arm_id=arm_id,
                                num_sub_repeats=num_sub_repeats,
                                sub_repeat_num=r,
                            )
                            header = next(ds).header()
                            translated_header = translate_spec122_to_spec214_l0(header)
                            hdu = fits.PrimaryHDU(
                                data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                            )
                            hdul = fits.HDUList([hdu])
                            task.write(
                                data=hdul,
                                tags=[CryonirspTag.linearized(), CryonirspTag.frame()],
                                encoder=fits_hdulist_encoder,
                            )
            # Now do the incomplete map
            for map_scan in range(num_map_scans, num_map_scans + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(1, num_steps):  # One step is missing in the last map
                        for r in range(1, num_sub_repeats + 1):
                            ds = CryonirspHeadersValidObserveFrames(
                                dataset_shape=(2, 2, 2),
                                array_shape=(1, 2, 2),
                                time_delta=10,
                                num_scan_steps=num_steps,
                                scan_step=s,
                                num_modstates=num_modstates,
                                modstate=m,
                                num_map_scans=num_map_scans,
                                map_scan=map_scan,
                                num_meas=1,
                                meas_num=1,
                                arm_id=arm_id,
                                num_sub_repeats=num_sub_repeats,
                                sub_repeat_num=r,
                            )
                            header = next(ds).header()
                            translated_header = translate_spec122_to_spec214_l0(header)
                            hdu = fits.PrimaryHDU(
                                data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                            )
                            hdul = fits.HDUList([hdu])
                            task.write(
                                data=hdul,
                                tags=[CryonirspTag.linearized(), CryonirspTag.frame()],
                                encoder=fits_hdulist_encoder,
                            )
            yield task, num_steps, num_map_scans
        finally:
            task._purge()


@pytest.fixture(scope="function", params=["CI", "SP"])
def parse_task_with_incomplete_raster_scan(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, request
):
    arm_id = request.param
    num_steps = 4
    num_maps = 1
    num_modstates = 2
    with ParseL0CryonirspLinearizedData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryonirsp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            for map_scan in range(1, num_maps + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(1, num_steps + 1):
                        ds = CryonirspHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_scan_steps=num_steps,
                            scan_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            num_map_scans=1,
                            map_scan=1,
                            num_meas=1,
                            meas_num=1,
                            arm_id=arm_id,
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        translated_header["CNNUMSCN"] = num_steps + 10
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.write(
                            data=hdul,
                            tags=[CryonirspTag.linearized(), CryonirspTag.frame()],
                            encoder=fits_hdulist_encoder,
                        )
            yield task, num_steps, num_maps
        finally:
            task._purge()


@pytest.fixture(scope="function")
def parse_task_with_polcal_task_types(
    tmp_path,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
):
    with ParseL0CryonirspLinearizedData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryonirsp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())

            base_header = CryonirspHeadersValidPolcalFrames(
                dataset_shape=(1, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=30,
                num_modstates=1,
                modstate=1,
            ).header()

            dark_header = base_header.copy()
            dark_header["PAC__008"] = "DarkShutter"
            dark_header["PAC__006"] = "clear"
            dark_header["PAC__004"] = "clear"

            gain_header = base_header.copy()
            gain_header["PAC__008"] = "FieldStopFoo"
            gain_header["PAC__006"] = "clear"
            gain_header["PAC__004"] = "clear"

            data_header = base_header.copy()
            data_header["PAC__008"] = "FieldStopFoo"
            data_header["PAC__006"] = "SiO2 SAR"
            data_header["PAC__004"] = "Sapphire Polarizer"

            for header in [dark_header, gain_header, data_header]:
                translated_header = translate_spec122_to_spec214_l0(header)
                hdu = fits.PrimaryHDU(
                    data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                )
                hdul = fits.HDUList([hdu])
                task.write(
                    data=hdul,
                    tags=[CryonirspTag.linearized(), CryonirspTag.frame()],
                    encoder=fits_hdulist_encoder,
                )

            yield task
        finally:
            task._purge()


def test_parse_cryonirsp_linearized_data(parse_linearized_valid_task, mocker):
    """
    Given: A ParseCryonirspInputData task
    When: Calling the task instance
    Then: All tagged files exist and individual task tags are applied
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    parse_linearized_valid_task()
    # Then
    translated_input_files = parse_linearized_valid_task.read(
        tags=[CryonirspTag.linearized(), CryonirspTag.frame()]
    )
    for filepath in translated_input_files:
        assert filepath.exists()

    assert list(
        parse_linearized_valid_task.read(tags=[CryonirspTag.linearized(), CryonirspTag.task_dark()])
    )
    assert list(
        parse_linearized_valid_task.read(
            tags=[CryonirspTag.linearized(), CryonirspTag.task_lamp_gain()]
        )
    )
    assert list(
        parse_linearized_valid_task.read(
            tags=[CryonirspTag.linearized(), CryonirspTag.task_solar_gain()]
        )
    )
    assert list(
        parse_linearized_valid_task.read(
            tags=[CryonirspTag.linearized(), CryonirspTag.task_polcal()]
        )
    )
    assert list(
        parse_linearized_valid_task.read(
            tags=[CryonirspTag.linearized(), CryonirspTag.task_observe()]
        )
    )


def test_parse_cryonirsp_non_linearized_data(parse_non_linearized_valid_task, mocker):
    """
    Given: A ParseCryonirspInputData task
    When: Calling the task instance
    Then: All tagged files exist and individual task tags are applied
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    parse_non_linearized_valid_task()
    # Then
    translated_input_files = parse_non_linearized_valid_task.read(
        tags=[CryonirspTag.input(), CryonirspTag.frame()]
    )
    filepaths = list(translated_input_files)
    cncndr_list = []
    for i, filepath in enumerate(filepaths):
        assert filepath.exists()
        hdul = fits.open(filepath)
        cncndr_list.append(hdul[0].header["CNCNDR"])
    assert len(filepaths) == 2
    assert sorted(cncndr_list) == [1, 2]
    assert parse_non_linearized_valid_task.constants._db_dict["CAM_READOUT_MODE"] == "FastUpTheRamp"
    assert parse_non_linearized_valid_task.constants._db_dict["ARM_ID"] == "SP"
    assert len(parse_non_linearized_valid_task.constants._db_dict["TIME_OBS_LIST"]) == 1
    assert parse_non_linearized_valid_task.constants._db_dict["TIME_OBS_LIST"][0] == datetime(
        1946, 11, 20
    ).isoformat("T")


def test_parse_cryonirsp_linearized_data_constants(parse_linearized_valid_task, mocker):
    """
    Given: A ParseCryonirspInputData task
    When: Calling the task instance
    Then: Constants are in the constants object as expected
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    parse_linearized_valid_task()
    # Then
    assert parse_linearized_valid_task.constants._db_dict["NUM_MODSTATES"] == 2
    assert parse_linearized_valid_task.constants._db_dict["NUM_MAP_SCANS"] == 1
    assert parse_linearized_valid_task.constants._db_dict["NUM_SCAN_STEPS"] == 3
    assert parse_linearized_valid_task.constants._db_dict["WAVELENGTH"] == 1080.2
    assert parse_linearized_valid_task.constants._db_dict["DARK_EXPOSURE_TIMES"] == [1.0]
    assert parse_linearized_valid_task.constants._db_dict["LAMP_GAIN_EXPOSURE_TIMES"] == [10.0]
    assert parse_linearized_valid_task.constants._db_dict["SOLAR_GAIN_EXPOSURE_TIMES"] == [20.0]
    assert parse_linearized_valid_task.constants._db_dict["POLCAL_EXPOSURE_TIMES"] == [0.01]
    assert parse_linearized_valid_task.constants._db_dict["OBSERVE_EXPOSURE_TIMES"] == [0.02, 0.03]
    assert parse_linearized_valid_task.constants._db_dict["MODULATOR_SPIN_MODE"] == "Continuous"


def test_parse_cryonirsp_values(parse_linearized_valid_task, mocker):
    """
    :Given: A valid parse input task
    :When: Calling the task instance
    :Then: Values are correctly loaded into the constants mutable mapping
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    parse_linearized_valid_task()
    assert parse_linearized_valid_task.constants.instrument == "CRYO-NIRSP"
    assert parse_linearized_valid_task.constants.average_cadence == 10
    assert parse_linearized_valid_task.constants.maximum_cadence == 10
    assert parse_linearized_valid_task.constants.minimum_cadence == 10
    assert parse_linearized_valid_task.constants.variance_cadence == 0


def test_multiple_num_scan_steps_raises_error(parse_task_with_multi_num_scan_steps, mocker):
    """
    :Given: A prase task with data that have inconsistent CNNUMSCN values
    :When: Calling the parse task
    :Then: The correct error is raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    with pytest.raises(ValueError, match="Multiple NUM_SCAN_STEPS values found.*"):
        parse_task_with_multi_num_scan_steps()


def test_incomplete_single_map(parse_task_with_incomplete_raster_scan, mocker):
    """
    :Given: A parse task with data that has an incomplete raster scan
    :When: Calling the parse task
    :Then: The correct number of raster steps are found
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, num_steps, num_map_scans = parse_task_with_incomplete_raster_scan
    task()
    assert task.constants._db_dict["NUM_SCAN_STEPS"] == num_steps
    assert task.constants._db_dict["NUM_MAP_SCANS"] == num_map_scans


def test_incomplete_final_map(parse_task_with_incomplete_final_map, mocker):
    """
    :Given: A parse task with data that has complete raster scans along with an incomplete raster scan
    :When: Calling the parse task
    :Then: The correct number of raster steps and maps are found
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, num_steps, num_map_scans = parse_task_with_incomplete_final_map
    task()
    assert task.constants._db_dict["NUM_SCAN_STEPS"] == num_steps
    assert task.constants._db_dict["NUM_MAP_SCANS"] == num_map_scans - 1


def test_polcal_task_parsing(parse_task_with_polcal_task_types, mocker):
    """
    :Given: A Parse task with associated polcal files that include polcal gain and dark
    :When: Tagging the task of each file
    :Then: Polcal gain and darks are identified and also tagged with simply TASK_POLCAL
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = parse_task_with_polcal_task_types
    task()
    assert task.scratch.count_all(tags=[CryonirspTag.task("POLCAL_DARK")]) == 1
    assert task.scratch.count_all(tags=[CryonirspTag.task("POLCAL_GAIN")]) == 1
    assert task.scratch.count_all(tags=[CryonirspTag.task("POLCAL")]) == 3
