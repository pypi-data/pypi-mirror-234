# `luma`

**Usage**:

```console
$ luma [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`: Show the version and exit.
* `--help`: Show this message and exit.

**Commands**:

* `config`
* `dbt`
* `postgres`

## `luma config`

**Usage**:

```console
$ luma config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `init`: Initialize the configuration.
* `send`: Send the current configuration information...
* `show`: Display the current configuration...

### `luma config init`

Initialize the configuration.

**Usage**:

```console
$ luma config init [OPTIONS]
```

**Options**:

* `-c, --config-dir PATH`: Specify the directory with the config files. Defaults to ./.luma  [env var: LUMA_CONFIG_DIR; default: ./.luma]
* `-f, --force`: Force the operation
* `--help`: Show this message and exit.

### `luma config send`

Send the current configuration information to luma

**Usage**:

```console
$ luma config send [OPTIONS]
```

**Options**:

* `-c, --config-dir PATH`: Specify the directory with the config files. Defaults to ./.luma  [env var: LUMA_CONFIG_DIR; default: ./.luma]
* `-l, --luma-url TEXT`: URL of the luma instance  [env var: LUMA_URL]
* `--help`: Show this message and exit.

### `luma config show`

Display the current configuration information.

**Usage**:

```console
$ luma config show [OPTIONS]
```

**Options**:

* `-c, --config-dir PATH`: Specify the directory with the config files. Defaults to ./.luma  [env var: LUMA_CONFIG_DIR; default: ./.luma]
* `--help`: Show this message and exit.

## `luma dbt`

**Usage**:

```console
$ luma dbt [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ingest`: Ingests a bundle of JSON files...
* `send-test-results`: Sends the 'run_results.json' file located...

### `luma dbt ingest`

Ingests a bundle of JSON files (manifest.json, catalog.json, sources.json, run_results.json) located in the specified directory to a Luma endpoint.
If any of these files is not present in the directory, the command will fail. Uses the current working directory if 'metadata_dir' is not specified.

**Usage**:

```console
$ luma dbt ingest [OPTIONS]
```

**Options**:

* `-m, --metadata-dir PATH`: Specify the directory with dbt metadata files. Defaults to current working directory if not provided.
* `-l, --luma-url TEXT`: URL of the luma instance  [env var: LUMA_URL]
* `-D, --dry-run`: Perform a dry run. Print the payload but do not send it.
* `-c, --config-dir PATH`: Specify the directory with the config files. Defaults to ./.luma  [env var: LUMA_CONFIG_DIR; default: ./.luma]
* `-n, --no-config`: Set this flag to prevent sending configuration data along with the request.
* `--help`: Show this message and exit.

### `luma dbt send-test-results`

Sends the 'run_results.json' file located in the specified directory to a Luma endpoint.
The command will fail if the 'run_results.json' file is not present in the directory. The current working directory is used if 'metadata_dir' is not specified.

**Usage**:

```console
$ luma dbt send-test-results [OPTIONS]
```

**Options**:

* `-m, --metadata-dir PATH`: Specify the directory with dbt metadata files. Defaults to current working directory if not provided.
* `-l, --luma-url TEXT`: URL of the luma instance  [env var: LUMA_URL]
* `-D, --dry-run`: Perform a dry run. Print the payload but do not send it.
* `-c, --config-dir PATH`: Specify the directory with the config files. Defaults to ./.luma  [env var: LUMA_CONFIG_DIR; default: ./.luma]
* `-n, --no-config`: Set this flag to prevent sending configuration data along with the request.
* `--help`: Show this message and exit.

## `luma postgres`

**Usage**:

```console
$ luma postgres [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ingest`: Sends metadata from a PostgreSQL database...

### `luma postgres ingest`

Sends metadata from a PostgreSQL database to a Luma ingestion endpoint.
If 'endpoint' is not specified, it will auto-generate from the '.luma/config.yaml' file.

**Usage**:

```console
$ luma postgres ingest [OPTIONS]
```

**Options**:

* `-l, --luma-url TEXT`: URL of the luma instance  [env var: LUMA_URL]
* `-u, --username TEXT`: The username for the PostgreSQL database.  [env var: LUMA_POSTGRES_USERNAME; required]
* `-d, --database TEXT`: The name of the PostgreSQL database.  [env var: LUMA_POSTGRES_DATABASE; required]
* `-h, --host TEXT`: The host address of the PostgreSQL database.  [env var: LUMA_POSTGRES_HOST; default: localhost]
* `-p, --port TEXT`: The port number for the PostgreSQL database.  [env var: LUMA_POSTGRES_PORT; default: 5432]
* `-P, --password TEXT`: The password for the PostgreSQL database.  [env var: LUMA_POSTGRES_PASSWORD; required]
* `-D, --dry-run`: Perform a dry run. Print the payload but do not send it.
* `-c, --config-dir PATH`: Specify the directory with the config files. Defaults to ./.luma  [env var: LUMA_CONFIG_DIR; default: ./.luma]
* `-n, --no-config`: Set this flag to prevent sending configuration data along with the request.
* `--help`: Show this message and exit.
