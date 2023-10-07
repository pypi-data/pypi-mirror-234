"""CryoNIRSP task parser."""
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)

from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess


def parse_header_ip_task(fits_obj: CryonirspL0FitsAccess) -> str:
    """
    Parse CryoNIRSP tasks that aren't fully captured by the single IPTASK keyword.

    Right now this just distinguishes between solar and lamp gain images.
    """
    if (
        fits_obj.ip_task_type.upper() == TaskName.gain.value
        and fits_obj.gos_level3_status == "lamp"
        and fits_obj.gos_level3_lamp_status == "on"
    ):
        return TaskName.lamp_gain.value
    if (
        fits_obj.ip_task_type.upper() == TaskName.gain.value
        and fits_obj.gos_level3_status == "clear"
    ):
        return TaskName.solar_gain.value

    return fits_obj.ip_task_type


class CryonirspTaskTypeFlower(SingleValueSingleKeyFlower):
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
        return parse_header_ip_task(fits_obj)
