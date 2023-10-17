"""Cryonirsp polarimeter mode parser."""
from typing import Type

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.parsers.unique_bud import UniqueBud

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess


class ModulatorSpinModeBud(UniqueBud):
    """Bud for finding modulator spin mode in observe and polcal data."""

    def __init__(self):
        self.metadata_key = "modulator_spin_mode"
        super().__init__(
            constant_name=CryonirspBudName.modulator_spin_mode.value,
            metadata_key=self.metadata_key,
        )

    def setter(self, fits_obj: CryonirspL0FitsAccess) -> Type[SpilledDirt] | str:
        """
        Setter for the bud.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type != "observe" and fits_obj.ip_task_type != "polcal":
            return SpilledDirt
        return getattr(fits_obj, self.metadata_key)
