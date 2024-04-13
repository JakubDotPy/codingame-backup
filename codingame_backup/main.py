import logging
from pathlib import Path

import codingame
import typer
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


def version_callback(value: bool):
    if value:
        typer.echo(
            f'{__app_name__}: {typer.style(__version__, fg=typer.colors.YELLOW, bold=True)}'
        )
        raise typer.Exit()


@app.callback()
def common(
        ctx: typer.Context,
        version: bool = typer.Option(None, "--version", callback=version_callback),
):
    """[blue]Codingame backup[/blue]"""
    _ = version  # consume unused arguments
    # create and log in the user
    log.debug('creating the codingame client')
    client = codingame.Client()
    client.login(remember_me_cookie=config['REMEMBER_ME_COOKIE'])
    ctx.obj = client


@app.command()
def download_solutions(
        ctx: typer.Context
) -> None:
    """Download excercise solutions from Codingame."""
    # prepare output folder
    Path('output').mkdir(exist_ok=True)


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
