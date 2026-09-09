"""Verify generated private asset URLs against the published authorization prefix."""

from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import sys


class AssetReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.runtime_config = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "script" and attrs.get("id") == "__config":
            self.runtime_config = True
        if tag in {"img", "script", "source", "video", "audio", "iframe", "embed"}:
            if attrs.get("src"):
                self.urls.append(attrs["src"])
        if tag == "object" and attrs.get("data"):
            self.urls.append(attrs["data"])
        if tag == "link" and attrs.get("href"):
            if set(attrs.get("rel", "").split()) & {"stylesheet", "icon", "preload", "modulepreload"}:
                self.urls.append(attrs["href"])
        if tag == "a" and urlsplit(attrs.get("href", "")).path.endswith(".svg"):
            self.urls.append(attrs["href"])
        for candidate in attrs.get("srcset", "").split(","):
            if candidate.strip():
                self.urls.append(candidate.strip().split()[0])
        if attrs.get("poster"):
            self.urls.append(attrs["poster"])

    def handle_data(self, data):
        if self.runtime_config:
            runtime = json.loads(data)
            if runtime.get("search"):
                self.urls.append(runtime["search"])
                base = runtime.get("base", ".").rstrip("/") + "/"
                self.urls.append(base + "search.json")

    def handle_endtag(self, tag):
        if tag == "script":
            self.runtime_config = False


def verify(site):
    site = Path(site).resolve()
    private = site / "death-star"
    if not (private / "index.html").is_file():
        raise ValueError("Missing generated /death-star/index.html")
    count = 0
    blueprints = set()
    for page in private.rglob("*.html"):
        parser = AssetReferences()
        parser.feed(page.read_text())
        page_url = "https://documentation.invalid/" + page.relative_to(site).as_posix()
        for reference in parser.urls:
            # External theme resources are not locally published DS-1 assets.
            if urlsplit(reference).scheme or reference.startswith("//"):
                continue
            resolved = urlsplit(urljoin(page_url, unquote(reference))).path
            if not resolved.startswith("/death-star/"):
                raise ValueError(f"Asset escapes authorization boundary: {page.name}: {reference}")
            target = (site / resolved.lstrip("/")).resolve()
            if not target.is_relative_to(private) or not target.is_file():
                raise ValueError(f"Missing or escaped asset: {page.name}: {reference}")
            count += 1
            if target.suffix == ".svg" and "blueprints" in target.parts:
                blueprints.add(target)
    for plate in (private / "assets/blueprints").glob("*.svg"):
        if plate not in blueprints:
            raise ValueError(f"Blueprint is not referenced by generated HTML: {plate.name}")
    print(f"Verified {count} local asset references and {len(blueprints)} linked blueprints under /death-star/")


if __name__ == "__main__":
    verify(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "site")
