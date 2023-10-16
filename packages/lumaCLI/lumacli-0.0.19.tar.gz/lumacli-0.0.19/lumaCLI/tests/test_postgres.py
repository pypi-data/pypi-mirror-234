from lumaCLI import app
from typer.testing import CliRunner

runner = CliRunner()


def test_ingest(test_server, setup_db):
    result = runner.invoke(
        app,
        [
            "postgres",
            "ingest",
            "--luma-url",
            test_server,
            "--database",
            setup_db.info.dbname,
            "--host",
            setup_db.info.host,
            "--port",
            setup_db.info.port,
            "--username",
            setup_db.info.user,
            "--password",
            setup_db.info.password,
            "--no-config",
        ],
    )
    assert result.exit_code == 0
    assert "The request was successful!" in result.output
