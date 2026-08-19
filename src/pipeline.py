import time
from uuid import uuid4
from dataclasses import fields
import config
from src.logger import log
from src.physics import find_distance, find_luminosity, find_colour_index, find_absolute_magnitude, estimate_temperature
from src.models import Star, SourceID, GaiaData, ZTFData
from src.scraper import fetch_data
from src.database import add_star

def clean_val(val):
    if val in (None, "NOT_AVAILABLE") or str(val).strip() == "":
        return None
    if isinstance(val, bool):
        return val
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def process_star(row, source):
    """Takes raw data returned from Gaia query and constructs star dataclass."""
    if source not in config.allowed_sources:
        log(f"Skipping star; unknown source {source}", level="error")
        return None
    try:
        source_id = None
        if source == "gaia":
            source_id = SourceID(catalogue="gaia", id=str(row["source_id"]))
        elif source == "ztf":
            source_id = SourceID(catalogue="ztf", id=str(row["oid"]))
        # TODO: Check if source ID is in table before creating new ID
    except Exception as e:
        log(f"Failed to parse critical field from row: {e}", level="error")
        return None

    hyperion_id = f"H_{uuid4()}"
    gaia_data = None
    ztf_data = None
    try:
        if source == "gaia":
            gaia_data = GaiaData(
                **{
                    field.name: clean_val(row[field.name])
                    for field in fields(GaiaData)
                }
            )
        elif source == "ztf":
            ztf_data = ZTFData(
                **{
                    field.name: clean_val(row[field.name])
                    for field in fields(ZTFData)
                }
            )
        star = Star(id=hyperion_id,
                    ra = clean_val(row["ra"]),
                    dec = clean_val(row["dec"]),
                    source_ids = [source_id],
                    gaia_data = gaia_data,
                    ztf_data = ztf_data
                    )
    except (TypeError, ValueError) as e:
        log(f"Skipping star {source_id}, critical error: {e}", level="error")
        return None

    # Changed so calculations are not stored in DB for now. They can be calculated on demand.
    # TODO: Add ability for user to change GAIA fields

    return star

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
    DATA_SOURCE = "ztf" # TODO: Move
    start_time = time.time()

    log(f"Initiating bulk retrieval for {limit} targets...", level="INFO")
    results = fetch_data(limit=limit, source=DATA_SOURCE)
    total = len(results) if results else 0

    if total == 0:
        log("No star data returned. Exiting pipeline.", level="CRITICAL")
        return

    if total != limit:
        log(f"Stellar payload mismatch: Received {total} results, expected {limit}.", level="WARN")

    log(f"Beginning pipeline execution layout for {total} stars...", level="INFO")

    success_count = 0
    num_updates = 100
    update_every = max(1, int(total / num_updates))
    for idx, row in enumerate(results):
        current_star_num = idx + 1

        final_record = process_star(row, DATA_SOURCE)

        if final_record:
            add_star(final_record)
            # TODO: Change to bulk adding
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