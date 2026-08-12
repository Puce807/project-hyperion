import time
from src.logger import log
from src.physics import find_distance, find_luminosity, find_colour_index, find_absolute_magnitude, estimate_temperature
from config import GAIA_FIELDS_LIST

def clean_val(val):
    if val in (None, "NOT_AVAILABLE") or str(val).strip() == "":
        return None
    if isinstance(val, bool):
        return val
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

    safe_values = {}
    try:
        for key in GAIA_FIELDS_LIST:
            safe_values[key] = clean_val(row[key])
    except (TypeError, ValueError) as e:
        log(f"Skipping star {source_id}, critical error: {e}", level="error")
        return None
    safe_values["id"] = safe_values.pop("source_id")

    # --- Calculations ---

    distance = find_distance(safe_values["parallax"])
    colour_index = find_colour_index(safe_values["phot_bp_mean_mag"], safe_values["phot_rp_mean_mag"]) if safe_values["bp_rp"] is None else safe_values["bp_rp"]
    temperature = estimate_temperature(colour_index)

    absolute_magnitude = float(find_absolute_magnitude(safe_values["phot_g_mean_mag"], distance)) if distance is not None else None
    luminosity = float(find_luminosity(absolute_magnitude)) if absolute_magnitude is not None else None

    computed_fields = dict(distance=distance, colour_index=colour_index, temperature=temperature, absolute_magnitude=absolute_magnitude, luminosity=luminosity)
    db_record = safe_values | computed_fields

    # NOTE: When changing this file, ensure fields in initialise_database (config.py) correlate
    # TODO: Add ability for user to change GAIA fields

    return db_record

def format_time(seconds):
    if seconds == 0:
        return "0 seconds"
    if seconds <= 1:
        return f"{round(seconds, 2)} seconds"

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
            log(f"Completed {current_star_num}/{total} stars ({round(current_star_num / total, 4)*100}%) Est. {format_time(time_estimate)} remaining")

    elapsed_time = time.time() - start_time
    per_star_latency = elapsed_time / total if total > 0 else 0

    log(f"Ingestion complete. Successfully committed {success_count}/{total} records to database. ", level="CLI")
    log(f"Total time: {elapsed_time:.2f}s | Multi-target average: {per_star_latency:.4f}s per star.", level="CLI")