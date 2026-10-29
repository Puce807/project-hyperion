import config
import pytest
import sqlite3
from pathlib import Path
from src.database import initialize_database

def table_exists(cursor, table_name):
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?
    """, (table_name,))
    return cursor.fetchone() is not None

@pytest.mark.timeout(60)
def test_initialise_database():
    """Tests if tables were created"""
    initialize_database()
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()

    for table in config.TABLES:
        exists = table_exists(cursor, table)
        assert exists == True

    connection.close()


def test_ingestion():
    config.DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "test.db"

    test_initialise_database()


