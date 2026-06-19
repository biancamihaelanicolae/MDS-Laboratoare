import json
import os
from pathlib import Path

HERE = Path(__file__).parent

def build():
    with open(HERE / "data.json") as f:
        items = json.load(f)

    lines = []
    lines.append("<html><body>")
    lines.append("<h1>My list</h1>")
    lines.append("<ul>")
    for item in items:
        lines.append(f"  <li><strong>{item['title']}</strong>: {item['description']}</li>")
    lines.append("</ul>")
    lines.append("</body></html>")

    os.makedirs(HERE / "site", exist_ok=True)
    with open(HERE / "site/index.html", "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    build()
