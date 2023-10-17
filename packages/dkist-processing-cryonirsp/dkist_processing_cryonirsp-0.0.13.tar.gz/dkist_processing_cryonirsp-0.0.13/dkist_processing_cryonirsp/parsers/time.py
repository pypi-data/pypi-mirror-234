"""Bud to find exposure time."""
from typing import Hashable

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.parsers.time import TaskExposureTimesBud

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspRampFitsAccess
from dkist_processing_cryonirsp.parsers.task import parse_header_ip_task


class CryonirspTaskExposureTimesBud(TaskExposureTimesBud):
    """
    Overload of common TaskExposureTimesBud to allow for custom Cryonirsp parsing of ip_task_type.

    Parameters
    ----------
    stem_name : str
        The name of the stem of the tag
    ip_task_type : str
        Instrument program task type
    """

    def setter(self, fits_obj: CryonirspL0FitsAccess):
        """
        Set the value of the bud.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        # This is where it's different than the common `TaskExposureTimesBud`
        ip_task_type = parse_header_ip_task(fits_obj)
        if ip_task_type.lower() == self.ip_task_type.lower():
            raw_exp_time = getattr(fits_obj, self.metadata_key)
            return round(raw_exp_time, 6)
        return SpilledDirt


class CryonirspTimeObsBud(Stem):
    """
    Produce a tuple of all time_obs values present in the dataset.

    The time_obs is a unique identifier for all raw frames in a single ramp. Hence, this list identifies all
    the ramps that must be processed in a data set.
    """

    def __init__(self):
        super().__init__(stem_name=CryonirspBudName.time_obs_list.value)

    def setter(self, fits_obj: CryonirspRampFitsAccess):
        """
        Set the time_obs for this fits object.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The time_obs value associated with this fits object
        """
        return fits_obj.time_obs

    def getter(self, key: Hashable) -> tuple:
        """
        Get the sorted tuple of time_obs values.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        A tuple of exposure times
        """
        time_obs_tup = tuple(sorted(set(self.key_to_petal_dict.values())))
        return time_obs_tup
