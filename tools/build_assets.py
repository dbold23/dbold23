"""Generate the SVG artwork for the profile README.

Run from the repo root: python3 tools/build_assets.py
Every number drawn here is quoted from the source repository named beside it.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

NAVY = "#0b1f33"
DEEP = "#071522"
TEAL = "#2bb3a9"
TEAL_DIM = "#1b6f6b"
AMBER = "#f2a93b"
FOAM = "#e6f2f1"
MIST = "#9fb6c3"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# A stylised white shark in lateral view, snout at x=0, facing left.
SHARK = (
    "M0,42 C18,30 58,22 112,21 L150,19 L168,-20 L196,17 L262,24 L300,31 "
    "L338,-8 L352,-6 L334,38 L356,78 L342,80 L300,47 L262,52 L204,58 "
    "L160,60 L126,94 L112,92 L118,62 L70,62 C36,60 12,54 0,42 Z"
)


def banner():
    import base64
    SPRITE = base64.b64encode((OUT / "white-shark-sprite.webp").read_bytes()).decode()
    rings = "".join(
        f'<circle cx="1110" cy="64" r="12" class="ring" style="animation-delay:{d}s"/>'
        for d in (0, 1.1, 2.2)
    )
    contours = "".join(
        f'<path d="M-20,{y} C200,{y-18} 420,{y+22} 640,{y} S1060,{y-20} 1240,{y+6}" '
        f'fill="none" stroke="{TEAL}" stroke-opacity="{op}" stroke-width="1"/>'
        for y, op in ((210, .16), (234, .12), (258, .09), (282, .06), (186, .08))
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-labelledby="t d">
<title id="t">Dan Sambold</title>
<desc id="d">Marine scientist and research engineer. A 3D white shark swims past a pulsing radio tag.</desc>
<style>
.ring{{fill:none;stroke:{AMBER};stroke-width:2;transform-origin:1110px 64px;animation:ping 3.3s ease-out infinite;opacity:0}}
@keyframes ping{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(9);opacity:0}}}}
.frames{{animation:frames 6s steps(24) infinite}}
@keyframes frames{{to{{transform:translateY(-7200px)}}}}
.swim{{animation:swim 16s ease-in-out infinite alternate}}
@keyframes swim{{from{{transform:translate(560px,0)}}to{{transform:translate(610px,10px)}}}}
.drift{{animation:drift 9s linear infinite}}
@keyframes drift{{from{{transform:translateY(0)}}to{{transform:translateY(-300px)}}}}
@media (prefers-reduced-motion:reduce){{.ring,.swim,.drift,.frames{{animation:none}}.ring{{opacity:.35}}}}
</style>
<defs>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#123a55"/><stop offset=".55" stop-color="{NAVY}"/><stop offset="1" stop-color="{DEEP}"/></linearGradient>
<radialGradient id="sun" cx=".78" cy="-.1" r=".8"><stop offset="0" stop-color="{TEAL}" stop-opacity=".35"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1200" height="300" rx="14" fill="url(#sea)"/>
<rect width="1200" height="300" rx="14" fill="url(#sun)"/>
{contours}
<g class="drift" fill="{FOAM}" fill-opacity=".35">
{"".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((520,280,1.2),(610,330,1),(880,300,1.5),(960,420,1),(1110,360,1.3),(760,460,1),(1160,520,1.1),(450,480,1),(1050,560,1.4),(820,590,1)))}
</g>
<g class="swim"><svg width="560" height="300" viewBox="0 0 560 300" overflow="hidden"><image class="frames" href="data:image/webp;base64,{SPRITE}" width="560" height="7200"/></svg></g>
{rings}
<circle cx="1110" cy="64" r="5" fill="{AMBER}"/>
<text x="1110" y="96" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{AMBER}" fill-opacity=".85">151.2 MHz</text>
<text x="64" y="128" font-family="{FONT}" font-size="54" font-weight="700" fill="{FOAM}">Dan Sambold</text>
<text x="66" y="168" font-family="{FONT}" font-size="24" fill="{TEAL}">Marine scientist and research engineer</text>
<text x="66" y="206" font-family="{FONT}" font-size="16" fill="{MIST}">Computer vision, radio telemetry and field instruments</text>
<text x="66" y="228" font-family="{FONT}" font-size="16" fill="{MIST}">for sharks and the coastal ocean.</text>
</svg>'''
    (OUT / "banner.svg").write_text(svg)


def card(slug, kicker, title, lines, metric, metric_caption, tags, accent=TEAL):
    body = "".join(
        f'<text x="28" y="{104 + i * 21}" font-family="{FONT}" font-size="14" fill="{MIST}">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    x = 28
    chips = []
    for t in tags:
        w = 14 + 7.2 * len(t)
        chips.append(
            f'<rect x="{x}" y="186" width="{w:.0f}" height="22" rx="11" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".45"/>'
            f'<text x="{x + w / 2:.0f}" y="201" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{FOAM}">{escape(t)}</text>'
        )
        x += w + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="228" viewBox="0 0 440 228" role="img" aria-label="{escape(title)}: {escape(' '.join(lines))}">
<rect x=".5" y=".5" width="439" height="227" rx="14" fill="{NAVY}" stroke="{TEAL_DIM}" stroke-opacity=".6"/>
<rect x="0" y="0" width="6" height="228" rx="3" fill="{accent}"/>
<text x="28" y="38" font-family="{MONO}" font-size="11.5" letter-spacing="1.5" fill="{accent}">{escape(kicker.upper())}</text>
<text x="28" y="70" font-family="{FONT}" font-size="23" font-weight="700" fill="{FOAM}">{escape(title)}</text>
{body}
<text x="412" y="70" text-anchor="end" font-family="{FONT}" font-size="26" font-weight="700" fill="{accent}">{escape(metric)}</text>
<text x="412" y="88" text-anchor="end" font-family="{FONT}" font-size="11" fill="{MIST}">{escape(metric_caption)}</text>
{"".join(chips)}
</svg>'''
    (OUT / f"card-{slug}.svg").write_text(svg)


def flow(slug, title, steps, note, accent=TEAL):
    """A left-to-right pipeline diagram with numbered boxes."""
    n = len(steps)
    w_box, gap, top = 150, 26, 64
    width = 40 + n * w_box + (n - 1) * gap
    parts = []
    for i, (head, sub) in enumerate(steps):
        x = 20 + i * (w_box + gap)
        last = i == n - 1
        col = AMBER if last else accent
        parts.append(
            f'<rect x="{x}" y="{top}" width="{w_box}" height="86" rx="10" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".7"/>'
            f'<text x="{x + 12}" y="{top + 24}" font-family="{MONO}" font-size="11" fill="{col}">{i + 1:02d}</text>'
            f'<text x="{x + 12}" y="{top + 47}" font-family="{FONT}" font-size="14.5" font-weight="600" fill="{FOAM}">{escape(head)}</text>'
        )
        for j, s in enumerate(sub):
            parts.append(
                f'<text x="{x + 12}" y="{top + 66 + j * 15}" font-family="{FONT}" font-size="11.5" fill="{MIST}">{escape(s)}</text>'
            )
        if not last:
            ax = x + w_box + 4
            parts.append(
                f'<path d="M{ax},{top + 43} h{gap - 10}" stroke="{MIST}" stroke-width="1.6" marker-end="url(#arr)"/>'
            )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="196" viewBox="0 0 {width} 196" role="img" aria-label="{escape(title)}">
<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{MIST}"/></marker></defs>
<rect x=".5" y=".5" width="{width - 1}" height="195" rx="14" fill="{NAVY}" stroke="{TEAL_DIM}" stroke-opacity=".6"/>
<text x="20" y="38" font-family="{FONT}" font-size="17" font-weight="700" fill="{FOAM}">{escape(title)}</text>
{"".join(parts)}
<text x="20" y="180" font-family="{FONT}" font-size="11.5" fill="{MIST}">{escape(note)}</text>
</svg>'''
    (OUT / f"flow-{slug}.svg").write_text(svg)


def relay_chart():
    """Weakest tag each detector path first validates, synthetic AWGN bench.
    Source: Relay-Cellular docs/RANGE_BUDGET.md, testing/bench_range.py, 2026-09-09.
    Lower (more negative) is better, so bars grow to the left from +12 dB.
    """
    rows = [
        ("Welch survey (old)", 9, "+9 dB"),
        ("STFT survey", -9, "-9 dB"),
        ("Matched filter", -15, "-15 dB"),
        ("MF + fold, 91 s", -18, "-18 dB"),
        ("MF + fold, 141 s", -21, "-21 dB"),
    ]
    W, H = 880, 300
    x0, x1 = 220, 820          # x0 = -24 dB, x1 = +12 dB
    def px(db):
        return x0 + (db + 24) / 36 * (x1 - x0)
    base = px(12)
    out = []
    for g in (-24, -18, -12, -6, 0, 6, 12):
        gx = px(g)
        out.append(f'<line x1="{gx:.1f}" y1="70" x2="{gx:.1f}" y2="{70 + len(rows) * 38}" stroke="{MIST}" stroke-opacity=".15"/>')
        out.append(f'<text x="{gx:.1f}" y="{88 + len(rows) * 38}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{MIST}">{g:+d}</text>')
    for i, (label, db, txt) in enumerate(rows):
        y = 76 + i * 38
        left = px(db)
        col = MIST if i == 0 else TEAL
        out.append(f'<text x="{x0 - 14}" y="{y + 17}" text-anchor="end" font-family="{FONT}" font-size="13" fill="{FOAM}">{escape(label)}</text>')
        out.append(f'<rect x="{left:.1f}" y="{y}" width="{base - left:.1f}" height="24" rx="4" fill="{col}" fill-opacity="{.55 if i == 0 else .85}"/>')
        out.append(f'<text x="{left - 8:.1f}" y="{y + 17}" text-anchor="end" font-family="{FONT}" font-size="12.5" font-weight="600" fill="{FOAM}">{txt}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Weakest in-channel SNR at which each RelayStation detector path first validates a tag, synthetic noise bench: Welch +9 dB, STFT -9 dB, matched filter -15 dB, matched filter with fold -18 dB at 91 s and -21 dB at 141 s.">
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{NAVY}" stroke="{TEAL_DIM}" stroke-opacity=".6"/>
<text x="24" y="36" font-family="{FONT}" font-size="17" font-weight="700" fill="{FOAM}">Weakest tag each detector finds (in-channel SNR, dB)</text>
<text x="24" y="56" font-family="{FONT}" font-size="12" fill="{MIST}">Longer bar = hears a fainter tag. Bench on synthetic noise, 2026-09-09; the outdoor range walk is not yet redone.</text>
{"".join(out)}
</svg>'''
    (OUT / "relay-sensitivity.svg").write_text(svg)


def divider():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="24" viewBox="0 0 1200 24" aria-hidden="true">
<path d="M0,12 C100,2 200,22 300,12 S500,2 600,12 S800,22 900,12 S1100,2 1200,12" fill="none" stroke="{TEAL}" stroke-opacity=".55" stroke-width="2"/>
</svg>'''
    (OUT / "wave.svg").write_text(svg)


if __name__ == "__main__":
    banner()
    divider()
    flow("relay", "RelayStation detection chain",
         [("SDR read", ["128 ms of IQ", "2.048 Msps"]),
          ("STFT survey", ["500 Hz bins, CFAR", "fitted per station"]),
          ("Matched filter", ["per-tag, 16 kHz", "Exp(1) normalised"]),
          ("Period fold", ["finds tags too weak", "for one pulse"]),
          ("Validate + lock", ["5 pulses, then", "report to Central"])],
         "Every channel-frame lands in exactly one pipeline stage, and the counts ride the heartbeat, so a deaf station cannot look healthy.")
    flow("annotator", "The annotation flywheel",
         [("Human labels", ["scar box, type,", "zone, side"]),
          ("Track", ["follow the scar", "across frames"]),
          ("Consensus", ["3+ raters, absence", "counts as a vote"]),
          ("Retrain", ["detector proposes", "the next scar"]),
          ("Verify", ["judge, don't draw", "faster and steadier"])],
         "Built and wired end to end; the first verification round is what turns the loop.", accent=AMBER)
    flow("pose3d", "shark-pose-3d, per-individual fit",
         [("Detect", ["16 keypoints", "YOLOv8-pose"]),
          ("Segment", ["SAM2 silhouette", "per frame"]),
          ("Fit", ["SharkSMPL over a", "window of frames"]),
          ("Measure", ["girth field, station", "chords, proportions"]),
          ("Ledger", ["per-individual record", "with refusals"])],
         "Length proportions are quotable; absolute girth waits on an external calibration (drone stations).")
    relay_chart()
    print("wrote", sorted(p.name for p in OUT.iterdir()))


def spin_tile(slug, title, sub, n=36, w=560, h=280):
    """A tile with a turntable of one of the site's 3D shark models (sprite rendered with three.js)."""
    import base64
    sprite = base64.b64encode((OUT / f"{slug}-spin.webp").read_bytes()).decode()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h + 70}" viewBox="0 0 {w} {h + 70}" role="img" aria-label="{escape(title)}, rotating 3D model">
<style>.f{{animation:f 9s steps({n}) infinite}}@keyframes f{{to{{transform:translateY(-{n * h}px)}}}}@media (prefers-reduced-motion:reduce){{.f{{animation:none}}}}</style>
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#123a55"/><stop offset="1" stop-color="{DEEP}"/></linearGradient>
<clipPath id="r"><rect width="{w}" height="{h + 70}" rx="14"/></clipPath></defs>
<g clip-path="url(#r)"><rect width="{w}" height="{h + 70}" fill="url(#bg)"/>
<ellipse cx="{w / 2}" cy="{h - 18}" rx="{w * .3}" ry="14" fill="#000" fill-opacity=".25"/>
<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" overflow="hidden"><image class="f" href="data:image/webp;base64,{sprite}" width="{w}" height="{n * h}"/></svg></g>
<text x="20" y="{h + 32}" font-family="{FONT}" font-size="20" font-weight="700" fill="{FOAM}">{escape(title)}</text>
<text x="20" y="{h + 54}" font-family="{FONT}" font-size="13" fill="{MIST}">{escape(sub)}</text>
<text x="{w - 20}" y="{h + 42}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{AMBER}">click to spin it yourself</text>
<rect x=".5" y=".5" width="{w - 1}" height="{h + 69}" rx="14" fill="none" stroke="{TEAL_DIM}" stroke-opacity=".7"/>
</svg>'''
    (OUT / f"spin-{slug}.svg").write_text(svg)


if __name__ == "__main__":
    spin_tile("white-shark", "White shark", "Carcharodon carcharias")
    spin_tile("leopard-shark", "Leopard shark", "Triakis semifasciata")
