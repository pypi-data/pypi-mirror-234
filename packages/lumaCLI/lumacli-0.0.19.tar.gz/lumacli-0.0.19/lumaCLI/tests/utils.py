import os

TESTS_DIR = os.path.dirname(__file__)
TEMP_DIR = os.path.join(TESTS_DIR, "temp")
METADATA_DIR = os.path.join(TESTS_DIR, "metadata_dir")
MANIFEST_JSON = os.path.join(METADATA_DIR, "manifest.json")
INVALID_JSON = os.path.join(METADATA_DIR, "invalid_json.json")
FILE_TXT = os.path.join(METADATA_DIR, "file.txt")
POSTGRES_DUMP_FILE = os.path.join(METADATA_DIR, "postgres_dump_file.sql")
LUMA_CONFIG_DIR = os.path.join(TESTS_DIR, ".luma")
INVALID_SCHEMA_LUMA_CONFIG_DIR = os.path.join(TESTS_DIR, ".invalid_schema_luma")
