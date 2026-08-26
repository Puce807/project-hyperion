# Add New Data Source

This guide details how to add a new data source to the pipeline.

> *NOTE:* This is an internal development guide for the creator, assumes familiarity with Hyperion architecture.
> Instructions make more sense when looking at existing code in context

1. Create a new file in `datasources` with the name of your new data source, eg `tess.py`
2. Copy the content of another datasource class such as `ztf.py` into your new file
3. Edit variables
   - `name`, name of data source, string
   - `table`, name of table storing datasource data, string (e.g. `tess_data`)
   - `query_fields`, what fields are returned from fetch, dict format (key = field name, val = type) 
   - `quality_filters`, filters to apply on fetch, SQL format
   - `schema`, schema of table storing datasource data, string
   - `database_fields`, fields to insert into datasource table, list
4. Modify `fetch` function to return data from new datasource
5. In `models.py` define a new dataclass and add it to the `Star` dataclass
6. In your new file, modify `normalise` to adapt a row returned from `fetch` into your new model
7. In `datasources/__init__.py` add the new datasource to the `DATA_SOURCES` dict, using the datasource name as the key and the new datasource class as the value.