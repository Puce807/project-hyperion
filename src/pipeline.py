from src.logger import log
from src.physics import find_distance, find_luminosity, find_colour_index, find_absolute_magnitude, estimate_temperature

def safe_float(val):
    if val in (None, "NOT_AVAILABLE") or str(val).strip() == "":
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def process_star(row):
    """Takes raw data returned from Gaia query and constructs dictionary for use in add_star function in database.py
    pipeline.py computes all calculated fields."""

    try:
        source_id = int(row["source_id"])
        log(f"Processing calculations for target: {source_id}...")
    except Exception as e:
        log(f"Failed to parse critical field `source_id` from row: {e}", level="error")
        return None

    try:
        ra = safe_float(row["ra"])
        dec = safe_float(row["dec"])
        parallax = safe_float(row["parallax"])
        parallax_error = safe_float(row["parallax_error"])
        ruwe = safe_float(row["ruwe"])
        excess_noise = safe_float(row["astrometric_excess_noise"])
        g_mag = safe_float(row["phot_g_mean_mag"])
        bp_mag = safe_float(row["phot_bp_mean_mag"])
        rp_mag = safe_float(row["phot_rp_mean_mag"])
        bp_rp = safe_float(row["bp_rp"])
        flux = safe_float(row["phot_g_mean_flux"])
        flux_error = safe_float(row["phot_g_mean_flux_error"])
        flux_over_error = safe_float(row["phot_g_mean_flux_over_error"])
        rv_amplitude_robust = safe_float(row["rv_amplitude_robust"])
        radial_velocity = safe_float(row["radial_velocity"])
        radial_velocity_error = safe_float(row["radial_velocity_error"])
        pmra = safe_float(row["pmra"])
        pmdec = safe_float(row["pmdec"])

        phot_g_n_obs = int(row["phot_g_n_obs"]) if row["phot_g_n_obs"] not in (None, "NOT_AVAILABLE") else None
        phot_bp_n_obs = int(row["phot_bp_n_obs"]) if row["phot_bp_n_obs"] not in (None, "NOT_AVAILABLE") else None
        phot_rp_n_obs = int(row["phot_rp_n_obs"]) if row["phot_rp_n_obs"] not in (None, "NOT_AVAILABLE") else None

        variable_flag = str(row["phot_variable_flag"]) if row["phot_variable_flag"] not in (None,
                                                                                            "NOT_AVAILABLE") else "NOT_AVAILABLE"
        has_epoch_photometry = bool(row["has_epoch_photometry"]) if row["has_epoch_photometry"] is not None else False

    except (TypeError, ValueError) as e:
        log(f"Skipping star {source_id}, critical error: {e}", level="error")
        return None

    # --- Calculations ---

    distance = find_distance(parallax)
    colour_index = find_colour_index(bp_mag, rp_mag) if bp_rp is None else bp_rp
    temperature = estimate_temperature(colour_index)

    abs_mag = float(find_absolute_magnitude(g_mag, distance)) if distance is not None else None
    luminosity = float(find_luminosity(abs_mag)) if abs_mag is not None else None

    log(f"Calculations complete for {source_id}", level="INFO")

    db_record = {
        "id": source_id,
        "ra": ra,
        "dec": dec,
        "parallax": parallax,
        "parallax_error": parallax_error,
        "ruwe": ruwe,
        "astrometric_excess_noise": excess_noise,
        "phot_g_mean_mag": g_mag,
        "phot_bp_mean_mag": bp_mag,
        "phot_rp_mean_mag": rp_mag,
        "bp_rp": colour_index,
        "phot_g_mean_flux": flux,
        "phot_g_mean_flux_error": flux_error,
        "phot_g_mean_flux_over_error": flux_over_error,
        "radial_velocity": radial_velocity,
        "radial_velocity_error": radial_velocity_error,
        "phot_variable_flag": variable_flag,
        "rv_amplitude_robust": rv_amplitude_robust,
        "has_epoch_photometry": has_epoch_photometry,
        "pmra": pmra,
        "pmdec": pmdec,
        "phot_g_n_obs": phot_g_n_obs,
        "phot_bp_n_obs": phot_bp_n_obs,
        "phot_rp_n_obs": phot_rp_n_obs,

        # Computed fields
        "distance": distance,
        "temperature": temperature,
        "colour_index": colour_index,
        "absolute_magnitude": abs_mag,
        "luminosity": luminosity
    }

    # NOTE: When changing this file, ensure fields in initialise_database (src/database.py) correlate

    return db_record