"""Geometry check for the interactive architecture blueprint.

Loads docs/src/architecture.html in headless Chrome at scale 1 and reports:

* pairs of canvas elements that overlap by more than 3px,
* boxes whose text is clipped by the box,
* anything positioned outside the stage bounds,
* dangling references in the tour (STEPS) and drawer cross-navigation pills.

Exits non-zero if anything is wrong.
"""

import json
import os
import pathlib
import re
import subprocess
import sys

CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
HERE = pathlib.Path(__file__).parent
SOURCE = HERE.parent.parent / "docs" / "src" / "architecture.html"

PROBE = r"""
<script>
setTimeout(() => {
  const out = {overlaps: [], clipped: [], oob: []};
  try {
    setScale(1);
    const SEL = '.node,.wlabel,.ptitle,.psub,.subhead,.notes';
    const els = [...document.querySelectorAll(SEL)].filter(e => {
      const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
    const desc = e => String(e.className).split(' ')[0]
      + (e.dataset && e.dataset.id ? '#' + e.dataset.id : '')
      + ':' + (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 34);
    const rects = els.map(e => e.getBoundingClientRect());
    let total = 0;
    for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
      if (els[i].contains(els[j]) || els[j].contains(els[i])) continue;
      const a = rects[i], b = rects[j];
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      const oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 3 && oy > 3) {
        total++;
        if (out.overlaps.length < 40)
          out.overlaps.push({a: desc(els[i]), b: desc(els[j]),
                             ox: Math.round(ox), oy: Math.round(oy)});
      }
    }
    out.totalOverlaps = total;
    document.querySelectorAll('.node').forEach(n => {
      if (n.scrollHeight > n.clientHeight + 1 || n.scrollWidth > n.clientWidth + 1)
        out.clipped.push(n.dataset.id);
    });
    const st = document.getElementById('stage').getBoundingClientRect();
    out.oob = [...document.querySelectorAll('.node,.notes,.wlabel')].filter(e => {
      const r = e.getBoundingClientRect();
      return r.left < st.left - 2 || r.right > st.right + 2 || r.bottom > st.bottom + 2;
    }).map(desc);
    // dangling references
    const nodeIds = new Set(N.map(n => n.id));
    const edges = new Set(A.map(a => a.f + '->' + a.t));
    out.badRefs = [];
    STEPS.forEach((s, i) => {
      s.nodes.forEach(id => { if (!nodeIds.has(id)) out.badRefs.push(`STEPS[${i}].nodes ${id}`); });
      s.arrows.forEach(k => { if (!edges.has(k)) out.badRefs.push(`STEPS[${i}].arrows ${k}`); });
    });
    nodeIds.forEach(id => { if (!D[id]) out.badRefs.push(`no drawer for ${id}`); });
    document.querySelectorAll('#drawer, #stage').forEach(() => {});
    Object.entries(D).forEach(([id, d]) => {
      [...(d.b || '').matchAll(/data-node="([^"]+)"/g)]
        .forEach(m => { if (!nodeIds.has(m[1])) out.badRefs.push(`${id} pill -> ${m[1]}`); });
    });
    out.counts = {nodes: N.length, arrows: A.length, steps: STEPS.length,
                  drawers: Object.keys(D).length};
    out.ok = total === 0 && !out.clipped.length && !out.oob.length && !out.badRefs.length;
  } catch (err) { out.error = String(err); out.ok = false; }
  document.title = 'RESULT::' + JSON.stringify(out);
}, 900);
</script>
"""


def main() -> int:
    build = HERE / ".build"
    build.mkdir(exist_ok=True)
    probe = build / "audit.html"
    probe.write_text(SOURCE.read_text().replace("</body>", PROBE + "</body>"))
    dom = subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--virtual-time-budget=6000",
            "--window-size=2400,1600",
            "--dump-dom",
            f"file://{probe}",
        ],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    m = re.search(r"RESULT::([^<]*)", dom)
    if not m:
        print("audit failed - page did not report a result", file=sys.stderr)
        return 1
    d = json.loads(m.group(1))

    if d.get("error"):
        print(f"error: {d['error']}", file=sys.stderr)
    for o in d.get("overlaps", []):
        print(f"overlap  {o['a']}  ||  {o['b']}  ({o['ox']}x{o['oy']}px)")
    for c in d.get("clipped", []):
        print(f"clipped  {c}")
    for o in d.get("oob", []):
        print(f"outside  {o}")
    for r in d.get("badRefs", []):
        print(f"bad ref  {r}")

    counts = d.get("counts", {})
    status = "ok" if d.get("ok") else "FAILED"
    print(
        f"{status} - {counts.get('nodes')} nodes, {counts.get('arrows')} arrows, "
        f"{counts.get('steps')} tour steps, {counts.get('drawers')} drawers"
    )
    return 0 if d.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
