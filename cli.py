import click
from src.scraper import fetch_individual_star
from src.database import fetch_star, add_star
from src.logger import log

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
    pass

@click.command()
@click.argument("gaia_id", type=int)
def inspect(gaia_id):
    # TODO: Add verbose flag
    """Pull star data from local database or Gaia"""
    data = fetch_star(int(gaia_id))
    if data is not None: # Star exists in local database
        star_dict = dict(data)
        exists = True
        log(f"Displaying local database record for star {gaia_id}")
    else:
        exists = False
        log(f"Star {gaia_id} not found locally. Querying Gaia servers...")
        data = fetch_individual_star(int(gaia_id))
        if data is not None:
            star_dict = dict(zip(data.colnames, data))
        else:
            log(f"Could not locate star {gaia_id} in local storage or online registries.", level="error")
            return

    for column_name, value in star_dict.items():
        print(f"{column_name:<30}: {value}")

    #answer = ask("Do you want to save this star to the local database? [y/n]", ["y","n"])
    #if answer.lower() == "y":
        # TODO: Check local DB before query
        #add_star(star_dict)

cli.add_command(inspect)

if __name__ == "__main__":
    cli()

# TODO: Fetch bulk - downloads a bulk cluster of stars - --limit, --min-parallax
# TODO: Sync star - saves / updates star to DB
# TODO: List stars - prints clean table of current stars - --sort --limit
# TODO: HR Diagram - opens matplotlib HR diagram - --save (save image as png)
# TODO: Stats - prints fun stats