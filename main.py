import shutil
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

    results = fetch_data()
    if not results or len(results) == 0:
        log("No star data returned from scraper. Exiting pipeline", level="critical")
        exit()

    source_id = int(results["source_id"][0])
    distance = find_distance(float(results["parallax"][0]))
    temp = estimate_temperature(float(results["bp_rp"][0]))
    abs_mag = float(find_absolute_magnitude(results["phot_g_mean_mag"][0], distance))
    luminosity = float(find_luminosity(abs_mag))

    data_dict = {
        "id": source_id,
        "ra_deg": float(results["ra"][0]),
        "dec_deg": float(results["dec"][0]),
        "parallax_mas": float(results["parallax"][0]),
        "parallax_error": float(results["parallax_error"][0]),
        "ruwe": float(results["ruwe"][0]),
        "astrometric_excess_noise": float(results["astrometric_excess_noise"][0]),
        "phot_g_mean_mag": float(results["phot_g_mean_mag"][0]),
        "phot_bp_mean_mag": float(results["phot_bp_mean_mag"][0]),
        "phot_rp_mean_mag": float(results["phot_rp_mean_mag"][0]),
        "bp_rp": float(results["bp_rp"][0]),
        "phot_g_mean_flux_over_error": float(results["phot_g_mean_flux_over_error"][0]),
        "phot_variable_flag": str(results["phot_variable_flag"][0])
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

    # Next: Error handling, SQL database1
