"""Stems for organizing files into separate dsps repeats."""
from __future__ import annotations

from abc import ABC
from collections import defaultdict
from functools import cached_property
from typing import Type

from astropy.time import Time
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.models.tags import CryonirspStemName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess


class SingleScanStep:
    """
    An object that uniquely defines a (scan_step, meas_num, modstate, sub_rep, time_obs) tuple from any number of dsps repeat repeats.

    This is just a fancy tuple.

    Basically, it just hashes the (scan_step, meas_num, modstate, sub_rep, time_obs) tuple so these objects can easily be compared.
    Also uses the time_obs property so that multiple dsps repeats of the same (scan_step, meas_num, modstate, sub_rep) can be sorted.
    """

    def __init__(self, fits_obj: CryonirspL0FitsAccess):
        """Read scan step, modstate, meas_num, sub_repeat_num, and obs time information from a FitsAccess object."""
        self.scan_step = fits_obj.scan_step
        self.modulator_state = fits_obj.modulator_state
        self.date_obs = Time(fits_obj.time_obs)
        self.meas_num = fits_obj.meas_num
        self.sub_repeat_num = fits_obj.sub_repeat_num

    def __repr__(self):
        return f"SingleScanStep with {self.scan_step = }, {self.modulator_state = }, {self.date_obs = }, {self.meas_num = }, and {self.sub_repeat_num = }"

    def __eq__(self, other: SingleScanStep) -> bool:
        """Two frames are equal if they have the same (scan_step, meas_num, modstate, sub_rep) tuple."""
        if not isinstance(other, SingleScanStep):
            raise TypeError(f"Cannon compare ScanStep with type {type(other)}")

        for attr in ["scan_step", "modulator_state", "date_obs", "meas_num", "sub_repeat_num"]:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def __lt__(self, other: SingleScanStep) -> bool:
        """Only sort on date_obs."""
        return self.date_obs < other.date_obs

    def __hash__(self) -> int:
        """Not strictly necessary, but does allow for using set() on these objects."""
        return hash(
            (
                self.scan_step,
                self.modulator_state,
                self.date_obs,
                self.meas_num,
                self.sub_repeat_num,
            )
        )


class MapScanStemBase(Stem, ABC):
    """Base class for Stems that use a dictionary of [int, dict[int, dict[int, dict[int, list[SingleScanStep]]]]] to analyze map_scan-related stuff."""

    # This only here so type-hinting of this complex dictionary will work.
    key_to_petal_dict: dict[str, SingleScanStep]

    @cached_property
    def scan_step_dict(self) -> dict[int, dict[int, dict[int, dict[int, list[SingleScanStep]]]]]:
        """Nested dictionary that contains a SingleScanStep for each ingested frame.

        Dictionary structure is [scan_step (int), dict[measurement(int), dict[modstate (int), dict[sub_repeat (int), list[SingleScanStep]]]]
        """
        scan_step_dict = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        )

        for scan_step_obj in self.key_to_petal_dict.values():
            scan_step_dict[scan_step_obj.scan_step][scan_step_obj.meas_num][
                scan_step_obj.modulator_state
            ][scan_step_obj.sub_repeat_num].append(scan_step_obj)

        return scan_step_dict

    def setter(self, fits_obj: CryonirspL0FitsAccess) -> SingleScanStep | Type[SpilledDirt]:
        """Ingest observe frames as SingleScanStep objects."""
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt
        return SingleScanStep(fits_obj=fits_obj)


class MapScanFlower(MapScanStemBase):
    """Flower for computing and assigning map scan numbers."""

    def __init__(self):
        super().__init__(stem_name=CryonirspStemName.map_scan.value)

    def getter(self, key: str) -> int:
        """Compute the map scan number for a single frame.

        The frame implies a SingleScanStep. That object is then compared to the sorted list of objects for a single
        (raster_step, meas_num, modstate, sub_repeat) tuple. The location within that sorted list is the map scan number.
        """
        scan_step_obj = self.key_to_petal_dict[key]
        step_list = sorted(
            self.scan_step_dict[scan_step_obj.scan_step][scan_step_obj.meas_num][
                scan_step_obj.modulator_state
            ][scan_step_obj.sub_repeat_num]
        )
        num_exp = step_list.count(scan_step_obj)
        if num_exp > 1:
            raise ValueError(
                f"More than one exposure detected for a single map scan of a single map step. (Randomly chosen step has {num_exp} exposures)."
            )
        return step_list.index(scan_step_obj) + 1  # Here we decide that map scan indices start at 1


class NumMapScansBud(MapScanStemBase):
    """Bud for determining the total number of dsps repeats.

    Also checks that all scan steps have the same number of dsps repeats.
    """

    def __init__(self):
        super().__init__(stem_name=CryonirspBudName.num_map_scans.value)

    def getter(self, key: str) -> int:
        """Compute the total number of dsps repeats.

        The number of map_scans for every scan step are calculated and if a map_scan is incomplete,
        it will not be included.
        Assumes the incomplete map_scan is always the last one due to summit abort or cancellation.
        """
        map_scans_per_scan_step = []
        for meas_dict in self.scan_step_dict.values():
            for mod_dict in meas_dict.values():
                for sub_repeat_dict in mod_dict.values():
                    files_per_subrepeat = []
                    for file_list in sub_repeat_dict.values():
                        files_per_subrepeat.append(len(file_list))
                    map_scans_per_scan_step.append(files_per_subrepeat[0])

        if min(map_scans_per_scan_step) + 1 < max(map_scans_per_scan_step):
            raise ValueError("More than one incomplete map exists in the data.")
        return min(map_scans_per_scan_step)
