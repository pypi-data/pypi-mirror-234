"""Cryo filter list and tooling."""
import astropy.units as u
from dkist_processing_common.models.wavelength import WavelengthRange


class Filter(WavelengthRange):
    """
    CRYONirsp filter data structure.

    Parameters
    ----------
    filter_id
        Unique ID of the filter in use
    """

    filter_id: str


CRYONIRSP_CI_FILTERS = [
    Filter(filter_id="Continuum", min=1049.000 * u.nm, max=1050.000 * u.nm),
    Filter(filter_id="FeXIII1075", min=1074.200 * u.nm, max=1075.200 * u.nm),
    Filter(filter_id="FeXIII1080", min=1079.300 * u.nm, max=1080.300 * u.nm),
    Filter(filter_id="HeI", min=1082.500 * u.nm, max=1083.500 * u.nm),
    Filter(filter_id="HPaschen-beta", min=1281.300 * u.nm, max=1282.300 * u.nm),
    Filter(filter_id="JBand", min=1170.000 * u.nm, max=1330.000 * u.nm),
    Filter(filter_id="SiX", min=1427.500 * u.nm, max=1432.500 * u.nm),
]


def find_associated_ci_filter(filter_id: str) -> Filter:
    """
    Given a wavelength, find the Filter that contains that wavelength between its wavemin/wavemax.

    Parameters
    ----------
    filter_id
        Unique ID of the filter in use

    Returns
    -------
    A Filter object that contains the wavelength
    """
    matching_filters = [f for f in CRYONIRSP_CI_FILTERS if f.filter_id == filter_id]
    if len(matching_filters) == 1:
        return matching_filters[0]
    raise ValueError(f"Found {len(matching_filters)} matching filters when 1 was expected.")
