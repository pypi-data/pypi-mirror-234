"""Flower to tag specific polcal subtypes gain and dark."""
from typing import Type

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)

from dkist_processing_cryonirsp.models.task_name import CryonirspTaskName
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess


def parse_polcal_task_type(fits_obj: CryonirspL0FitsAccess) -> str | Type[SpilledDirt]:
    """Identify and tag polcal dark and gain frames."""
    if (
        fits_obj.gos_level0_status == "DarkShutter"
        and fits_obj.gos_retarder_status == "clear"
        and fits_obj.gos_polarizer_status == "clear"
    ):
        return CryonirspTaskName.polcal_dark.value
    elif (
        fits_obj.gos_level0_status.startswith("FieldStop")
        and fits_obj.gos_retarder_status == "clear"
        and fits_obj.gos_polarizer_status == "clear"
    ):
        return CryonirspTaskName.polcal_gain.value

    return SpilledDirt


class PolcalTaskFlower(SingleValueSingleKeyFlower):
    """Flower to find the CryoNIRSP task type."""

    def __init__(self):
        super().__init__(tag_stem_name=StemName.task.value, metadata_key="ip_task_type")

    def setter(self, fits_obj: CryonirspL0FitsAccess):
        """
        Set value of the flower.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type.upper() != TaskName.polcal.value:
            return SpilledDirt

        return parse_polcal_task_type(fits_obj)
