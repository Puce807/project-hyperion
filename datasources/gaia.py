from dataclasses import fields
from uuid import uuid4
from astroquery.gaia import Gaia
from src.logger import log
from src.models import Star, SourceID, GaiaData
from .utils import clean_val
from .base import DataSource
import config

class GaiaDataSource(DataSource):
    name = "gaia"
    table = "gaia_data"
    query_fields = {
        "source_id": str,
        "ra": float,
        "dec": float,
        "parallax": float,
        "parallax_error": float,
        "parallax_over_error": float,
        "phot_bp_mean_mag": float,
        "phot_rp_mean_mag": float,
        "phot_g_mean_mag": float,
        "bp_rp": float
    }
    query_fields_str = ", ".join(query_fields.keys())
    # TODO: Improve quality filters
    quality_filters = """
        parallax IS NOT NULL
        AND parallax_error IS NOT NULL
        AND parallax_over_error IS NOT NULL
        AND phot_g_mean_mag IS NOT NULL
        AND phot_bp_mean_mag IS NOT NULL
        AND phot_rp_mean_mag IS NOT NULL
        AND parallax > 0
    """
    schema = """
        gaia_id TEXT NOT NULL,
        parallax REAL,
        parallax_error REAL,
        parallax_over_error REAL,
        phot_bp_mean_mag REAL,
        phot_rp_mean_mag REAL,
        phot_g_mean_mag REAL,
        bp_rp REAL"""
    database_fields = [
        "hyperion_id",
        "gaia_id",
        "parallax",
        "parallax_error",
        "parallax_over_error",
        "phot_bp_mean_mag",
        "phot_rp_mean_mag",
        "phot_g_mean_mag",
        "bp_rp",
    ]
    source = "gaiadr3.gaia_source"

    def fetch(self, limit=1):
        """Fetch data from Gaia catalogue"""
        query = f"""
                SELECT TOP {limit}
                    {self.query_fields_str}
                FROM 
                    {self.source}
                WHERE 
                    {self.quality_filters}
                """
        try:
            job = Gaia.launch_job(query)
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

    def normalise(self, data):
        """Convert source-specific data into Hyperion data model"""
        hyperion_id = f"H_{uuid4()}"
        source_id = SourceID(catalogue=self.name, id=str(data["source_id"]))
        gaia_data = GaiaData(
            **{
                field.name: clean_val(data[field.name])
                for field in fields(GaiaData)
            }
        )
        star = Star(id=hyperion_id,
                    ra = clean_val(data["ra"]),
                    dec = clean_val(data["dec"]),
                    source_ids = [source_id],
                    gaia_data = gaia_data,
                    ztf_data = None
                    )
        return star