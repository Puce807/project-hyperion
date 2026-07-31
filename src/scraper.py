from astroquery.gaia import Gaia
from src.logger import log
import config

Gaia.MAIN_GAIA_TABLE = config.GAIA_TABLE

GAIA_QUALITY_FILTERS = """
    parallax IS NOT NULL
    AND parallax_error IS NOT NULL
    AND parallax_over_error IS NOT NULL
    AND ruwe IS NOT NULL
    AND phot_g_mean_mag IS NOT NULL
    AND phot_g_mean_flux_over_error IS NOT NULL
    AND phot_bp_mean_mag IS NOT NULL
    AND phot_rp_mean_mag IS NOT NULL
    AND parallax > 0
    AND phot_bp_rp_excess_factor BETWEEN 1.0 AND 1.8
    AND parallax_over_error > 10
    AND phot_g_mean_flux_over_error > 50
    AND phot_bp_mean_flux_over_error > 20
    AND phot_rp_mean_flux_over_error > 20
    AND ruwe <= 1.4
"""

def execute_gaia_query(adql_query: str):
    """Helper function to handle job execution"""
    try:
        job = Gaia.launch_job(adql_query)
        results = job.get_results()
        log(f"Gaia query executed successfully. Retrieved {len(results)} rows.")
        return results

    except Exception as e:
        error_msg = str(e).lower()
        response = getattr(e, 'response', None)
        status_code = getattr(response, 'status_code', None)

        if status_code == 503 or "not appear to be a votable" in error_msg or "maintenance" in error_msg:
            log("Could not execute Gaia query: Gaia Archive is currently under maintenance.", level="warning")
        else:
            log(f"Could not execute Gaia query (HTTP {status_code or 'Unknown'}): {e}", level="error")

        return None

        log(f"Could not execute Gaia query: {e}", level="error")
        return None

def fetch_bulk(limit: int=1):
    """Fetches a sample of stars for testing"""
    query = f"""
        SELECT TOP {limit}
            {config.GAIA_FIELDS}
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
            {config.GAIA_FIELDS}
        FROM 
            gaiadr3.gaia_source
        WHERE 
            source_id = {source_id}
            AND {GAIA_QUALITY_FILTERS}
        """
    results = execute_gaia_query(query)
    if results and len(results) > 0:
        return results[0]
    else:
        log("No results found", level="error")
        return None

