# Architecture diagram

Every rendering of the App Framework architecture diagram comes from one source.

| File | Purpose |
|------|---------|
| [`docs/src/architecture.html`](../../docs/src/architecture.html) | **The source.** A self-contained interactive blueprint — clickable boxes with detail drawers, a numbered "walk the flow" tour, hover connection tracing, light/dark toggle. No dependencies; opens from `file://`. |
| `docs/src/img/architecture-overview.svg` | Static vector, dark. Used in the docs pages. |
| `docs/src/img/architecture-overview.png` | Static raster at 2×, dark. For READMEs and anywhere SVG isn't practical. |
| `docs/src/img/architecture-overview-light.svg` | Static vector, light. |
| `docs/src/img/architecture-overview-light.png` | Static raster at 2×, light. |

The docs pick the variant with Material's `#only-dark` / `#only-light` image
suffixes, so the static picture follows the palette toggle:

```markdown
![App Framework Architecture](img/architecture-overview.svg#only-dark)
![App Framework Architecture](img/architecture-overview-light.svg#only-light)
```

## Editing

Edit `docs/src/architecture.html` only. Everything lives in the one `<script>`
block: `panels`, `N` (nodes), `A` (arrows) and `subheads` between the
`/*==DATA-START==*/` markers define the canvas; `D` holds the per-box drawers and
`STEPS` the guided tour.

## Regenerating the SVG and PNG

```bash
python3 tools/architecture-diagram/render.py
```

The script loads the interactive page in headless Chrome once per colour scheme,
reads the *rendered* geometry and the scheme's own CSS variables out of the DOM,
and re-emits them as SVG — so neither the layout nor the colours of the static
images can drift from the interactive one. Override the browser with
`CHROME=/path/to/chrome`.

## Checking a change

```bash
# geometry: zero overlaps, no clipped box text, nothing outside the stage
python3 tools/architecture-diagram/audit.py
```
