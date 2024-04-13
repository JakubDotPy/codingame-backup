from pathlib import Path

import typer
from typing_extensions import Annotated

from codingame_backup import __app_name__
from codingame_backup import __version__


class ExampleSession:
    def __init__(self, url: str):
        print(f"opening session to '{url}'")
        self.url = url

    def send(self, data: str) -> None:
        print(f"sending '{data}' to '{self.url}'")

    def close(self) -> None:
        print("closing session")


def session_dependency(ctx: typer.Context) -> ExampleSession:
    """opens a session for decorated subcommands"""
    session = ExampleSession("https://example.com")
    ctx.call_on_close(session.close)
    return session


def parse_session(url: str) -> ExampleSession:
    session = ExampleSession(url)
    return session


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
    _, _ = ctx, version  # consume unused arguments



@app.command()
def download_solutions(
        session: Annotated[ExampleSession, typer.Option(
            parser=parse_session,
            callback=session_dependency,
            hidden=True,
        )] = None
) -> None:
    """Download excercise solutions from Codingame."""
    # prepare output folder
    Path('output').mkdir(exist_ok=True)
    session.send('ahoj')



@app.command()
def list_solutions() -> None:
    """List all downloaded solutions."""


@app.command()
def show_statistics() -> None:
    """Show how many excercises are completed."""


if __name__ == "__main__":
    raise SystemExit(app())
