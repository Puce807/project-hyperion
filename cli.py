import click
from src.logger import log
import src.logger as logger


def ask(msg, valid_options=None):
    print(msg)
    valid = False
    answer = ""
    while not valid:
        answer = input("> ")
        if answer.lower() in valid_options:
            valid = True
        else:
            print("Invalid answer, try again")
    return answer

@click.group()
def cli():
    """Hyperion CLI"""
    pass

@click.command()
@click.argument("gaia_id", type=int)
@click.option("-v", "--verbose", is_flag=True, help="Print debug logs to the terminal.")
def inspect(gaia_id, verbose):
    """Pull star data from local database or Gaia including calculated fields"""
    from src.scraper import fetch_individual_star
    from src.database import fetch_star, add_star
    from src.pipeline import process_star

    logger.VERBOSE = verbose

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

cli.add_command(inspect)

if __name__ == "__main__":
    cli()

# TODO: Fetch bulk - downloads a bulk cluster of stars - --limit, --min-parallax
# TODO: Sync star - saves / updates star to DB
# TODO: List stars - prints clean table of current stars - --sort --limit
# TODO: HR Diagram - opens matplotlib HR diagram - --save (save image as png)
# TODO: Stats - prints fun stats
# TODO: Purge - deletes DB