from typing import Sequence

import typer
from rich.console import Console

from alvin_cli.utils.common_arguments import (
    BRIGHT_BLUE_COLOR_TYPER,
    BRIGHT_CYAN_COLOR_TYPER,
    BRIGHT_GREEN_COLOR_TYPER,
    BRIGHT_MAGENTA_COLOR_TYPER,
    BRIGHT_RED_COLOR_TYPER,
)

console = Console()


def handle_print_exception(detail: Sequence, status_code: str) -> None:
    """Print status code and error message for the raised exception"""

    console.print(
        f"[bold yellow]The status code returned is \U0001f928 :[/bold yellow] "
        f"[bold red]{status_code.replace('(', '').replace(')', '')}[/bold red]",
    )
    console.print(
        f"[bold blue]The connection has failed with the following details \U0001f631 :[/bold blue] {detail[0]}",
        style="bold red",
    )


def typer_secho_raise(text: str, color: str) -> None:
    c = None
    if color == "CYAN":
        c = BRIGHT_CYAN_COLOR_TYPER

    elif color == "MAGENTA":
        c = BRIGHT_MAGENTA_COLOR_TYPER

    elif color == "RED":
        c = BRIGHT_RED_COLOR_TYPER

    elif color == "BLUE":
        c = BRIGHT_BLUE_COLOR_TYPER

    elif color == "GREEN":
        c = BRIGHT_GREEN_COLOR_TYPER

    if c:
        typer.secho(
            text,
            fg=c,
        )
