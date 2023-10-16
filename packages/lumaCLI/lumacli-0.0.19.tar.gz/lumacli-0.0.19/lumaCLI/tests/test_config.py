from lumaCLI import app
from typer.testing import CliRunner
from lumaCLI.utils.luma_utils import get_config
from rich.console import Console
import yaml
import click

runner = CliRunner()


def test_get_config(config_dir):
    config = get_config(config_dir=config_dir)
    assert config


def test_show(config_dir):
    result = runner.invoke(
        app,
        [
            "config",
            "show",
            "--config-dir",
            config_dir,
        ],
    )

    assert result.exit_code == 0
    config = get_config(config_dir=config_dir)
    console = Console(record=True)
    console.print(config)
    text = console.export_text()
    assert text in result.output


def test_send(config_dir, test_server):
    result = runner.invoke(
        app,
        ["config", "send", "--config-dir", config_dir, "--luma-url", test_server],
    )

    assert result.exit_code == 0
    assert "The request was successful!" in result.output


# Invalid schema tests
def test_get_config_invalid_schema(config_dir_invalid_schema):
    try:
        config = get_config(config_dir=config_dir_invalid_schema)
        assert config is None
    except click.exceptions.Abort:
        pass


def test_show_invalid_schema(config_dir_invalid_schema):
    result = runner.invoke(
        app,
        [
            "config",
            "show",
            "--config-dir",
            config_dir_invalid_schema,
        ],
    )

    assert result.exit_code == 1
    assert "Error parsing YAML file" in result.output


def test_send_invalid_schema(config_dir_invalid_schema, test_server):
    result = runner.invoke(
        app,
        [
            "config",
            "send",
            "--config-dir",
            config_dir_invalid_schema,
            "--luma-url",
            test_server,
        ],
    )

    assert result.exit_code == 1
    assert "Error parsing YAML file" in result.output
