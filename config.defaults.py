from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "data" / "data.db"

SOURCES = ["ztf", "gaia"]

GAIA_TABLE = "gaiadr3.gaia_source"
GAIA_FIELDS = """
source_id, ra, dec, 
parallax, parallax_error, parallax_over_error, 
phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag, bp_rp """
GAIA_FIELDS_LIST = [field.strip() for field in GAIA_FIELDS.split(",") if field.strip()]

FIELD_PRESETS = {
    "default": ["id", "ra", "dec", "phot_g_mean_mag", "parallax"],
    "quality": ["id", "ruwe", "parallax_over_error", "phot_g_mean_flux_over_error"],
    "photometry": ["id", "phot_g_mean_mag", "phot_bp_mean_mag", "phot_rp_mean_mag", "bp_rp"],
    "astrometry": ["id", "ra", "dec", "pmra", "pmdec", "parallax"],
    "variability": ["id", "phot_g_mean_mag", "phot_g_mean_flux_over_error", "bp_rp", "has_epoch_photometry", "phot_variable_flag"],
    "all": GAIA_FIELDS_LIST
}

ZTF_SOURCE = ""
ZTF_FIELDS = """oid, ra, dec, filtercode, nobs, ngoodobs, weightedmeanmag, weightedmagrms, chisq"""
ZTF_FIELDS_LIST = [field.strip() for field in ZTF_FIELDS.split(",") if field.strip()]

TABLES = ["stars", "source_ids", "gaia_data", "ztf_data"]
SAFE_TABLES = ["gaia_data", "ztf_data"] # Tables that are (safe) to delete