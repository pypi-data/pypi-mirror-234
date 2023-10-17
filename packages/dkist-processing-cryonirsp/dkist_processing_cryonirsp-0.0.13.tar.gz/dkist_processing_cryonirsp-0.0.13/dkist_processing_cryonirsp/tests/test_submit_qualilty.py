import pytest

from dkist_processing_cryonirsp.tasks.l1_output_data import CISubmitQuality
from dkist_processing_cryonirsp.tasks.l1_output_data import SPSubmitQuality


@pytest.fixture(scope="function", params=["CI", "SP"])
def cryo_submit_quality_task(tmp_path, recipe_run_id, request):
    arm_id = request.param
    if arm_id == "CI":
        with CISubmitQuality(
            recipe_run_id=recipe_run_id,
            workflow_name="cryonirsp_submit_quality",
            workflow_version="VX.Y",
        ) as task:
            yield task, arm_id
            task._purge()
    elif arm_id == "SP":
        with SPSubmitQuality(
            recipe_run_id=recipe_run_id,
            workflow_name="cryonirsp_submit_quality",
            workflow_version="VX.Y",
        ) as task:
            yield task, arm_id
            task._purge()


@pytest.fixture
def build_report_mock(mocker):
    yield mocker.patch(
        "dkist_processing_common.tasks.mixin.quality.QualityMixin.quality_build_report",
        autospec=True,
    )


def test_correct_polcal_label_list(cryo_submit_quality_task, build_report_mock, mocker):
    """
    Given: A CISubmitQuality task
    When: Calling the task
    Then: The correct polcal_label_list property is passed to .build_report
    """
    task, arm_id = cryo_submit_quality_task

    # We don't care about this

    if arm_id == "SP":
        mocker.patch(
            "dkist_processing_cryonirsp.tasks.l1_output_data.SPSubmitQuality.metadata_store_add_quality_report"
        )
        task()
        build_report_mock.assert_called_once_with(
            task, polcal_label_list=["SP Beam 1", "SP Beam 2"]
        )
    elif arm_id == "CI":
        mocker.patch(
            "dkist_processing_cryonirsp.tasks.l1_output_data.CISubmitQuality.metadata_store_add_quality_report"
        )
        task()
        build_report_mock.assert_called_once_with(task, polcal_label_list=["CI Beam 1"])
