import pathlib
import sqlite3
import os

import config
from src.logger import log

def initialize_database():
    """Initialises database by creating file and adding missing columns."""
    os.makedirs("data", exist_ok=True)
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS stars (id INTEGER PRIMARY KEY)")
    log(f"Database core file verified at {config.DATABASE_PATH}")

    core_gaia_columns = [
        "ra_deg REAL",
        "dec_deg REAL",
        "parallax_mas REAL",
        "parallax_error REAL",
        "ruwe REAL",
        "astrometric_excess_noise REAL",
        "phot_g_mean_mag REAL",
        "phot_bp_mean_mag REAL",
        "phot_rp_mean_mag REAL",
        "bp_rp REAL",
        "phot_g_mean_flux_over_error REAL",
        "radial_velocity REAL",
        "phot_variable_flag TEXT"
    ]

    calculated_columns = [
        "absolute_magnitude REAL",
        "distance REAL",
        "color_index REAL",
        "temperature REAL",
        "luminosity REAL"
    ]


    columns = core_gaia_columns + calculated_columns
    log(f"Verifying {len(columns)} database schema columns...")
    for col in columns:
        col_name = col.split()[0]
        try:
            cursor.execute(f"ALTER TABLE stars ADD COLUMN {col};")
            log(f"Schema updated: Added column '{col_name}'")
            # ADD LOGS HERE
        except sqlite3.OperationalError:
            pass
    connection.commit()
    connection.close()

    log("Database initialization complete", level="INFO")

def add_star(data_dict: dict):
    """Inserts any number of rows into the stars table using a dictionary"""
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()

    columns = ", ".join(data_dict.keys())
    placeholders = ", ".join(["?"] * len(data_dict))
    sql = f"INSERT INTO stars ({columns}) VALUES ({placeholders})"

    try:
        cursor.execute(sql, tuple(data_dict.values()))
        connection.commit()
        log(f"Successfully stored target ID {data_dict.get('id')} to local database")
    except sqlite3.IntegrityError:
        log(f"Target ID {data_dict.get('id')} already exists in local database. Skipping", level="warn")
    except Exception as e:
        log(f"Failed database write operation: {e} Star ({data_dict.get('id')}) not saved", level="error")
    finally:
        connection.close()

def fetch_star(source_id):
    """Returns saved data on a certain star based on source ID"""
    connection = sqlite3.connect(config.DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    sql = f"SELECT * FROM stars WHERE id = {source_id};"

    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        log(f"Successfully retrieved data of star {source_id} from local database")
        if results is None:
            log(f"No data found for star {source_id}", level="error")
            return None
        return results
    except Exception as e:
        log(f"Failed to retrieve data of star {source_id} Error: {e}", level="error")
        return None
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

