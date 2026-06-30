import click
from src.scraper import fetch_individual_star

@click.group()
def cli():
    pass

@click.command()
@click.argument("gaia_id", type=int)
def inspect(gaia_id):
    """Pull star data from local database or Gaia"""
    # TODO: Check local database before pulling from Gaia
    data = fetch_individual_star(int(gaia_id))
    data.pprint_all()

    star_dict = dict(zip(data.colnames, data[0]))

    for column_name, value in star_dict.items():
        print(f"{column_name:<30}: {value}")

cli.add_command(inspect)

if __name__ == "__main__":
    cli()