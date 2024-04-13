import typer

from codingame_backup import __app_name__
from codingame_backup import __version__

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


@app.command
def foo() -> None:
    pass


if __name__ == "__main__":
    raise SystemExit(app())
