import pathlib
import sqlite3
import os
import config
from src.logger import log
from src.models import Star

def initialize_database():
    """Initialises database by creating file and adding missing columns."""
    os.makedirs("data", exist_ok=True)
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("CREATE TABLE IF NOT EXISTS stars (id TEXT PRIMARY KEY)")
    log(f"Database core file verified at {config.DATABASE_PATH}")

    #core_gaia_columns = config.GAIA_FIELDS_LIST

    #integer_fields = ["phot_g_n_obs", "phot_bp_n_obs", "phot_rp_n_obs"]
    #text_fields = ["phot_variable_flag"]
    #boolean_fields = ["has_epoch_photometry"]

    #calculated_columns = [
    #    "absolute_magnitude REAL",
    #    "distance REAL",
    #    "colour_index REAL",
    #    "temperature REAL",
    #    "luminosity REAL"
    #]

    #columns = core_gaia_columns + calculated_columns
    columns = ["ra", "dec"]
    log(f"Verifying {len(columns)} database schema columns...")

    for col in columns:
        col_def = f"{col} REAL"

        try:
            cursor.execute(f"ALTER TABLE stars ADD COLUMN {col_def};")
            log(f"Schema updated: Added telemetry column '{col}' ({col_def.split()[1]})", level="INFO")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                pass
            else:
                log(f"Failed database operation: {e}", level="error")

    connection.commit()
    connection.close()
    log("Database initialization complete", level="INFO")

def add_star(star: Star):
    """Inserts any number of rows into the stars table using a dictionary"""
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO stars (id, ra, dec) VALUES (?, ?, ?)",
            (star.id, star.ra, star.dec)
        )
        connection.commit()
    except sqlite3.IntegrityError as e:
        #log(f"Target ID {star.id} already exists in local database. Skipping", level="warn")
        log(f"Error for star ID {star.id}: {e}", level="error")
    except Exception as e:
        log(f"Failed database write operation: {e} Star ({star.id}) not saved", level="error")
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
        if results is None:
            log(f"No data found for star {source_id}", level="error")
            return None
        log(f"Successfully retrieved data of star {source_id} from local database")
        return results
    except Exception as e:
        log(f"Failed to retrieve data of star {source_id} Error: {e}", level="error")
        return None
    finally:
        connection.close()

def fetch_stars_batch(source_ids=None, fields=None, limit=None):
    """Returns saved data for a list of star source IDs or picks random stars if empty, selecting specific fields"""
    # TODO: Remove fetch_star function as this makes it redundant
    if source_ids is None:
        source_ids = []

    connection = sqlite3.connect(config.DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    columns_clause = ", ".join(fields) if fields else "*"

    query_args = ()
    limit_clause = f" LIMIT {int(limit)}" if limit is not None else ""

    if source_ids:
        placeholders = ", ".join(["?"] * len(source_ids))
        sql = f"SELECT {columns_clause} FROM stars WHERE id IN ({placeholders}){limit_clause};"
        query_args = tuple(source_ids)
        log_msg = f"Querying up to {limit if limit else len(source_ids)} specific target IDs"
    else:
        sql = f"SELECT {columns_clause} FROM stars ORDER BY RANDOM(){limit_clause};"
        log_msg = f"No source IDs provided. Fetching {limit if limit else 'all available'} random stars from local DB"

    log(log_msg, level="INFO")

    try:
        cursor.execute(sql, query_args)
        results = cursor.fetchall()

        log(f"Successfully retrieved {len(results)} records from the local database", level="CLI")
        return results
    except Exception as e:
        log(f"Failed to execute batch/random star retrieval. Error: {e}", level="error")
        return []
    finally:
        connection.close()

def fetch_number():
    """Returns the number of stars in the database"""
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM stars")
    count = cursor.fetchone()[0]
    connection.close()
    return count

def delete_db():
    """Deletes data in local database. Returns True on success, otherwise False"""
    connection = None
    try:
        connection = sqlite3.connect(config.DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM stars")
        connection.commit()
        log("All data deleted from DB successfully")
        return True
    except sqlite3.Error as e:
        log(f"Could not delete DB data: {e}", level="error")
        return False
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    initialize_database()

