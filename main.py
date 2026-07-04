import shutil
import time
from src.logger import log
from pathlib import Path
from src.physics import find_distance, find_luminosity, find_colour_index, find_absolute_magnitude, estimate_temperature
from src.pipeline import process_star
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

    stars_to_fetch = 100
    start = time.time()
    results = fetch_data(stars_to_fetch)
    if not results or len(results) == 0:
        log("No star data returned from scraper. Exiting pipeline", level="critical")
        exit()
    if len(results) != stars_to_fetch:
        log(f"Number of received results ({len(results)}) does not match expected amount ({stars_to_fetch})", level="warn")

    for row in results:
        final_record = process_star(row)
        if final_record:
            add_star(final_record)
        else:
            log("Could not add star to DB as process_star returned None", level="error")
    length = time.time() - start
    per_star = length / len(results)
    log(f"Processed {len(results)} stars in {round(length, 2)} seconds. Average {round(per_star, 4)}s per star")


