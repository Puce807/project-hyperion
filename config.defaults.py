from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "data" / "data.db"

GAIA_TABLE = "gaiadr3.gaia_source"

GAIA_FIELDS = """
source_id, ra, dec, parallax, parallax_error, parallax_over_error, ruwe, 
    astrometric_excess_noise, phot_g_mean_mag, phot_bp_mean_mag, 
    phot_rp_mean_mag, bp_rp, 
    phot_g_mean_flux_over_error, phot_g_mean_flux_error, phot_g_mean_flux,
    radial_velocity, radial_velocity_error, 
    phot_variable_flag, rv_amplitude_robust, has_epoch_photometry,
    pmra, pmdec, phot_g_n_obs, phot_bp_n_obs, phot_rp_n_obs, teff_gspphot"""
GAIA_FIELDS_LIST = [field.strip() for field in GAIA_FIELDS.split(",") if field.strip()]

FIELD_PRESETS = {
    "default": ["id", "ra", "dec", "phot_g_mean_mag", "parallax"],
    "quality": ["id", "ruwe", "parallax_over_error", "phot_g_mean_flux_over_error"],
    "photometry": ["id", "phot_g_mean_mag", "phot_bp_mean_mag", "phot_rp_mean_mag", "bp_rp"],
    "astrometry": ["id", "ra", "dec", "pmra", "pmdec", "parallax"],
    "variability": ["id", "phot_g_mean_mag", "phot_g_mean_flux_over_error", "bp_rp", "has_epoch_photometry", "phot_variable_flag"],
    "all": GAIA_FIELDS_LIST
}
