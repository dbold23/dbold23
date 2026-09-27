"""Photo tiles and the hero strip, built from images already on dbold23.github.io.

Each tile is an SVG that embeds one photo (cropped to fill) with a short label, so
every tile in the README grid has the same shape whatever the source aspect ratio.
Run from the repo root: python3 tools/build_photos.py <path-to-dbold23.github.io/assets>
"""
import base64
import sys
from pathlib import Path
from xml.sax.saxutils import escape

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("../dbold23.github.io/assets")
OUT = Path(__file__).resolve().parent.parent / "assets" / "tiles"
OUT.mkdir(parents=True, exist_ok=True)
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
MIME = {".avif": "image/avif", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def data_uri(rel):
    p = SRC / rel
    return f"data:{MIME[p.suffix.lower()]};base64,{base64.b64encode(p.read_bytes()).decode()}"


def tile(slug, rel, kicker, title, stat="", accent="#2bb3a9", w=400, h=260, pos="xMidYMid"):
    stat_svg = ""
    if stat:
        sw = 16 + 8 * len(stat)
        stat_svg = (f'<rect x="{w - sw - 14}" y="14" width="{sw}" height="28" rx="14" fill="#071522" fill-opacity=".72"/>'
                    f'<text x="{w - 14 - sw / 2}" y="33" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="{accent}">{escape(stat)}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<defs><clipPath id="r"><rect width="{w}" height="{h}" rx="14"/></clipPath>
<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset=".45" stop-color="#071522" stop-opacity="0"/><stop offset="1" stop-color="#071522" stop-opacity=".92"/></linearGradient></defs>
<g clip-path="url(#r)"><image href="{data_uri(rel)}" width="{w}" height="{h}" preserveAspectRatio="{pos} slice"/>
<rect width="{w}" height="{h}" fill="url(#g)"/></g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{accent}" stroke-opacity=".55"/>
{stat_svg}
<text x="18" y="{h - 46}" font-family="{MONO}" font-size="11" letter-spacing="1.4" fill="{accent}">{escape(kicker.upper())}</text>
<text x="18" y="{h - 20}" font-family="{FONT}" font-size="21" font-weight="700" fill="#e6f2f1">{escape(title)}</text>
</svg>'''
    (OUT / f"{slug}.svg").write_text(svg)


def strip(slug, rels, w=1200, h=230, gap=10):
    n = len(rels)
    cw = (w - gap * (n - 1)) / n
    parts = []
    for i, (rel, pos) in enumerate(rels):
        x = i * (cw + gap)
        parts.append(f'<clipPath id="c{i}"><rect x="{x:.1f}" width="{cw:.1f}" height="{h}" rx="12"/></clipPath>'
                     f'<image clip-path="url(#c{i})" href="{data_uri(rel)}" x="{x:.1f}" width="{cw:.1f}" height="{h}" preserveAspectRatio="{pos} slice"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Field work photos">{"".join(parts)}</svg>'
    (OUT / f"{slug}.svg").write_text(svg)


if __name__ == "__main__":
    strip("field-strip", [
        ("panels/sa-divegear.avif", "xMidYMid"),
        ("me with a shark tag and antena.avif", "xMidYMid"),
        ("relay-station-sunset.avif", "xMidYMid"),
        ("small image of me presenting my shark research.avif", "xMidYMid"),
    ])
    tile("pose3d", "pres/shark-3.avif", "3D shape from video", "shark-pose-3d", "250 sharks")
    tile("annotator", "shark-annotator-zones.png", "Live annotation app", "Shark Scar Annotator", "live", accent="#f2a93b", pos="xMinYMid")
    tile("relay", "pres/relay-1.avif", "Radio telemetry", "RelayStation", "-21 dB")
    tile("sevengill-dummy", "/tmp/pa2/76-sevengill-dummy-preview.jpg", "Life-size, my CAD", "2 m sevengill handling dummy", "3D", w=640, h=360)
    tile("relay-tripod", "/tmp/pa/revg-render.jpg", "RELAY Rev G, my CAD", "Field station", "3D", pos="xMidYMax", w=560, h=350)
    tile("anchor", "panels/anchor-track-map.avif", "Biologging", "anchor", "v0.1", accent="#f2a93b")
    tile("porpoise", "panels/porpoise-match.avif", "Photo re-ID", "PorpoiseID", "198 animals")
    tile("fathomnet", "panels/fathomnet-masks.avif", "MBARI, summer 2026", "FathomNet", accent="#f2a93b")
    tile("urchins", "panels/urchin-tank.avif", "Aquaculture", "Purple urchin ranching")
    tile("tecan", "tecan-confusion-matrix.png", "Open source", "TECAN growth curves", accent="#f2a93b")
    tile("relay-field", "panels/fieldops.avif", "Fieldwork", "In the water", accent="#2bb3a9")
    print(sorted(p.name for p in OUT.iterdir()))
