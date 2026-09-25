import csv
from pathlib import Path

from flask import Flask, render_template

ROOT = Path(__file__).resolve().parent.parent
ARTWORKS_CSV = ROOT / "data" / "artworks.csv"

app = Flask(__name__)


def count_artworks():
    with ARTWORKS_CSV.open(encoding="utf-8", newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


@app.route("/")
def index():
    return render_template("index.html", artwork_count=count_artworks())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
