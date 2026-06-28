import astropy.units as u
import math
from astroquery.gaia import Gaia

Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"

adql_query = """
SELECT TOP 1
    source_id, ra, dec, parallax, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag
FROM
    gaiadr3.gaia_source
WHERE
    parallax IS NOT NULL
    AND parallax_error IS NOT NULL
    AND ruwe IS NOT NULL
    AND phot_g_mean_mag IS NOT NULL
    AND phot_g_mean_mag IS NOT NULL
    AND phot_g_mean_flux_over_error IS NOT NULL
    AND phot_bp_mean_mag IS NOT NULL
    AND phot_rp_mean_mag IS NOT NULL
    AND parallax > 0
"""

def find_distance(parallax_mas: float) -> float:
    """Calculates distance in Parsecs using parallax angle in milliarcseconds"""
    return 1000 / parallax_mas

def find_colour_index(bp: float, rp: float) -> float:
    """Calculates color index (surface temperature of a star)"""
    return bp - rp

def find_absolute_magnitude(apparent_magnitude: float, distance_parsecs: float) -> float:
    """Calculate absolute magnitude using the distance modulus formula."""
    return apparent_magnitude - 5 * math.log10(distance_parsecs) + 5

def estimate_temperature(colour_index: float) -> float:
    """Estimate stellar effective temperature from BP-RP colour index."""
    return 4600 * (1 / (0.92 * colour_index + 1.7) + 1 / (0.92 * colour_index + 0.62))

def find_luminosity(absolute_magnitude: float) -> float:
    """Calculate luminosity relative to the sun (L☉) from absolute magnitude"""
    sun_absolute_magnitude = 4.83
    return 10 ** ((sun_absolute_magnitude - absolute_magnitude) / 2.5)


job = Gaia.launch_job(adql_query) # Change to async later
results = job.get_results()
results.pprint_all()

distance = find_distance(results["parallax"][0])
ci = find_colour_index(results["phot_bp_mean_mag"][0],results["phot_rp_mean_mag"][0])
temp = estimate_temperature(ci)
abs_mag = find_absolute_magnitude(results["phot_g_mean_mag"][0], distance)
luminosity = find_luminosity(abs_mag)
print("Distance: ", distance)
print("CI: ", ci)
print("Temp: ", temp)
print("Absolute Magnitude: ", abs_mag)
print("Luminosity: ", luminosity)

# Next: Error handling, SQL database1