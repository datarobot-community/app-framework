# Architecture diagram

Three renderings of the same App Framework architecture diagram, from one source.

| File | Purpose |
|------|---------|
| [`docs/src/architecture.html`](../../docs/src/architecture.html) | **The source.** A self-contained interactive blueprint — clickable boxes with detail drawers, a numbered "walk the flow" tour, hover connection tracing. No dependencies; opens from `file://`. |
| `docs/src/img/architecture-overview.svg` | Static vector, generated from the source. Used in the docs pages. |
| `docs/src/img/architecture-overview.png` | Static raster at 2×, generated from the SVG. For READMEs and anywhere SVG isn't practical. |

## Editing

Edit `docs/src/architecture.html` only. Everything lives in the one `<script>`
block: `panels`, `N` (nodes), `A` (arrows) and `subheads` between the
`/*==DATA-START==*/` markers define the canvas; `D` holds the per-box drawers and
`STEPS` the guided tour.

## Regenerating the SVG and PNG

```bash
python3 tools/architecture-diagram/render.py
```

The script loads the interactive page in headless Chrome, reads the *rendered*
geometry out of the DOM and re-emits it as SVG, so the static images can never
drift from the interactive one. Override the browser with `CHROME=/path/to/chrome`.

## Checking a change

```bash
# geometry: zero overlaps, no clipped box text, nothing outside the stage
python3 tools/architecture-diagram/audit.py
```
