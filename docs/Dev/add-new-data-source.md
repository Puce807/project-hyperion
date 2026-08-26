# Add New Data Source

This guide details how to add a new data source to the pipeline.

> *NOTE:* This is an internal development guide for the creator, assumes familiarity with Hyperion architecture

1. In `src/scraper.py`, create function following pattern of `fetch_bulk_ztf` to fetch data. Ideally use TAP query if possible.
2. In `src/scaper.py` in the `fetch_data` function, add case to route requests to new data source.
3. Data model
   1. In `models.py`, create a new data class called the name of your new data source
   2. In `models.py`, add your new data class to `Star` data class
4. Config 
   1. In `config.py` and `config.defaults.py`, add the name of your new data source to the list `SOURCES` 
   2. In `config.py` and `config.defaults.py`, add the name of your new data source table name to the list `TABLES` and `SAFE_TABLES` 
   3. In `config.py` and `config.defaults.py`, create a variable for fields to download 
5. Database
   1. In `database.py`, in `initialize_database`, add statement to create table to store data from your new source with correct schema.
      - Must include `hyperion_id` as primary key referencing stars DB
      - Must include data source identifier 
   2. In `database.py` in `add_star`, add a statement to insert data into newly created table
6. CLI
   1. In `cli.py`, in `list_data`, add fields to `default_fields` dictionary