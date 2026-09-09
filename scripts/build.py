"""Build public and authenticated documentation into one Azure deployment."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from verify_assets import verify


ROOT = Path(__file__).resolve().parents[1]


def build():
    zensical = shutil.which("zensical")
    if not zensical:
        raise SystemExit("Install Zensical first: pip install zensical==0.0.60")

    config = ROOT / "staticwebapp.config.json"
    rules = json.loads(config.read_text())["routes"]
    for route in ("/death-star", "/death-star/*"):
        if not any(
            rule.get("route") == route
            and rule.get("allowedRoles") == ["authenticated"]
            for rule in rules
        ):
            raise SystemExit(f"Missing authenticated access rule for {route}")

    output = ROOT / "site"
    if output.is_symlink():
        raise SystemExit("Refusing to replace a symlink at site/")

    # Staging prevents private pages from entering public HTML, search or sitemaps.
    with tempfile.TemporaryDirectory(prefix=".docs-build-", dir=ROOT) as temp:
        staging = Path(temp)
        public = staging / "public"
        private = staging / "private"
        shutil.copytree(
            ROOT / "docs", public / "docs",
            ignore=lambda path, names: (
                [name for name in names if name in {"death-star", "stylesheets"}]
                if Path(path) == ROOT / "docs" else []
            ),
        )
        shutil.copytree(ROOT / "docs/death-star", private / "docs")
        shutil.copy2(ROOT / "zensical.toml", public / "zensical.toml")
        shutil.copy2(ROOT / "zensical.death-star.toml", private / "zensical.toml")

        for project in (public, private):
            subprocess.run(
                [zensical, "build", "--clean", "--config-file", "zensical.toml"],
                cwd=project, check=True,
            )
            if not (project / "site/index.html").is_file():
                raise SystemExit(f"Missing built index for {project.name}")

        public_site = public / "site"
        if (public_site / "death-star").exists():
            raise SystemExit("Private content unexpectedly present in public build")
        for artifact in public_site.rglob("*"):
            if artifact.suffix in {".html", ".json", ".xml"}:
                if "death-star" in artifact.read_text():
                    raise SystemExit(f"Private reference in public output: {artifact.name}")

        shutil.move(str(private / "site"), str(public_site / "death-star"))
        # Zensical 0.0.60 emits root-relative resources in its 404 template,
        # even with a path-only site_url. Mount that template with the subsite.
        not_found = public_site / "death-star/404.html"
        if not_found.exists():
            not_found.write_text(re.sub(
                r'((?:href|src)="/)(?!/|death-star(?:/|"))',
                r'\1death-star/', not_found.read_text(),
            ))
            def mount_runtime(match):
                runtime = json.loads(match[2])
                runtime["base"] = "/death-star/"
                if runtime.get("search", "").startswith("/assets/"):
                    runtime["search"] = "/death-star" + runtime["search"]
                return match[1] + json.dumps(runtime) + match[3]

            not_found.write_text(re.sub(
                r'(<script id="__config"[^>]*>)(.*?)(</script>)',
                mount_runtime, not_found.read_text(),
            ))
        shutil.copy2(config, public_site / config.name)
        verify(public_site)

        # Replace generated output only after both builds have succeeded.
        if output.exists():
            shutil.move(str(output), str(staging / "previous-site"))
        shutil.move(str(public_site), str(output))

    print("Ready to deploy: site/ (private documentation: /death-star/)")


if __name__ == "__main__":
    build()
