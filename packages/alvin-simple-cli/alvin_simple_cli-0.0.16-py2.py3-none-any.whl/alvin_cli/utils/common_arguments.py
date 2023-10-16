import typer

BRIGHT_GREEN_COLOR_TYPER = typer.colors.BRIGHT_GREEN
BRIGHT_CYAN_COLOR_TYPER = typer.colors.BRIGHT_CYAN
BRIGHT_YELLOW_COLOR_TYPER = typer.colors.BRIGHT_YELLOW
BRIGHT_RED_COLOR_TYPER = typer.colors.BRIGHT_RED
BRIGHT_MAGENTA_COLOR_TYPER = typer.colors.BRIGHT_MAGENTA
BRIGHT_BLUE_COLOR_TYPER = typer.colors.BRIGHT_BLUE

PLATFORM_ID = typer.Option(
    ...,
    "--platform-id",
    "-pid",
    help=typer.style("Platform ID", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)


DW_PLATFORM_ID = typer.Option(
    ...,
    "--dw-platform-id",
    "-dwpid",
    help=typer.style(
        "Data Warehouse (Target) Platform ID", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True,
    ),
)

DBT_PROJECT_NAME = typer.Option(
    ...,
    "--project-name",
    "-dbtproj",
    help=typer.style("Dbt Project Name", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)

DBT_USER_EMAIL = typer.Option(
    ...,
    "--user-email",
    "-user",
    help=typer.style("Dbt User Email", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)

ARTIFACTS_PATH = typer.Option(
    ...,
    "--artifacts-path",
    "-path",
    help=typer.style(
        "Path to dbt target folder", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True,
    ),
)
