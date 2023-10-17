"""List of intermediate task names."""
from enum import Enum


class CryonirspTaskName(str, Enum):
    """Controlled list of CryoNirsp task tag names."""

    beam_boundaries = "BEAM_BOUNDARIES"
    bad_pixel_map = "BAD_PIXEL_MAP"
    polcal_dark = "POLCAL_DARK"
    polcal_gain = "POLCAL_GAIN"


# TODO: Move this to `*-common`
class TaskName(str, Enum):
    """Controlled list of task tag names."""

    observe = "OBSERVE"
    polcal = "POLCAL"
    dark = "DARK"
    gain = "GAIN"
    geometric = "GEOMETRIC"
    lamp_gain = "LAMP_GAIN"
    solar_gain = "SOLAR_GAIN"
    geometric_angle = "GEOMETRIC_ANGLE"
    geometric_offsets = "GEOMETRIC_OFFSETS"
    geometric_spectral_shifts = "GEOMETRIC_SPEC_SHIFTS"
    demodulation_matrices = "DEMOD_MATRICES"
