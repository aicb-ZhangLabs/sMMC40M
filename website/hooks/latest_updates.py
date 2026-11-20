"""MkDocs hook: fill <!-- LATEST_UPDATES --> on the home page with the newest update posts.

Posts live in website/updates/posts/*.md and need `date:` front matter, a `# Title` and a
`<!-- more -->` excerpt separator (see scripts/new_monthly_update.py).
"""
import datetime as dt
import re
from pathlib import Path

import yaml

MARKER = "<!-- LATEST_UPDATES -->"
SHOW = 3


def _posts(docs_dir):
    posts = []
    for path in sorted((Path(docs_dir) / "updates" / "posts").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            continue
        meta, body = yaml.safe_load(m.group(1)) or {}, m.group(2)
        if meta.get("draft"):
            continue
        date = meta.get("date")
        if isinstance(date, dict):
            date = date.get("created")
        if isinstance(date, str):
            date = dt.date.fromisoformat(date[:10])
        if isinstance(date, dt.datetime):
            date = date.date()
        title = re.search(r"^#\s+(.+)$", body, re.M)
        head = body.split("<!-- more -->")[0]
        excerpt = re.sub(r"^#\s+.+$", "", head, flags=re.M).strip()
        excerpt = re.sub(r"\s+", " ", excerpt)
        posts.append(dict(date=date, title=title.group(1).strip() if title else path.stem,
                          excerpt=excerpt, link=f"updates/posts/{path.name}"))
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def on_page_markdown(markdown, page, config, files):
    if MARKER not in markdown:
        return markdown
    items = []
    for p in _posts(config["docs_dir"])[:SHOW]:
        date = f"{p['date']:%B} {p['date'].day}, {p['date'].year}"
        items.append(f'- <span class="date">{date}</span>\n'
                     f'  [{p["title"]}]({p["link"]}){{ .title }}\n'
                     f'  <span class="excerpt">{p["excerpt"]}</span>')
    block = '<div class="smcc-updates" markdown>\n\n' + "\n".join(items) + "\n\n</div>"
    return markdown.replace(MARKER, block)
