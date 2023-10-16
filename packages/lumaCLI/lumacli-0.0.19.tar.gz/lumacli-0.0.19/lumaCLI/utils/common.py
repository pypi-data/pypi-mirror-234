import typer
import os
from pathlib import Path
from rich.panel import Panel
from rich import print
from importlib.metadata import version

CLI_NAME = "luma"
# Get version
__version__ = version("lumaCLI")


# Utility functions
def get_current_working_directory(metadata_dir, ctx: typer.Context) -> Path:
    # Returns current working directory if metadata_dir is not specified
    if ctx.resilient_parsing:
        return
    if metadata_dir is not None:
        return metadata_dir
    cwd = Path(os.getcwd())
    print(
        Panel(
            f"[yellow]'metadata_dir' not specified, using current working directory {cwd}[/yellow]"
        )
    )
    return cwd


# Callback functions
def require_if_not_dry_run(value, param: typer.CallbackParam, ctx: typer.Context):
    if ctx.resilient_parsing:
        return
    dry_run = ctx.params.get("dry_run", False)

    if value or dry_run:
        return value

    # Raise a typer.BadParameter exception to simulate the same error as missing 'endpoint'
    raise typer.BadParameter(f"Missing argument '{param.name.upper()}'")


# Create command line optionss
MetadataDir: Path = typer.Option(
    None,
    "--metadata-dir",
    "-m",
    help="Specify the directory with dbt metadata files. Defaults to current working directory if not provided.",
    callback=get_current_working_directory,
    exists=True,
    dir_okay=True,
    resolve_path=True,
)
ConfigDir: Path = typer.Option(
    "./.luma",
    "--config-dir",
    "-c",
    help="Specify the directory with the config files. Defaults to ./.luma",
    envvar="LUMA_CONFIG_DIR",
    dir_okay=True,
    resolve_path=True,
)
Force: bool = typer.Option(
    False,
    "--force",
    "-f",
    help="Force the operation",
)

DryRun: bool = typer.Option(
    False,
    "--dry-run",
    "-D",
    help="Perform a dry run. Print the payload but do not send it.",
)
NoConfig: bool = typer.Option(
    False,
    "--no-config",
    "-n",
    help="Set this flag to prevent sending configuration data along with the request.",
)
LumaURL: str = typer.Option(
    None,
    "--luma-url",
    "-l",
    help="URL of the luma instance",
    envvar="LUMA_URL",
    callback=require_if_not_dry_run,
)
PostgresUsername: str = typer.Option(
    ...,
    "--username",
    "-u",
    envvar="LUMA_POSTGRES_USERNAME",
    help="The username for the PostgreSQL database.",
    prompt="PostgreSQL username",
)
PostgresDatabase: str = typer.Option(
    ...,
    "--database",
    "-d",
    envvar="LUMA_POSTGRES_DATABASE",
    help="The name of the PostgreSQL database.",
    prompt="PostgreSQL database",
)
PostgresHost: str = typer.Option(
    "localhost",
    "--host",
    "-h",
    envvar="LUMA_POSTGRES_HOST",
    help="The host address of the PostgreSQL database.",
)
PostgresPort: str = typer.Option(
    "5432",
    "--port",
    "-p",
    envvar="LUMA_POSTGRES_PORT",
    help="The port number for the PostgreSQL database.",
)
PostgresPassword: str = typer.Option(
    ...,
    "--password",
    "-P",
    envvar="LUMA_POSTGRES_PASSWORD",
    help="The password for the PostgreSQL database.",
    prompt="PostgreSQL password",
    hide_input=True,
)
