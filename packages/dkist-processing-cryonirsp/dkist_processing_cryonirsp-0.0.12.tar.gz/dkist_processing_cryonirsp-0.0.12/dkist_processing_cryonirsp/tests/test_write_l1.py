from datetime import datetime
from typing import Literal

import numpy as np
import pytest
from astropy.io import fits
from astropy.time import Time
from dkist_fits_specifications import __version__ as spec_version
from dkist_header_validator import spec214_validator
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.write_l1 import CIWriteL1Frame
from dkist_processing_cryonirsp.tasks.write_l1 import SPWriteL1Frame
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb


@pytest.fixture(scope="function")
def write_l1_task(
    recipe_run_id,
    calibrated_ci_cryonirsp_headers,
    calibrated_cryonirsp_headers,
    init_cryonirsp_constants_db,
    num_stokes_params,
    num_map_scans,
    num_meas,
    arm_id,
):
    if num_stokes_params == 1:
        num_modstates = 1
    else:
        num_modstates = 2
    num_scan_steps = 2
    if arm_id == "CI":
        axis_1_type = "HPLN-TAN"
        axis_2_type = "HPLT-TAN"
        axis_3_type = "AWAV"
        write_l1_task = CIWriteL1Frame
        calibrated_headers = calibrated_ci_cryonirsp_headers
    else:
        axis_1_type = "AWAV"
        axis_2_type = "HPLT-TAN"
        axis_3_type = "HPLN-TAN"
        write_l1_task = SPWriteL1Frame
        calibrated_headers = calibrated_cryonirsp_headers

    constants_db = CryonirspConstantsDb(
        AVERAGE_CADENCE=10,
        MINIMUM_CADENCE=10,
        MAXIMUM_CADENCE=10,
        VARIANCE_CADENCE=0,
        NUM_MAP_SCANS=num_map_scans,
        NUM_SCAN_STEPS=num_scan_steps,
        # Needed so self.correct_for_polarization is set to the right value
        NUM_MODSTATES=num_modstates,
        ARM_ID=arm_id,
        AXIS_1_TYPE=axis_1_type,
        AXIS_2_TYPE=axis_2_type,
        AXIS_3_TYPE=axis_3_type,
        NUM_MEAS=num_meas,
    )

    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with write_l1_task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            if num_stokes_params == 1:
                stokes_params = ["I"]
            else:
                stokes_params = ["I", "Q", "U", "V"]
            # Random data needed so skew and kurtosis don't barf
            header = calibrated_headers
            hdu = fits.PrimaryHDU(
                data=np.random.random((header["NAXIS3"], header["NAXIS2"], header["NAXIS1"]))
                * 100.0,
                header=calibrated_headers,
            )
            hdul = fits.HDUList([hdu])
            hdul[0].header["CTYPE1"] = axis_1_type
            hdul[0].header["CTYPE2"] = axis_2_type
            hdul[0].header["CTYPE3"] = axis_3_type
            for map_scan in range(1, num_map_scans + 1):
                for scan_step in range(1, num_scan_steps + 1):
                    for meas_num in range(1, num_meas + 1):
                        # all stokes files have the same date-beg
                        hdul[0].header["DATE-BEG"] = datetime.now().isoformat("T")
                        for stokes_param in stokes_params:
                            hdul[0].header["CNCMEAS"] = meas_num
                            hdul[0].header["CNMAP"] = map_scan
                            task.write(
                                data=hdul,
                                tags=[
                                    CryonirspTag.calibrated(),
                                    CryonirspTag.frame(),
                                    CryonirspTag.stokes(stokes_param),
                                    CryonirspTag.meas_num(meas_num),
                                    CryonirspTag.map_scan(map_scan),
                                    CryonirspTag.scan_step(scan_step),
                                ],
                                encoder=fits_hdulist_encoder,
                            )
            yield task, stokes_params
        finally:
            task._purge()


@pytest.mark.parametrize(
    "num_stokes_params",
    [pytest.param(1, id="Stokes I"), pytest.param(4, id="Stokes IQUV")],
)
@pytest.mark.parametrize(
    "num_meas",
    [pytest.param(1, id="single meas"), pytest.param(2, id="multiple meas")],
)
@pytest.mark.parametrize(
    "num_map_scans",
    [pytest.param(1, id="single map"), pytest.param(2, id="multiple maps")],
)
@pytest.mark.parametrize(
    "arm_id",
    [pytest.param("CI", id="CI"), pytest.param("SP", id="SP")],
)
def test_write_l1_frame(write_l1_task, mocker, arm_id, num_stokes_params, num_map_scans, num_meas):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, stokes_params = write_l1_task
    task()
    if arm_id == "CI":
        dtype1_value = "SPATIAL"
        scan_step_value = "TEMPORAL"
    else:
        dtype1_value = "SPECTRAL"
        scan_step_value = "SPATIAL"

    for stokes_param in stokes_params:
        for map_scan in range(1, task.constants.num_map_scans + 1):
            for scan_step in range(1, task.constants.num_scan_steps + 1):
                for meas_num in range(1, task.constants.num_meas + 1):
                    common_tags = [
                        CryonirspTag.frame(),
                        CryonirspTag.stokes(stokes_param),
                        CryonirspTag.map_scan(map_scan),
                        CryonirspTag.scan_step(scan_step),
                        CryonirspTag.meas_num(meas_num),
                    ]
                    output_files = list(task.read(tags=common_tags + [CryonirspTag.output()]))
                    calibrated_files = list(
                        task.read(tags=common_tags + [CryonirspTag.calibrated()])
                    )
                    assert len(output_files) == 1
                    output_file = output_files.pop()
                    assert output_file.exists
                    assert spec214_validator.validate(output_file, extra=False)
                    hdu_list = fits.open(output_file)
                    header = hdu_list[1].header
                    assert len(hdu_list) == 2  # Primary, CompImage
                    assert type(hdu_list[0]) is fits.PrimaryHDU
                    assert type(hdu_list[1]) is fits.CompImageHDU
                    assert header["DTYPE1"] == dtype1_value
                    assert header["DNAXIS1"] == header["NAXIS1"]
                    assert header["DTYPE2"] == "SPATIAL"
                    assert header["DNAXIS2"] == header["NAXIS2"]
                    axis_num = 3
                    if task.constants.num_meas > 1:
                        # measurement axis
                        assert header[f"DTYPE{axis_num}"] == "TEMPORAL"
                        assert header[f"DNAXIS{axis_num}"] == task.constants.num_meas
                        assert header[f"DINDEX{axis_num}"] == header["CNCMEAS"]
                        axis_num += 1
                        # scan step axis
                        assert header[f"DTYPE{axis_num}"] == scan_step_value
                        assert header[f"DNAXIS{axis_num}"] == task.constants.num_scan_steps
                        assert header[f"DINDEX{axis_num}"] == header["CNCURSCN"]
                    else:
                        # scan step axis
                        assert header[f"DTYPE{axis_num}"] == scan_step_value
                        assert header[f"DNAXIS{axis_num}"] == task.constants.num_scan_steps
                        assert header[f"DINDEX{axis_num}"] == header["CNCURSCN"]
                    if task.constants.num_map_scans > 1:
                        axis_num += 1
                        # map scan axis
                        assert header[f"DTYPE{axis_num}"] == "TEMPORAL"
                        assert header[f"DNAXIS{axis_num}"] == task.constants.num_map_scans
                        assert header[f"DINDEX{axis_num}"] == header["CNMAP"]
                    if task.constants.correct_for_polarization:
                        axis_num += 1
                        # stokes axis
                        assert header[f"DTYPE{axis_num}"] == "STOKES"
                        assert header[f"DNAXIS{axis_num}"] == 4
                        assert header[f"DINDEX{axis_num}"] in range(1, 5)
                    assert header["DAAXES"] == 2
                    assert header["DNAXIS"] == axis_num
                    assert header["DEAXES"] == axis_num - 2
                    assert f"DNAXIS{axis_num + 1}" not in header

                    assert header["INFO_URL"] == task.docs_base_url
                    assert header["HEADVERS"] == spec_version
                    assert (
                        header["HEAD_URL"]
                        == f"{task.docs_base_url}/projects/data-products/en/v{spec_version}"
                    )
                    calvers = task._get_version_from_module_name()
                    assert header["CALVERS"] == calvers
                    assert (
                        header["CAL_URL"]
                        == f"{task.docs_base_url}/projects/{task.constants.instrument.lower()}/en/v{calvers}/{task.workflow_name}.html"
                    )
                    cal_header = fits.open(calibrated_files.pop())[0].header

                    # Make sure we didn't overwrite pre-computed DATE-BEG and DATE-END keys
                    assert header["DATE-BEG"] == cal_header["DATE-BEG"]
                    assert header["DATE-END"] == cal_header["DATE-END"]
                    date_avg = (
                        (
                            Time(header["DATE-END"], precision=6)
                            - Time(header["DATE-BEG"], precision=6)
                        )
                        / 2
                        + Time(header["DATE-BEG"], precision=6)
                    ).isot
                    assert header["DATE-AVG"] == date_avg
                    assert isinstance(header["HLSVERS"], str)
                    assert header["NSPECLNS"] == 1
                    assert header["WAVEBAND"] == "He I (1083.0 nm)"
                    assert header["SPECLN01"] == "He I (1083.0 nm)"
                    with pytest.raises(KeyError):
                        header["SPECLN02"]
