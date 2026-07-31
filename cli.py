import click
import random

from PIL.JpegPresets import presets

from src.logger import log
import src.logger as logger
from config import FIELD_PRESETS
from src.plotting import plot_hr_diagram
from src.database import fetch_number, delete_db, fetch_stars_batch
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
@click.argument("gaia_id", type=int)
@click.option("-v", "--verbose", is_flag=True, help="Print debug logs to the terminal.")
def inspect(gaia_id, verbose):
    """Pull star data from local database or Gaia including calculated fields"""
    from src.scraper import fetch_individual_star
    from src.database import fetch_star, add_star, initialize_database
    from src.pipeline import process_star

    logger.VERBOSE = verbose

    initialize_database()
    data = fetch_star(int(gaia_id))
    if data is not None: # Star exists in local database
        final_record = dict(data)
        exists = True
        log(f"Displaying local database record for star {gaia_id}", level="cli")
    else:
        exists = False
        log(f"Star {gaia_id} not found locally. Querying Gaia servers...", level="cli")
        data = fetch_individual_star(int(gaia_id))
        if data is not None:
            final_record = process_star(data)
        else:
            log(f"Could not locate star {gaia_id} in local storage or online registries.", level="cli")
            return

    for column_name, value in final_record.items():
        print(f"{column_name:<30}: {value}")

    if not exists:
        answer = ask("Do you want to save this star to the local database? [y/n]", ["y","n"])
        if answer.lower() == "y":
            add_star(final_record)

@cli.command()
@click.option("-l", "--limit", type=int, default=1000, help="Number of stars to fetch")
@click.option("-v", "--verbose", is_flag=True, help="Print debug logs to the terminal.")
def fetch_bulk(limit, verbose):
    """Pull stars from Gaia database for download to local DB"""
    # TODO: Add filters (eg, strict, custom etc)
    from src.pipeline import run_ingestion
    from src.database import initialize_database
    initialize_database()
    logger.VERBOSE = verbose
    run_ingestion(limit)

@cli.command()
@click.option("-l", "--limit", type=int, default=10000, help="Number of stars to show on plot")
@click.option("-s", "--style", type=str, default="colour", help="Style of plot: colour, density")
@click.option("-a", "--annotations", is_flag=True, help="*EXPERIMENTAL* Include lines and text to show each part")
@click.option("--save", type=str, is_flag=False, flag_value="default", default=None, help="Save plot to file, pass without value to generate filename")
def hr_diagram(limit, style, annotations, save):
    """Shows a HR diagram using stars from local DB"""
    # TODO: Fix title formatting + filtering
    print(save)
    if save is None:
        plot_hr_diagram(limit=limit, style=style, annotations=annotations)
    elif save == "default":
        filename = f"HR_{limit}_{style.upper()[0]}_{random.randint(1,1000)}"
        plot_hr_diagram(limit, style, filename, annotations=annotations)
    else:
        plot_hr_diagram(limit, style, save, annotations=annotations)

@cli.command()
def purge():
    """Deletes all data in local database"""
    total = fetch_number()
    if total == 0:
        print("Database is already empty")
        return
    answer = ask(f"To delete database with stars, please type `{total}`")
    if answer.strip() != str(total):
        print("Input did not match expected text, try again")
        return
    delete_db()

@cli.command()
@click.option("-l", "--limit", type=int, default=10, help="Number of stars to show in table")
@click.option("-f", "--fields", type=str, callback=parse_csv, help="Define custom fields to include")
@click.option("-p", "--preset",
              type=click.Choice(["default", "quality", "photometry", "astrometry", "variability", "all"]),
              default="default", help="Select a field group preset")
def list_stars(limit, fields, preset):
    """Prints a table of stars saved locally to DB"""
    # TODO: Add sorting and filtering
    if fields: selected_fields = fields
    else:
        selected_fields = FIELD_PRESETS[preset]
    results = fetch_stars_batch(limit=limit, fields=selected_fields)
    if len(results) == 0:
        print("No stars found in database")
        return
    print(tabulate(results, headers=selected_fields))



if __name__ == "__main__":
    cli()

# TODO: Sync star - saves / updates star to DB
# TODO: List stars - prints clean table of current stars - --sort --limit
# TODO: Stats - prints fun stats
