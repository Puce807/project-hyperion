from astroquery.gaia import Gaia
from src.logger import log
import config

Gaia.MAIN_GAIA_TABLE = config.GAIA_TABLE

GAIA_FIELDS = """
source_id, ra, dec, parallax, parallax_error, ruwe, 
    astrometric_excess_noise, phot_g_mean_mag, phot_bp_mean_mag, 
    phot_rp_mean_mag, bp_rp, phot_g_mean_flux_over_error, 
    radial_velocity, phot_variable_flag"""
GAIA_QUALITY_FILTERS = """
    parallax IS NOT NULL
    AND parallax_error IS NOT NULL
    AND ruwe IS NOT NULL
    AND phot_g_mean_mag IS NOT NULL
    AND phot_g_mean_flux_over_error IS NOT NULL
    AND phot_bp_mean_mag IS NOT NULL
    AND phot_rp_mean_mag IS NOT NULL
    AND parallax > 0
"""

def execute_gaia_query(adql_query: str):
    """Helper function to handle job execution"""
    try:
        job = Gaia.launch_job(adql_query)
        results = job.get_results()
        log(f"Gaia query executed successfully. Retrieved {len(results)} rows.")
        return results
    except Exception as e:
        print(e)
        log(f"Could not execute Gaia query: {e}", level="error")
        return None

def fetch_bulk(limit: int=1):
    """Fetches a sample of stars for testing"""
    query = f"""
        SELECT TOP {limit}
            {GAIA_FIELDS}
        FROM 
            gaiadr3.gaia_source
        WHERE 
            {GAIA_QUALITY_FILTERS}
        """
    return execute_gaia_query(query)

def fetch_data(limit):
    results = fetch_bulk(limit)
    return results

def fetch_individual_star(source_id):
    """Queries Gaia for specific target by source_id"""
    query = f"""
        SELECT TOP 1
            {GAIA_FIELDS}
        FROM 
            gaiadr3.gaia_source
        WHERE 
            source_id = {source_id}
            AND {GAIA_QUALITY_FILTERS}
        LIMIT 1
        """
    results = execute_gaia_query(query)
    if results and len(results) > 0:
        return results[0]
    else:
        log("No results found", level="error")
        return None

