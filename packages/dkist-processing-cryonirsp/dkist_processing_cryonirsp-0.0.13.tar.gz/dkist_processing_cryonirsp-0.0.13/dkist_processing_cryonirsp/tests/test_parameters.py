from dataclasses import asdict
from typing import Any

import numpy as np
import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from hypothesis import example
from hypothesis import given
from hypothesis import HealthCheck
from hypothesis import settings
from hypothesis import strategies as st

from dkist_processing_cryonirsp.models.parameters import CryonirspParameters
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import FileParameter
from dkist_processing_cryonirsp.tests.conftest import TestingParameters

# Definitions used throughout these tests:
# test_params are the parameters defined in CryonirspTestingParameters()
# task_params are the parameters defined in CryonirspParameters()


@pytest.fixture(scope="function")
def basic_science_task_with_parameter_mixin(
    tmp_path,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
    init_cryonirsp_constants_db,
):
    class Task(CryonirspTaskBase):
        def run(self):
            ...

    init_cryonirsp_constants_db(recipe_run_id, CryonirspConstantsDb())
    task = Task(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryonirsp_input_data",
        workflow_version="VX.Y",
    )
    try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        test_params = cryonirsp_testing_parameters_factory(param_path=tmp_path)
        assign_input_dataset_doc_to_task(task, test_params())
        yield task, test_params()
    finally:
        task._purge()


def _is_wavelength_param(param_value: Any) -> bool:
    return isinstance(param_value, dict) and "wavelength" in param_value


@given(wave=st.floats(min_value=800.0, max_value=2000.0))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@example(wave=1082.7)
def test_wave_parameters(basic_science_task_with_parameter_mixin, wave):
    """
    Given: A Science task with the parameter mixin
    When: Accessing properties for parameters that depend on wavelength
    Then: The correct value is returned
    """
    task, expected = basic_science_task_with_parameter_mixin
    task_params = task.parameters
    task_params._wavelength = wave
    pwaves = np.array(expected.cryonirsp_solar_zone_normalization_percentile.wavelength)
    midpoints = 0.5 * (pwaves[1:] + pwaves[:-1])
    idx = np.sum(midpoints < wave)
    for pn, pv in asdict(expected).items():
        if _is_wavelength_param(pv):
            assert getattr(task_params, pn.replace("cryonirsp_", "")) == pv["values"][idx]


def _is_file_param(param_value: Any) -> bool:
    return isinstance(param_value, dict) and "is_file" in param_value and param_value["is_file"]


def test_file_parameters(basic_science_task_with_parameter_mixin):
    """
    Given: A Science task with the parameter mixin
    When: Accessing parameters whose values are loaded from files
    Then: The correct value is returned

    This test exercises all aspects of file parameters from their names to the loading of values
    """
    task, test_params = basic_science_task_with_parameter_mixin
    task_params = task.parameters
    # Iterate over the test parameters and check that each file param exists in the task parameters
    # we load the actual parameter from the task param object using only the param name
    for pn, pv in asdict(test_params).items():
        # We want to test only file parameters
        if _is_file_param(pv):
            pn_no_prefix = pn.removeprefix("cryonirsp_")
            # If the param name is an attribute in task_params, then load it directly
            if hasattr(task_params, pn_no_prefix):
                param_name = pn_no_prefix
                actual = task_params._load_param_value_from_npy_file(
                    getattr(task_params, param_name)
                )
            # if the param name is not a task param attribute, then check that we can load the param
            # using the value defined in the input_dataset_parameters list of the task param object
            else:
                param_dict = task_params._find_most_recent_past_value(pn)
                actual = task_params._load_param_value_from_npy_file(param_dict)
            # Now get the expected value using the param value dict from the testing params
            expected = np.load(pv["param_path"])
            # Compare the actual and expected values
            assert np.array_equal(actual, expected)


def _is_arm_param(
    param_name: str, task_params: CryonirspParameters, testing_params: TestingParameters
):
    """
    Test if a parameter is an arm parameter.

    An arm parameter is one which is present in the task_param class with no arm suffix and is also
    present in the test_param class with suffixed forms only, one for each arm.
    This allows a non-arm-specific name to be used as a property in the parameters class which
    encapsulates the mechanism used to return the arm specific parameter value based on the arm in use.
    """
    # NB: param_name is assumed to have a prefix of "cryonirsp_"
    arm_suffixes = ["_sp", "_ci"]
    suffix = param_name[-3:]
    if suffix not in arm_suffixes:
        return False
    param_name_no_suffix = param_name[:-3]
    param_names_with_suffixes = [f"{param_name_no_suffix}{suffix}" for suffix in arm_suffixes]
    suffixed_names_exist = all(
        [hasattr(testing_params, pname) for pname in param_names_with_suffixes]
    )
    generic_param_name = param_name_no_suffix.removeprefix("cryonirsp_")
    return hasattr(task_params, generic_param_name) and suffixed_names_exist


def test_arm_parameters(basic_science_task_with_parameter_mixin):
    """
    Given: A Science task with the parameter mixin
    When: Accessing parameters that are "arm" parameters
    Then: The correct value is returned

    This test exercises all aspects of arm parameters from their names to the loading of values,
    which includes exercising the method _find_parameter_for_arm
    """
    # An arm parameter is one which is present in the param class with no arm suffix
    # and is also present in the testing param class with both suffix forms
    task, test_params = basic_science_task_with_parameter_mixin
    task_params = task.parameters
    # Iterate over the test parameters
    for pn, pv in asdict(test_params).items():
        # We want to test only generic parameters
        if _is_arm_param(pn, task_params, test_params):
            # get the generic param name
            suffix = pn[-3:]
            generic_param_name = pn.removeprefix("cryonirsp_").removesuffix(suffix)
            # Need to set arm_id here top make sure we get the right value
            task_params._arm_id = suffix[-2:].upper()
            actual = getattr(task_params, generic_param_name)
            expected = getattr(test_params, pn)
            if isinstance(expected, FileParameter) and expected.is_file:
                expected = task_params._load_param_value_from_npy_file(asdict(expected))
                assert np.array_equal(expected, actual)
            else:
                assert expected == actual


def test_other_parameters(basic_science_task_with_parameter_mixin):
    """
    Given: A Science task with the parameter mixin
    When: Accessing properties for parameters that are not wavelength, file or generic parameters
    Then: The correct value is returned
    """
    task, test_params = basic_science_task_with_parameter_mixin
    task_params = task.parameters
    for pn, pv in asdict(test_params).items():
        if (
            _is_file_param(pv)
            or _is_wavelength_param(pv)
            or _is_arm_param(pn, task_params, test_params)
        ):
            continue
        assert pv == getattr(task_params, pn.removeprefix("cryonirsp_"))
