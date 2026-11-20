"""Resolve links in rendered notebooks against MkDocs page URLs."""

from posixpath import dirname, join, normpath
from urllib.parse import unquote, urlsplit, urlunsplit

from bs4 import BeautifulSoup
from mkdocs.utils import get_relative_url


def on_page_content(html, page, config, files):
    if not page.file.src_uri.endswith(".ipynb"):
        return html

    content = BeautifulSoup(html, "html.parser")
    source_dir = dirname(page.file.src_uri)
    for link in content.find_all("a", href=True):
        url = urlsplit(link["href"])
        if url.scheme or url.netloc or url.path.startswith("/"):
            continue
        if not url.path.endswith((".md", ".ipynb")):
            continue
        source = normpath(join(source_dir, unquote(url.path)))
        destination = files.get_file_from_path(source)
        if destination is not None:
            path = get_relative_url(destination.url, page.url)
            link["href"] = urlunsplit(("", "", path, url.query, url.fragment))
    return str(content)
