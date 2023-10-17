import json

import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.quality_metrics import CryonirspL1QualityMetrics
from dkist_processing_cryonirsp.tests.conftest import Cryonirsp122ObserveFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import generate_214_l1_fits_frame


@pytest.fixture(scope="function")
def cryo_quality_task(tmp_path, recipe_run_id, init_cryonirsp_constants_db):
    num_map_scans = 3
    num_scan_steps = 1
    constants_db = CryonirspConstantsDb(
        NUM_MAP_SCANS=num_map_scans,
        NUM_SCAN_STEPS=num_scan_steps,
    )
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with CryonirspL1QualityMetrics(
        recipe_run_id=recipe_run_id, workflow_name="science_calibration", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path)

        # Create fake stokes frames
        for map_scan in range(1, num_map_scans + 1):
            for scan_step in range(1, num_scan_steps + 1):
                for stokes_param, index in zip(("I", "Q", "U", "V"), (1, 2, 3, 4)):
                    ds = Cryonirsp122ObserveFrames(
                        array_shape=(1, 10, 10),
                        num_steps=num_scan_steps,
                        num_map_scans=num_map_scans,
                    )
                    header_generator = (
                        spec122_validator.validate_and_translate_to_214_l0(
                            d.header(), return_type=fits.HDUList
                        )[0].header
                        for d in ds
                    )

                    hdul = generate_214_l1_fits_frame(s122_header=next(header_generator))
                    hdul[1].header["DINDEX5"] = index
                    task.write(
                        data=hdul,
                        tags=[
                            CryonirspTag.output(),
                            CryonirspTag.frame(),
                            CryonirspTag.stokes(stokes_param),
                            CryonirspTag.scan_step(scan_step),
                            CryonirspTag.map_scan(map_scan),
                            CryonirspTag.meas_num(1),
                        ],
                        encoder=fits_hdulist_encoder,
                    )

        yield task
        task._purge()


def test_quality_task(cryo_quality_task, mocker):
    """
    Given: A CryonirspQualityMetrics task
    When: Calling the task instance
    Then: A single sensitivity measurement and datetime is recorded for each map scan for each Stokes Q, U, and V,
            and a single noise measurement and datetime is recorded for L1 file for each Stokes Q, U, and V
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task = cryo_quality_task
    task()
    # Then
    num_map_scans = task.constants.num_map_scans
    num_steps = task.constants.num_scan_steps
    sensitivity_files = list(task.read(tags=[CryonirspTag.quality("SENSITIVITY")]))
    assert len(sensitivity_files) == 4
    for file in sensitivity_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            for time in data["x_values"]:
                assert isinstance(time, str)
            for sensitivity in data["y_values"]:
                assert isinstance(sensitivity, float)
            assert len(data["x_values"]) == len(data["y_values"]) == num_map_scans

    noise_files = list(task.read(tags=[CryonirspTag.quality("NOISE")]))
    assert len(noise_files) == 4
    for file in noise_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            for time in data["x_values"]:
                assert isinstance(time, str)
            for noise in data["y_values"]:
                assert isinstance(noise, float)
            assert len(data["x_values"]) == len(data["y_values"]) == num_map_scans * num_steps
