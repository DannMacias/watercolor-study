"""Environment check: Python/venv, packages, CSV schema and folder structure."""
import csv
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PACKAGES = {
    "flask": "flask",
    "opencv-python-headless": "cv2",
    "scikit-image": "skimage",
    "numpy": "numpy",
    "pillow": "PIL",
    "pymixbox": "mixbox",
    "requests": "requests",
    "pytest": "pytest",
}

SCHEMAS = {
    "data/artists.csv": [
        "artist_id", "name", "birth_year", "death_year",
        "nationality", "movement", "notes",
    ],
    "data/artworks.csv": [
        "artwork_id", "artist_id", "title", "year", "medium", "dimensions_cm",
        "source_museum", "source_url", "image_url", "license", "file_path",
        "width_px", "height_px",
    ],
}

FOLDERS = [
    "data", "images", "scripts", "tests", "app",
    "app/color", "app/values", "app/templates", "app/static",
]


def read_header(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as f:
        return next(csv.reader(f), [])


def package_version(dist, module):
    from importlib.metadata import version
    importlib.import_module(module)
    return version(dist)


def main():
    ok = True

    print(f"Python {sys.version.split()[0]}")
    venv = Path(sys.prefix).resolve() == (ROOT / ".venv").resolve()
    print(f"Inside .venv: {venv}")
    ok &= venv

    for dist, module in PACKAGES.items():
        try:
            print(f"  {dist}: {package_version(dist, module)}")
        except Exception as e:
            print(f"  {dist}: IMPORT FAILED ({e})")
            ok = False

    for path, expected in SCHEMAS.items():
        actual = read_header(path)
        if actual == expected:
            print(f"Schema OK: {path}")
        else:
            ok = False
            print(f"Schema MISMATCH: {path}")
            print(f"  missing: {[c for c in expected if c not in actual]}")
            print(f"  extra:   {[c for c in actual if c not in expected]}")
            print(f"  expected order: {expected}")
            print(f"  actual order:   {actual}")

    for folder in FOLDERS:
        if not (ROOT / folder).is_dir():
            print(f"Missing folder: {folder}")
            ok = False

    if not ok:
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
