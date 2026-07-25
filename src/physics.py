import math
from src.logger import *

def find_distance(parallax_mas: float) -> float | None:
    """Calculates distance in Parsecs using parallax angle in milliarcseconds"""
    if parallax_mas is None or parallax_mas <= 0:
        raise ValueError(f"parallax_mas must be positive, got: {parallax_mas}")
    return 1000 / parallax_mas

def find_colour_index(bp: float, rp: float) -> float | None:
    """Calculates colour index (surface temperature of a star)"""
    if bp is None or rp is None:
        return None

    return bp - rp

def find_absolute_magnitude(apparent_magnitude: float, distance_parsecs: float) -> float | None:
    """Calculate absolute magnitude using the distance modulus formula."""
    if apparent_magnitude is None:
        return None
    if distance_parsecs is None or distance_parsecs <= 0:
        return None

    return apparent_magnitude - 5 * math.log10(distance_parsecs) + 5

def estimate_temperature(colour_index: float) -> float | None:
    """Estimate stellar effective temperature (kelvin) from BP-RP colour index."""
    if colour_index is None:
        return None
    try:
        return 4600 * (1 / (0.92 * colour_index + 1.7) + 1 / (0.92 * colour_index + 0.62))
    except ZeroDivisionError:
        return None

def find_luminosity(absolute_magnitude: float) -> float | None:
    """Calculate luminosity relative to the sun (L☉) from absolute magnitude"""
    sun_absolute_magnitude = 4.83
    if absolute_magnitude is None:
        return None
    return 10 ** ((sun_absolute_magnitude - absolute_magnitude) / 2.5)