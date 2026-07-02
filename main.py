import shutil
import time
from src.logger import log
from pathlib import Path
from src.physics import find_distance, find_luminosity, find_colour_index, find_absolute_magnitude, estimate_temperature
from src.scraper import fetch_data
from src.database import initialize_database, add_star

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.py"
DEFAULTS_FILE = BASE_DIR / "config.defaults.py"

if not CONFIG_FILE.exists():
    shutil.copy(DEFAULTS_FILE, CONFIG_FILE)
import config

if __name__ == "__main__":
    log("Hyperion pipeline starting...")
    log("Initializing database...")
    initialize_database()
    log("Database initialized successfully")

    stars_to_fetch = 10
    start = time.time()
    results = fetch_data(stars_to_fetch)
    print(results)
    if not results or len(results) == 0:
        log("No star data returned from scraper. Exiting pipeline", level="critical")
        exit()
    if len(results) != stars_to_fetch:
        log(f"Number of received results ({len(results)}) does not match expected amount ({stars_to_fetch})", level="warn")

    for row in results:
        source_id = int(row["source_id"])
        log(f"Processing calculations for target: {source_id}...")

        distance = find_distance(float(row["parallax"]))
        temp = estimate_temperature(float(row["bp_rp"]))
        abs_mag = float(find_absolute_magnitude(row["phot_g_mean_mag"], distance))
        luminosity = float(find_luminosity(abs_mag))

        data_dict = {
            "id": source_id,
            "ra_deg": float(row["ra"]),
            "dec_deg": float(row["dec"]),
            "parallax_mas": float(row["parallax"]),
            "parallax_error": float(row["parallax_error"]),
            "ruwe": float(row["ruwe"]),
            "astrometric_excess_noise": float(row["astrometric_excess_noise"]),
            "phot_g_mean_mag": float(row["phot_g_mean_mag"]),
            "phot_bp_mean_mag": float(row["phot_bp_mean_mag"]),
            "phot_rp_mean_mag": float(row["phot_rp_mean_mag"]),
            "bp_rp": float(row["bp_rp"]),
            "phot_g_mean_flux_over_error": float(row["phot_g_mean_flux_over_error"]),
            "phot_variable_flag": str(row["phot_variable_flag"])
        }

        calc_dict = {
            "distance": distance,
            "temperature": temp,
            "absolute_magnitude": abs_mag,
            "luminosity": luminosity
        }

        log(f"Calculations complete for {source_id}. Handing record to database.", level="INFO")
        final_record = data_dict | calc_dict
        add_star(final_record)
    length = time.time() - start
    per_star = length / len(results)
    log(f"Processed {len(results)} stars in {round(length, 2)} seconds. Average {round(per_star, 4)}s per star")


