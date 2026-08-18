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
    cursor.execute("CREATE TABLE IF NOT EXISTS stars (id TEXT PRIMARY KEY, ra REAL NOT NULL, dec REAL NOT NULL)")
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS source_ids (
                       hyperion_id  TEXT NOT NULL,
                       catalogue    TEXT NOT NULL,
                       catalogue_id TEXT NOT NULL,

                       FOREIGN KEY (hyperion_id) REFERENCES stars (id),
                       UNIQUE (catalogue, catalogue_id)
                   )
                   """)

    log(f"Database verified at {config.DATABASE_PATH}")
    connection.commit()
    connection.close()
    log("Database initialization complete", level="INFO")

def add_star(star: Star):
    """Inserts any number of rows into the stars table using a dictionary"""
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()

    try:
        # Stars Database
        cursor.execute(
            "INSERT INTO stars (id, ra, dec) VALUES (?, ?, ?)",
            (star.id, star.ra, star.dec)
        )
        # Source IDs Database
        for source_id in star.source_ids:
            cursor.execute(
                "INSERT INTO source_ids (hyperion_id, catalogue, catalogue_id) VALUES (?, ?, ?)",
                (star.id, source_id.catalogue, source_id.id)
            )
            print("AFTER INSERT")
            print(cursor.lastrowid)
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
        cursor.execute("DELETE FROM source_ids")
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

