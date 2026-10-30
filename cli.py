import click
import random
from src.logger import log
import src.logger as logger
import config
from src.plotting import plot_hr_diagram
from src.database import fetch_number, delete_db, fetch_rows_batch
from tabulate import tabulate

# TODO: Fix verboseness

def ask(msg, valid_options=None):
    print(msg)
    valid = False
    answer = ""
    while not valid:
        answer = input("> ")
        if not valid_options or answer.lower() in valid_options:
            valid = True
        else:
            print("Invalid answer, try again")
    return answer

def parse_csv(ctx, param, value):
    if value:
        return [item.strip() for item in value.split(',')]
    return []

@click.group()
def cli():
    """Hyperion CLI"""
    pass

@cli.command()
@click.argument("source_id")
@click.option("-s", "--source", type=click.Choice([*config.SOURCES, "hyperion"]), default="hyperion", help="ID belonging to which catalogue")
@click.option("-r", "--raw", is_flag=True, help="Display original field names without formatting.")
@click.option("-v", "--verbose", is_flag=True, help="Print debug logs to the terminal.")
def inspect(source_id, source, raw, verbose):
    """Pull star data from local database"""
    # TODO: Make output json
    # TODO: Make option for querying remote database
    # TODO: Check for edge cases
    from src.database import fetch_star, initialize_database

    logger.VERBOSE = verbose

    initialize_database()
    source_ids_data = fetch_star(source_id=source_id, table="source_ids", source=source)

    if not source_ids_data:
        log(f"Could not locate star {source_id} in local database for catalogue `{source}`, table `source_ids'",
            level="cli")
        return

    hyperion_id = source_id if source == "hyperion" else dict(source_ids_data[0])["hyperion_id"]

    position_data = fetch_star(source_id=hyperion_id, table="stars", source="hyperion")
    position_data = position_data[0] if position_data else None

    catalogue_data = {}
    for star in source_ids_data:
        catalogue = dict(star)["catalogue"]
        cata_table = catalogue + "_data"
        cata_data = fetch_star(source_id=hyperion_id, table=cata_table, source="hyperion")
        if cata_data:
            catalogue_data[catalogue] = dict(cata_data[0])
        else:
            catalogue_data[catalogue] = None

    # === Message ===

    # --- Header ---
    msg = f" Star Record: {source_id}"
    border = "=" * len(msg)
    print(border)
    print(msg)
    print(border)
    print("")

    # --- Identifiers ---
    print("Identifiers")
    print(f" {'Hyperion ID':<30}: {hyperion_id}")
    for star in source_ids_data:
        star = dict(star)
        catalogue_name = star["catalogue"]
        catalogue_id = star["catalogue_id"]
        label = catalogue_name.capitalize() + " ID"
        print(f" {label:<30}: {catalogue_id}")
    print("")

    # --- Catalogue Data ---
    for catalogue_name, data in catalogue_data.items():
        print(catalogue_name.capitalize())
        if not data:
            print(" No data found")
            continue
        for field, value in data.items():
            if "id" in field:
                continue
            if raw:
                formatted_field = field
            else:
                formatted_field = (field.replace("_", " ")).capitalize()
            print(f" {formatted_field:<30}: {value}")
        print("")
    print("")

    # --- Position ---
    print("Position")
    if position_data is None:
        print(" No data found")
    else:
        ra = round(position_data["ra"], 6)
        dec = round(position_data["dec"], 6)
        print(f" {'RA':<30}: {ra}°")
        print(f" {'DEC':<30}: {dec}°")


@cli.command()
@click.argument("source", type=click.Choice(config.SOURCES))
@click.option("-l", "--limit", type=int, default=1000, help="Number of stars to fetch")
@click.option("-v", "--verbose", is_flag=True, help="Print debug logs to the terminal.")
def fetch(source, limit, verbose):
    """Pull stars from external database for download to local DB"""
    # TODO: Add filters (eg, strict, custom etc)
    from src.pipeline import run_ingestion
    from src.database import initialize_database
    initialize_database()
    logger.VERBOSE = verbose
    run_ingestion(source, limit)

@cli.command()
@click.option("-l", "--limit", type=int, default=10000, help="Number of stars to show on plot")
@click.option("-s", "--style", type=str, default="colour", help="Style of plot: colour, density")
@click.option("-a", "--annotations", is_flag=True, help="*EXPERIMENTAL* Include lines and text to show each part")
@click.option("--save", type=str, is_flag=False, flag_value="default", default=None, help="Save plot to file, pass without value to generate filename")
def hr_diagram(limit, style, annotations, save):
    """Shows a HR diagram using stars from local DB"""
    # TODO: Fix title formatting + filtering
    # TODO: Change to plot command with hr, light curve etc
    print(save)
    if save is None:
        plot_hr_diagram(limit=limit, style=style, annotations=annotations)
    elif save == "default":
        filename = f"HR_{limit}_{style.upper()[0]}_{random.randint(1,1000)}"
        plot_hr_diagram(limit, style, filename, annotations=annotations)
    else:
        plot_hr_diagram(limit, style, save, annotations=annotations)

@cli.command()
@click.option("-y", "--assume-yes", is_flag=True, help="Skip deletion confirm prompt")
@click.option("-t", "--table",
              type=click.Choice(config.SAFE_TABLES + ["all"]),
              default="all", help="Select table")
def purge(assume_yes, table):
    """Deletes all data in local database and drops tables"""
    # TODO: Purge by filter
    if not assume_yes:
        total = fetch_number(table)
        if total == 0:
            answer = ask("Database is already empty, continue deletion anyway? [y/n]",valid_options=["y", "n"])
            if answer == "n":
                return
            else:
                pass
        else:
            answer = ask(f"To delete database, please type `{total}`")
            if answer.strip() != str(total):
                print("Input did not match expected text, try again")
                return
    delete_db(table)

@cli.command()
@click.option("-l", "--limit", type=int, default=10, help="Number of stars to show in table")
@click.option("-f", "--fields", type=str, callback=parse_csv, help="Define custom fields to include")
@click.option("-t", "--table",
              type=click.Choice(config.TABLES),
              default="stars", help="Select table")
def list_data(limit, fields, table):
    """Prints a table of stars saved locally to DB"""
    from datasources import ZTFDataSource, GaiaDataSource
    # TODO: Add sorting and filtering
    # TODO: Add docs
    default_fields = {
        "stars": ["hyperion_id", "ra", "dec"],
        "source_ids": ["hyperion_id", "catalogue", "catalogue_id"],
        "gaia_data": GaiaDataSource.database_fields,
        "ztf_data": ZTFDataSource.database_fields}
    if fields:
        selected_fields = fields
    else:
        selected_fields = default_fields[table]
    print(table)
    results = fetch_rows_batch(limit=limit, fields=selected_fields, table=table)
    if len(results) == 0:
        print("No stars found in database")
        return
    print(tabulate(results, headers=selected_fields))



if __name__ == "__main__":
    cli()

# TODO: Sync star - saves / updates star to DB
# TODO: List stars - prints clean table of current stars - --sort --limit
# TODO: Stats - prints fun stats
# TODO: Remove - remove specific object
# TODO: detect - run full pipeline on an object and ask to save to db - --save

# TODO: Improve helps