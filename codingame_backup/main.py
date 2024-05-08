import logging
from pathlib import Path
from typing import Annotated
from typing import Optional

import typer
from codingame.client.sync import SyncClient
from rich.console import Console
from rich.table import Table

from codingame_backup import __app_name__
from codingame_backup import __version__
from codingame_backup.config import config
from codingame_backup.config import setup_logging

setup_logging()
log = logging.getLogger(__name__)

app = typer.Typer(
    name=__app_name__,
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode='rich',
)


class CGClient(SyncClient):
    """Custom wrapper around the codingame SyncClient directly."""

    def __init__(self):
        super().__init__()
        # automatic login on init
        # no need to use client without login
        self.login(remember_me_cookie=config['REMEMBER_ME_COOKIE'])

    def get_solved_excercises(self) -> list[dict]:
        """Get and sort all excercises."""
        return self.request('Puzzle', 'findAllMinimalProgress', [self.codingamer.id])


def version_callback(value: bool):
    if value:
        typer.echo(
            f'{__app_name__}: {typer.style(__version__, fg=typer.colors.YELLOW, bold=True)}'
        )
        raise typer.Exit()


@app.callback()
def common(
        version: Annotated[
            Optional[bool],
            typer.Option("--version", callback=version_callback, is_eager=True),
        ] = None,
):
    """[blue]Codingame backup[/blue]"""
    _ = version  # consume unused arguments


@app.command()
def check_login() -> None:
    """Create client and verify login."""
    typer.echo('checking login')
    try:
        client = CGClient()
    except Exception as e:
        typer.secho(e, fg=typer.colors.RED, bold=True)
    else:
        typer.echo(client.codingamer)
        typer.secho('login successfull', fg=typer.colors.GREEN)


@app.command()
def download_solutions() -> None:
    """Download excercise solutions from Codingame."""
    # prepare output folder
    Path('output').mkdir(exist_ok=True)

    client = CGClient()

    # excercises = ctx.obj.get_solved_excercises()
    # only_solved = list(exc for exc in excercises if exc['submitted'])
    # print(only_solved)


@app.command()
def list_solutions() -> None:
    """List all downloaded solutions."""


@app.command()
def show_statistics(
        ctx: typer.Context
) -> None:
    """Show how many excercises are completed."""

    user = ctx.obj.codingamer
    console = Console()
    table = Table("Attribute", "Value")
    attributes = [
        'avatar',
        'avatar_url',
        'biography',
        'category',
        'company',
        'country_id',
        'cover',
        'cover_url',
        'id',
        'level',
        'professional',
        'profile_url',
        'pseudo',
        'public_handle',
        'rank',
        'school',
        'student',
        'tagline',
        'xp',
    ]
    for attr in attributes:
        table.add_row(attr, str(getattr(user, attr)))
    console.print(table)


if __name__ == "__main__":
    raise SystemExit(app())
