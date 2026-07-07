import time
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

def format_time(seconds):
    if seconds == 0:
        return "0 seconds"

    intervals = (
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1)
    )

    parts = []
    for name, count in intervals:
        value = seconds // count
        if value > 0:
            seconds %= count
            unit_name = name[:-1] if value == 1 else name
            parts.append(f"{value} {unit_name}")

    if len(parts) == 1:
        return parts[0]
    else:
        return ", ".join(parts[:-1]) + f" and {parts[-1]}"

def run_ingestion(limit: int):
    """Orchestrates the downloading, processing, and database storage of stellar data."""
    from src.scraper import fetch_bulk
    from src.database import add_star

    start_time = time.time()

    log(f"Initiating bulk retrieval for {limit} targets...", level="INFO")
    results = fetch_bulk(limit)
    total = len(results) if results else 0

    if total == 0:
        log("No star data returned from the Gaia registry. Exiting pipeline.", level="CRITICAL")
        return

    if total != limit:
        log(f"Stellar payload mismatch: Received {total} results, expected {limit}.", level="WARN")

    log(f"Beginning pipeline execution layout for {total} stars...", level="INFO")

    success_count = 0
    for idx, row in enumerate(results):
        current_star_num = idx + 1
        num_updates = 100
        update_every = max(1, int(total / num_updates))

        final_record = process_star(row)

        if final_record:
            add_star(final_record)
            success_count += 1
        else:
            log(f"Pipeline dropped star row at index {idx}: process_star returned None.", level="ERROR")

        if current_star_num % update_every == 1:
            elapsed = time.time() - start_time
            per_star = elapsed / current_star_num
            time_estimate = (total - current_star_num) * per_star
            log(f"Completed {current_star_num}/{total} stars ({round(current_star_num / total, 2)}%) Est. {format_time(time_estimate)} remaining")

    elapsed_time = time.time() - start_time
    per_star_latency = elapsed_time / total if total > 0 else 0

    log(f"Ingestion complete. Successfully committed {success_count}/{total} records to database. ", level="CLI")
    log(f"Total time: {elapsed_time:.2f}s | Multi-target average: {per_star_latency:.4f}s per star.", level="CLI")