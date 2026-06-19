import json
from pathlib import Path
from build import build, HERE

def test_titles_appear_in_output():
    build()
    with open(HERE / "site/index.html") as f:
        html = f.read()
    with open(HERE / "data.json") as f:
        items = json.load(f)
    for item in items:
        assert item["title"] in html
