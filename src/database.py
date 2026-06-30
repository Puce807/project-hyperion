import pathlib
import sqlite3
import os
import config


def initialize_database():
    """Initialises database by creating file and adding missing columns."""

    os.makedirs("data", exist_ok=True)
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS stars (id INTEGER PRIMARY KEY)")

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

    for col in columns:
        col_name = col.split()[0]
        try:
            cursor.execute(f"ALTER TABLE stars ADD COLUMN {col};")
            # ADD LOGS HERE
        except sqlite3.OperationalError:
            pass
    connection.commit()
    connection.close()

def add_star(data_dict: dict):
    """Inserts any number of rows into the stars table using a dictionary"""
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()

    columns = ", ".join(data_dict.keys())
    placeholders = ", ".join(["?"] * len(data_dict))
    sql = f"INSERT INTO stars ({columns}) VALUES ({placeholders})"

    cursor.execute(sql, tuple(data_dict.values()))
    connection.commit()

if __name__ == "__main__":
    initialize_database()

