""" CLI Commands for interacting with auth"""

import typer
from rich import print
from rich.table import Table
import sieve.api.models as model

cli = typer.Typer()


@cli.callback()
def callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
        raise typer.Exit()


@cli.command()
def info():
    print("yes")


@cli.command()
def login():
    print("cool")
