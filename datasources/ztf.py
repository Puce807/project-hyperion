from dataclasses import fields
from uuid import uuid4
from astroquery.ipac.irsa import Irsa
from src.logger import log
from src.models import Star, SourceID, ZTFData
from src.pipeline import clean_val
from .base import DataSource
import config

class ZTFDataSource(DataSource):
    name = "ztf"
    table = "ztf_data"
    query_fields = {
        "oid": str,
        "ra": float,
        "dec": float,
        "filtercode": str,
        "nobs": int,
        "ngoodobs": int,
        "weightedmeanmag": float,
        "weightedmagrms": float,
        "chisq": float
    }
    query_fields_str = ", ".join(query_fields.keys())
    # TODO: Make quality filters better
    quality_filters = """
        nobs IS NOT NULL
        AND nobs > 20
        AND chisq IS NOT NULL
        AND filtercode IS NOT NULL"""
    schema = """
        ztf_id TEXT NOT NULL,
        filtercode TEXT,
        nobs REAL,
        ngoodobs REAL,
        weightedmeanmag REAL,
        weightedmagrms REAL,
        chisq REAL"""
    source = "ztf_objects_dr24"

    def fetch(self, limit=1):
        """Fetch data from ZTF catalogue"""
        # TODO NEXT: Ensure column names are correct
        try:
            result = Irsa.query_tap(f'''SELECT TOP {limit}
                                    {self.query_fields_str}
                                  FROM {self.source}
                                  WHERE {self.quality_filters}
                                  ''')
        except Exception as e:
            log(f"Could not execute ZTF tap query: {e}", level="error")
            return None
        return result

    def normalise(self, data):
        """Convert source-specific data into Hyperion data model"""
        hyperion_id = f"H_{uuid4()}"
        source_id = SourceID(catalogue=self.name, id=str(data["oid"]))
        ztf_data = ZTFData(
            **{
                field.name: clean_val(data[field.name])
                for field in fields(ZTFData)
            }
        )
        star = Star(id=hyperion_id,
                    ra = clean_val(data["ra"]),
                    dec = clean_val(data["dec"]),
                    source_ids = [source_id],
                    gaia_data = None,
                    ztf_data = ztf_data
                    )
        return star