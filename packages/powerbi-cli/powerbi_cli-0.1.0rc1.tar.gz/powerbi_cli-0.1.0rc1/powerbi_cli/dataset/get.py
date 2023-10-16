import click
from tabulate import tabulate

from powerbi_cli.client import pbi


@click.command()
@click.option("-w", "--workspace", default=None)
@click.argument("dataset")
def get(dataset: str, workspace: str):
    """Get details about one Dataset in a given workspace"""
    dataset_ = pbi.dataset(dataset=dataset, group=workspace)
    table = [[k, v] for k, v in dataset_.raw.items()]  # type: ignore
    click.echo(tabulate(table, tablefmt="plain"))
