"""Render the static architecture SVG from the live blueprint DOM.

Loads architecture.html in headless Chrome, walks the rendered canvas (panels,
nodes, arrow paths, labels, subheads) and emits an equivalent standalone SVG so
the PNG/SVG and the interactive page can never drift apart.
"""

import html
import os
import pathlib
import re
import subprocess
import sys

CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
HERE = pathlib.Path(__file__).parent
DOCS = HERE.parent.parent / "docs" / "src"
SOURCE = DOCS / "architecture.html"
IMG = DOCS / "img"
WIDTH, HEIGHT = 2130, 1100

EXPORT_JS = r"""
<script>
setTimeout(() => {
  setScheme('slate', false);   // the static image is dark regardless of any stored preference
  setScale(1);
  const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const HEIGHT = 1100;            // canvas rows only — the note bands stay out of the static image
  const px = n => Math.round(n * 100) / 100;
  const out = [];

  // gradients + the arrow marker/def block, lifted straight from the live wires svg
  const grads = Object.entries(C).filter(([k]) => k !== 'line').map(([k, hex]) => {
    const n = parseInt(hex.slice(1), 16), r = n>>16&255, g = n>>8&255, b = n&255;
    return `<linearGradient id="g-${k}" x1="0" y1="0" x2="0" y2="1">`
      + `<stop offset="0" stop-color="rgb(${r},${g},${b})" stop-opacity="0.16"/>`
      + `<stop offset="1" stop-color="rgb(${r},${g},${b})" stop-opacity="0.05"/></linearGradient>`;
  }).join('');
  out.push(`<defs>${grads}${document.querySelector('#wires defs').innerHTML}</defs>`);
  out.push(`<rect width="100%" height="100%" fill="#0B0B0B"/>`);

  // panels
  document.querySelectorAll('.panel').forEach(p => {
    const cs = getComputedStyle(p);
    const x = p.offsetLeft, y = p.offsetTop, w = p.offsetWidth, h = p.offsetHeight;
    out.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="15" fill="${cs.backgroundColor}"`
      + ` stroke="${cs.borderTopColor}" stroke-width="1" stroke-dasharray="6 5"/>`);
    const t = p.querySelector('.ptitle'), s = p.querySelector('.psub');
    if (t) {
      const r = t.getBoundingClientRect(), st = getComputedStyle(t);
      const bx = x + t.offsetLeft, by = y + t.offsetTop;
      out.push(`<rect x="${px(bx)}" y="${px(by)}" width="${px(r.width)}" height="${px(r.height)}" rx="9" fill="#0B0B0B"/>`);
      out.push(`<text x="${px(bx + 9)}" y="${px(by + r.height - 5)}" font-size="11.5" font-weight="700"`
        + ` letter-spacing="0.4" fill="${st.color}">${esc(t.textContent.toUpperCase())}</text>`);
    }
    if (s) {
      const r = s.getBoundingClientRect();
      const bx = x + s.offsetLeft, by = y + s.offsetTop;
      out.push(`<rect x="${px(bx)}" y="${px(by)}" width="${px(r.width)}" height="${px(r.height)}" rx="9" fill="#0B0B0B"/>`);
      out.push(`<text x="${px(bx + 8)}" y="${px(by + r.height - 4)}" font-size="10.5" fill="#8f9d94">${esc(s.textContent)}</text>`);
    }
  });

  // subheads
  document.querySelectorAll('.subhead').forEach(s => {
    out.push(`<text x="${s.offsetLeft}" y="${s.offsetTop + 10}" font-size="10.1" font-style="italic"`
      + ` fill="#8f9d94">${esc(s.textContent)}</text>`);
  });

  // arrows — reuse the exact paths the page drew
  document.querySelectorAll('#wires path').forEach(p => out.push(p.outerHTML));

  // nodes
  N.forEach(n => {
    const col = C[n.c], el = document.querySelector(`.node[data-id="${n.id}"]`);
    const stroke = getComputedStyle(el).borderTopColor;
    const cy = n.y + n.h / 2, sm = !!n.sm;
    out.push(`<g><rect x="${n.x}" y="${n.y}" width="${n.w}" height="${n.h}" rx="11" fill="url(#g-${n.c})"`
      + ` stroke="${stroke}" stroke-width="1"/>`
      + `<path d="M${n.x + 2},${n.y} h2 v${n.h} h-2 a2,2 0 0 1 -2,-2 v${-(n.h - 4)} a2,2 0 0 1 2,-2 z" fill="${col}"/>`
      + `<text x="${n.x + 11}" y="${px(cy - 2)}" font-size="${sm ? 12.3 : 13.2}" font-weight="650" fill="#ffffff">${esc(n.t)}</text>`
      + `<text x="${n.x + 11}" y="${px(cy + (sm ? 12 : 13))}" font-size="${sm ? 10.4 : 11}" fill="#98a69d">${esc(n.s)}</text></g>`);
  });

  // arrow labels
  document.querySelectorAll('.wlabel').forEach(l => {
    const r = l.getBoundingClientRect();
    const cx = parseFloat(l.style.left), cy = parseFloat(l.style.top);
    const seam = l.classList.contains('seam');
    const x = px(cx - r.width / 2), y = px(cy - r.height / 2);
    out.push(`<g><rect x="${x}" y="${y}" width="${px(r.width)}" height="${px(r.height)}" rx="6"`
      + ` fill="${seam ? '#2a0d0c' : '#0B0B0B'}" stroke="${seam ? '#7a2a26' : '#2a2d31'}" stroke-width="1"/>`
      + `<text x="${px(cx)}" y="${px(cy + 4)}" font-size="10.9" text-anchor="middle"`
      + ` font-weight="${seam ? 600 : 400}" fill="${seam ? '#ffd7d4' : '#c8d5cd'}">${esc(l.textContent)}</text></g>`);
  });

  // title block + legend, in the empty top-left of the canvas
  const legend = [['base','base / framework'],['llm','llm'],['agent','agent'],['api','fastapi + react'],
                  ['mcp','datarobot-mcp'],['aux','optional components'],['tool','tooling'],['ext','platform / people']];
  let lx = 42;
  const lg = legend.map(([k, label]) => {
    const s = `<rect x="${lx}" y="88" width="10" height="10" rx="2.5" fill="${C[k]}"/>`
      + `<text x="${lx + 15}" y="97" font-size="11.5" fill="#8f9d94">${esc(label)}</text>`;
    lx += 15 + label.length * 6.2 + 20;
    return s;
  }).join('');
  const lines = [
    `<line x1="${lx}" y1="93" x2="${lx + 22}" y2="93" stroke="${C.seam}" stroke-width="2"/>`
      + `<text x="${lx + 29}" y="97" font-size="11.5" fill="#8f9d94">numbered flow</text>`,
  ];
  lx += 22 + 29 + 'numbered flow'.length * 6.2 + 20;
  lines.push(`<line x1="${lx}" y1="93" x2="${lx + 22}" y2="93" stroke="${C.base}" stroke-width="2" stroke-dasharray="5 4"/>`
    + `<text x="${lx + 29}" y="97" font-size="11.5" fill="#8f9d94">template render</text>`);
  lx += 22 + 29 + 'template render'.length * 6.2 + 20;
  lines.push(`<line x1="${lx}" y1="93" x2="${lx + 22}" y2="93" stroke="${C.api}" stroke-width="2" stroke-dasharray="5 4"/>`
    + `<text x="${lx + 29}" y="97" font-size="11.5" fill="#8f9d94">runtime call</text>`);

  out.push(`<text x="42" y="42" font-size="21" font-weight="600" fill="#ffffff">DataRobot App Framework</text>`
    + `<text x="42" y="66" font-size="13" fill="#8f9d94">From component catalog to running application — an app is composed from versioned copier templates, then provisioned as code.</text>`
    + lg + lines.join(''));

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${STAGE_W} ${HEIGHT}" width="${STAGE_W}" height="${HEIGHT}"`
    + ` font-family="DM Sans, Inter, Helvetica, Arial, sans-serif" role="img"`
    + ` aria-label="DataRobot App Framework architecture: component catalog, recipe repository, local development, deploy and DataRobot platform runtime">`
    + `<title>DataRobot App Framework architecture</title>\n` + out.join('\n') + `\n</svg>`;

  const ta = document.createElement('textarea');
  ta.id = 'svgout';
  ta.textContent = svg;
  document.body.appendChild(ta);
  document.title = 'SVGREADY';
}, 900);
</script>
"""


def main() -> int:
    build = HERE / ".build"
    build.mkdir(exist_ok=True)
    (build / "export.html").write_text(
        SOURCE.read_text().replace("</body>", EXPORT_JS + "</body>")
    )
    dom = subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--virtual-time-budget=6000",
            "--window-size=2400,1600",
            "--dump-dom",
            f"file://{build}/export.html",
        ],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    m = re.search(r'<textarea id="svgout">(.*?)</textarea>', dom, re.DOTALL)
    if not m:
        print("export failed - no svgout in DOM", file=sys.stderr)
        return 1

    svg_path = IMG / "architecture-overview.svg"
    svg_path.write_text(html.unescape(m.group(1)))
    print(f"wrote {svg_path.relative_to(HERE.parent.parent)}")

    # PNG at 2x, via a wrapper page so the SVG is rasterised at a fixed size
    (build / "shot.html").write_text(
        "<!doctype html><meta charset='utf-8'>"
        "<style>html,body{margin:0;background:#0B0B0B}"
        f"img{{display:block;width:{WIDTH}px;height:{HEIGHT}px}}</style>"
        f"<img src='file://{svg_path}'>"
    )
    png_path = IMG / "architecture-overview.png"
    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            f"--window-size={WIDTH},{HEIGHT}",
            "--force-device-scale-factor=2",
            "--hide-scrollbars",
            f"--screenshot={png_path}",
            f"file://{build}/shot.html",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    print(f"wrote {png_path.relative_to(HERE.parent.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
