# Documentation build

Install Zensical 0.0.60 and build both documentation areas:

```sh
pip install zensical==0.0.60
python3 scripts/build.py
```

Deploy the complete `site/` directory to Azure Static Web Apps. The GitHub
workflow uses the same build command. Do not use plain `zensical build` for
deployment: it does not stage the separate public and private sites or include
the Azure configuration.

To preview the combined output locally after building:

```sh
python3 -m http.server 8000 --directory site
```

Open `http://localhost:8000/death-star/` for the private documentation, with its
own theme and Markdown configuration. A root-level `zensical serve` uses the
public site's configuration instead. Local preview does not enforce Azure login.

- `/` contains the public Engineering Practices documentation.
- `/death-star/` contains the DS-1 documentation, including its own navigation,
  search index, styles and drawings. It is absent from the public navigation,
  search and sitemap.
- `site/staticwebapp.config.json` requires authentication for `/death-star`
  and `/death-star/*`. Anonymous requests redirect to Microsoft Entra login.

The script builds in temporary directories and replaces the generated `site/`
only after both builds succeed. Existing generated files in `site/` are replaced.

The `authenticated` role allows any signed-in user, not just selected people or
members of a particular organization. Azure enforces these rules when deployed;
a local static file server does not enforce authentication. After deployment,
check pages, `/death-star/search.json` and drawings in a signed-out browser.

## Technical visuals

The private library includes 16 SVG blueprint drawings, a drawing register at
`docs/death-star/reference/visual-language.md`, and Mermaid architecture, process,
trust-boundary and failure-path diagrams. Its blueprint stylesheet lives under
`docs/death-star/assets/stylesheets/`. Figure links open the full SVG, and narrow
screens can scroll large technical drawings without shrinking labels away.

The build validates generated HTML asset references, including nested pages and
the private 404 page, before replacing `site/`. Run the check independently with:

```sh
python3 scripts/verify_assets.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```
