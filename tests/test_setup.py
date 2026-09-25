import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_env import FOLDERS, SCHEMAS, read_header  # noqa: E402


@pytest.mark.parametrize("path, expected", SCHEMAS.items())
def test_csv_header_matches_schema(path, expected):
    assert read_header(path) == expected


@pytest.mark.parametrize("folder", FOLDERS)
def test_folder_exists(folder):
    assert (ROOT / folder).is_dir()
