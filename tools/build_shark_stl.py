"""A low-poly white shark as an ASCII STL, small enough to render inline on GitHub.

GitHub draws a ```stl block as a model you can orbit and zoom. The body is lofted
from elliptical cross-sections along a length profile; the fins are thin plates.
Run: python3 tools/build_shark_stl.py  ->  assets/shark.stl and prints the block size.
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "shark.stl"
STATIONS = 18   # along the body
RING = 12       # around the girth


def half_sizes(s):
    """Half height and half width of the body at station s in [0, 1] (snout to peduncle)."""
    # Fusiform: fast rise from the snout, widest near 0.35, tapering to a narrow peduncle.
    u = min(1.0, s)
    h = 0.60 * math.sin(math.pi * u ** 0.85) ** 0.95 + 0.035
    w = 0.50 * math.sin(math.pi * u ** 0.82) ** 1.1 + 0.03
    return h, w


def body():
    L = 4.0
    rings = []
    for i in range(STATIONS + 1):
        s = i / STATIONS
        h, w = half_sizes(s)
        zc = 0.08 * math.sin(math.pi * s) - 0.05 * s   # slight arch of the back
        ring = []
        for j in range(RING):
            a = 2 * math.pi * j / RING
            ring.append((s * L, w * math.sin(a), zc + h * math.cos(a) * (1.0 if math.cos(a) > 0 else 0.82)))
        rings.append(ring)
    tris = []
    for i in range(STATIONS):
        for j in range(RING):
            a, b = rings[i][j], rings[i][(j + 1) % RING]
            c, d = rings[i + 1][j], rings[i + 1][(j + 1) % RING]
            tris += [(a, c, b), (b, c, d)]
    for i, tip in ((0, (-0.28, 0.0, -0.06)), (STATIONS, None)):
        if tip is None:
            continue
        ring = rings[i]
        tris += [(tip, ring[(j + 1) % RING], ring[j]) for j in range(RING)]
    tail_ring = rings[-1]
    cx = sum(p[0] for p in tail_ring) / RING
    cz = sum(p[2] for p in tail_ring) / RING
    tris += [((cx, 0.0, cz), tail_ring[j], tail_ring[(j + 1) % RING]) for j in range(RING)]
    return tris, cz


def plate(pts, thick=0.03, axis=1):
    """A fin: a polygon extruded a little along one axis, both faces plus the rim."""
    off = [0, 0, 0]
    off[axis] = thick / 2
    top = [tuple(p[k] + off[k] for k in range(3)) for p in pts]
    bot = [tuple(p[k] - off[k] for k in range(3)) for p in pts]
    tris = []
    for k in range(1, len(pts) - 1):
        tris.append((top[0], top[k], top[k + 1]))
        tris.append((bot[0], bot[k + 1], bot[k]))
    for k in range(len(pts)):
        a, b = top[k], top[(k + 1) % len(pts)]
        c, d = bot[k], bot[(k + 1) % len(pts)]
        tris += [(a, c, b), (b, c, d)]
    return tris


def fins(tail_z):
    t = []
    t += plate([(1.25, 0, 0.62), (1.95, 0, 0.55), (1.55, 0, 1.22)])                    # first dorsal
    t += plate([(3.05, 0, 0.18), (3.25, 0, 0.16), (3.18, 0, 0.32)])                    # second dorsal
    for side in (1, -1):                                                              # pectorals
        t += plate([(1.02, side * 0.38, -0.34), (1.45, side * 0.36, -0.40), (1.72, side * 1.25, -0.78)], axis=2)
    for side in (1, -1):                                                              # pelvics
        t += plate([(2.55, side * 0.18, -0.30), (2.78, side * 0.16, -0.26), (2.86, side * 0.42, -0.46)], axis=2)
    z = tail_z
    t += plate([(3.86, 0, z + 0.10), (4.10, 0, z - 0.06), (4.62, 0, z + 1.02), (4.44, 0, z + 1.06)])   # upper caudal lobe
    t += plate([(3.90, 0, z - 0.06), (4.10, 0, z + 0.04), (4.50, 0, z - 0.84), (4.34, 0, z - 0.88)])   # lower caudal lobe
    return t


def normal(a, b, c):
    u = [b[k] - a[k] for k in range(3)]
    v = [c[k] - a[k] for k in range(3)]
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    m = math.sqrt(sum(x * x for x in n)) or 1
    return tuple(x / m for x in n)


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".") if x else "0"


if __name__ == "__main__":
    b, tail_z = body()
    tris = b + fins(tail_z)
    lines = ["solid shark"]
    for a, bb, c in tris:
        n = normal(a, bb, c)
        lines.append(f"facet normal {' '.join(f(x) for x in n)}\nouter loop")
        lines += [f"vertex {f(p[0])} {f(p[1])} {f(p[2])}" for p in (a, bb, c)]
        lines.append("endloop\nendfacet")
    lines.append("endsolid shark")
    OUT.write_text("\n".join(lines) + "\n")
    print(len(tris), "triangles,", OUT.stat().st_size, "bytes")
