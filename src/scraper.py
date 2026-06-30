from astroquery.gaia import Gaia

Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source" # TODO: ADD TO CONFIG FILE

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

def fetch_data():
    # TODO: Add error handling
    job = Gaia.launch_job(adql_query) # Change to async later
    results = job.get_results()
    return results

def fetch_individual_star(source_id):
    query = f"""
                 SELECT 
                    source_id, ra, dec, parallax, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag
                 FROM
                     gaiadr3.gaia_source
                 WHERE
                     source_id = {source_id}
                     AND parallax IS NOT NULL
                     AND parallax_error IS NOT NULL
                     AND ruwe IS NOT NULL
                     AND phot_g_mean_mag IS NOT NULL
                     AND phot_g_mean_mag IS NOT NULL
                     AND phot_g_mean_flux_over_error IS NOT NULL
                     AND phot_bp_mean_mag IS NOT NULL
                     AND phot_rp_mean_mag IS NOT NULL
                     AND parallax > 0
                 """
    job = Gaia.launch_job(query)
    return job.get_results()