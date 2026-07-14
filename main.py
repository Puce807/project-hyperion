import shutil
from src.logger import log
from pathlib import Path
from src.pipeline import  run_ingestion
from src.database import initialize_database

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

    stars_to_fetch = 100000
    run_ingestion(stars_to_fetch)


# TODO: Add docs to explain what Gaia fields do
# TODO: Add CLI docs