#!/usr/bin/env python

# Required imports
import typer
import urllib3

# Local module imports
import lumaCLI.commands.config as config_module
import lumaCLI.commands.dbt as dbt_module
import lumaCLI.commands.postgres as postgres_module

from lumaCLI.utils.common import CLI_NAME, __version__

# Disabling warnings related to insecure requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create a Typer application with set properties
app = typer.Typer(
    name=CLI_NAME,  # Set the name of the CLI
    no_args_is_help=True,  # Show help message if no arguments are provided
    pretty_exceptions_show_locals=False,  # Do not display local variables when an exception occurs
    pretty_exceptions_enable=True,
    pretty_exceptions_short=True
)


# Version callback
def version_callback(show_version: bool):
    if show_version:
        typer.echo(__version__)
        raise typer.Exit()


# Add a --version option
@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    pass


# Add commands to the application
app.add_typer(dbt_module.app, name="dbt")
app.add_typer(postgres_module.app, name="postgres")
app.add_typer(config_module.app, name="config")


if __name__ == "__main__":
    app()
