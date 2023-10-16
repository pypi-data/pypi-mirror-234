import typer
from lumaCLI.models import Config
from rich import print
from pathlib import Path
from lumaCLI.utils import get_config, send_config, init_config
from lumaCLI.utils.common import LumaURL, ConfigDir, Force

app = typer.Typer(
    name="config", no_args_is_help=True, pretty_exceptions_show_locals=False
)


@app.command(help="Initialize the configuration.")
def init(config_dir: Path = ConfigDir, force: bool = Force):
    try:
        init_config(config_dir=config_dir, force=force)
        print(f"[green]Config initialized at[/green] {config_dir}")
        raise typer.Exit(0)
    except FileExistsError:
        print("[red]Error![/red]")
        print(
            f"[red]Config files already exist at[/red] {config_dir}\n[yellow]If you want to override run with flag [/yellow][red]--force/-f[/red]"
        )
        raise typer.Exit(1)


@app.command(help="Display the current configuration information.")
def show(config_dir: Path = ConfigDir):
    try:
        config: Config = get_config(config_dir=config_dir)
    except FileNotFoundError:
        print("[red]Error![/red]")
        print(
            f"[red]Config files not found at[/red] {config_dir}\n[yellow]To generate config files use [/yellow][white]'luma config init'[/white]"
        )
        raise typer.Exit(1)

    print(config)
    raise typer.Exit(0)


@app.command(help="Send the current configuration information to luma")
def send(config_dir: Path = ConfigDir, luma_url: str = LumaURL):
    # Retrieve the global config object
    try:
        config: Config = get_config(config_dir=config_dir)
    except FileNotFoundError:
        print("[red]Error![/red]")
        print(
            f"[red]Config files not found at[/red] {config_dir}\n[yellow]To generate config files use [/yellow][white]'luma config init'[/white]"
        )
        raise typer.Exit(1)

    # Send the configuration and exit the program
    if config:
        response = send_config(config=config, luma_url=luma_url)
        if not response.ok:
            raise typer.Exit(1)

    else:
        print(
            f"[red]No Config detected under {config_dir}[/red]\n[yellow]To generate config files use [/yellow][white]'luma config init'[/white]"
        )
