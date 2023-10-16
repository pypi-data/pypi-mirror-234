import pytest
from lumaCLI.utils import (
    run_command,
    create_conn,
    generate_pg_dump_content,
    get_pg_dump_tables_info,
    get_pg_dump_views_info,
    get_tables_size_info,
    get_tables_row_counts,
    get_db_metadata,
)


def test_run_command():
    command = 'echo "Hello, World!"'
    assert run_command(command, True) == "Hello, World!"


def test_create_conn(setup_db):
    assert isinstance(
        setup_db.info.port, int
    )  # Add this line to ensure port is an integer

    conn = create_conn(
        username=setup_db.info.user,
        password=setup_db.info.password,
        host=setup_db.info.host,
        port=setup_db.info.port,
        database=setup_db.info.dbname,
    )
    assert conn
    assert conn.closed == 0  # 0 indicates connection is open


def test_generate_pg_dump_content(setup_db):
    result = generate_pg_dump_content(
        username=setup_db.info.user,
        password=setup_db.info.password,
        host=setup_db.info.host,
        port=setup_db.info.port,
        database=setup_db.info.dbname,
    )
    assert "users" in result
    assert "products" in result
    assert "product_id" in result
    assert "user_id" in result
    assert "CURRENT_TIMESTAMP" in result


def test_get_pg_dump_tables_info(setup_db):
    dump_content = generate_pg_dump_content(
        username=setup_db.info.user,
        password=setup_db.info.password,
        host=setup_db.info.host,
        port=setup_db.info.port,
        database=setup_db.info.dbname,
    )
    result = get_pg_dump_tables_info(dump_content)
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_pg_dump_views_info(setup_db):
    dump_content = generate_pg_dump_content(
        username=setup_db.info.user,
        password=setup_db.info.password,
        host=setup_db.info.host,
        port=setup_db.info.port,
        database=setup_db.info.dbname,
    )
    result = get_pg_dump_views_info(dump_content)
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_tables_size_info(setup_db):
    result = get_tables_size_info(
        username=setup_db.info.user,
        password=setup_db.info.password,
        host=setup_db.info.host,
        port=setup_db.info.port,
        database=setup_db.info.dbname,
    )
    assert isinstance(result, dict)
    assert len(result) > 0


def test_get_tables_row_counts(setup_db):
    result = get_tables_row_counts(
        username=setup_db.info.user,
        password=setup_db.info.password,
        host=setup_db.info.host,
        port=setup_db.info.port,
        database=setup_db.info.dbname,
    )
    assert isinstance(result, dict)
    assert len(result) > 0


def test_get_db_metadata(setup_db):
    result = get_db_metadata(
        username=setup_db.info.user,
        password=setup_db.info.password,
        host=setup_db.info.host,
        port=setup_db.info.port,
        database=setup_db.info.dbname,
    )
    assert isinstance(result, dict)
    assert len(result) > 0
