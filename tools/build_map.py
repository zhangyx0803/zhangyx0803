# -*- coding: utf-8 -*-
"""Build a theme-aware China locator map (SVG) for the GitHub profile README.

Projection: Albers equal-area conic (standard parallels 25N/47N, central meridian 105E).
Input: china.json (DataV province boundaries, GeoJSON).
Output: assets/china-map-light.svg, assets/china-map-dark.svg
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "china.json")
OUT = os.path.join(ROOT, "assets")

W, H = 760, 560
PAD = 26
PHI1, PHI2, PHI0, LAM0 = 25.0, 47.0, 35.0, 105.0
CITY = {"lon": 121.4050, "lat": 31.1650, "name": "Xuhui"}
HIGHLIGHT = {"上海市"}
SKIP_ADCODE = {"100000_JD"}          # 南海诸岛九段线，缩放到全国时会压低主体
GRID_LON = list(range(80, 141, 20))
GRID_LAT = list(range(20, 61, 20))
EPS = 0.45


def albers(lon, lat):
    p1, p2, p0, l0 = map(math.radians, (PHI1, PHI2, PHI0, LAM0))
    lam, phi = math.radians(lon), math.radians(lat)
    n = (math.sin(p1) + math.sin(p2)) / 2.0
    c = math.cos(p1) ** 2 + 2 * n * math.sin(p1)
    rho0 = math.sqrt(c - 2 * n * math.sin(p0)) / n
    rho = math.sqrt(max(c - 2 * n * math.sin(phi), 0.0)) / n
    theta = n * (lam - l0)
    return rho * math.sin(theta), rho0 - rho * math.cos(theta)


def rdp(points, eps):
    if len(points) < 3:
        return points
    first, last = points[0], points[-1]
    dmax, index = 0.0, 0
    for i in range(1, len(points) - 1):
        px, py = points[i]
        dx, dy = last[0] - first[0], last[1] - first[1]
        norm = math.hypot(dx, dy)
        dist = (abs(dy * px - dx * py + last[0] * first[1] - last[1] * first[0]) / norm
                if norm else math.hypot(px - first[0], py - first[1]))
        if dist > dmax:
            dmax, index = dist, i
    if dmax > eps:
        return rdp(points[: index + 1], eps)[:-1] + rdp(points[index:], eps)
    return [first, last]


def rings_of(geom):
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    if geom["type"] == "MultiPolygon":
        return [ring for poly in geom["coordinates"] for ring in poly]
    return []


def main():
    with open(SRC, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    feats = []
    for feature in data["features"]:
        props = feature.get("properties") or {}
        name = props.get("name") or ""
        adcode = str(props.get("adcode") or "")
        if adcode in SKIP_ADCODE or not name:
            continue
        rings = rings_of(feature["geometry"])
        # 三沙等远海岛礁会把包围盒拉到赤道，缩放到全国时主体被压小
        rings = [r for r in rings if r and sum(c[1] for c in r) / len(r) >= 15.0]
        if rings:
            feats.append((name, rings))

    xs, ys, projected = [], [], []
    for name, rings in feats:
        out = []
        for ring in rings:
            pts = []
            for coord in ring:
                x, y = albers(coord[0], coord[1])
                pts.append((x, y))
                xs.append(x)
                ys.append(y)
            out.append(pts)
        projected.append((name, out))

    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    scale = min((W - 2 * PAD) / (x1 - x0), (H - 2 * PAD) / (y1 - y0))
    ox = PAD + ((W - 2 * PAD) - (x1 - x0) * scale) / 2
    oy = PAD + ((H - 2 * PAD) - (y1 - y0) * scale) / 2

    def to_px(x, y):
        return ox + (x - x0) * scale, oy + (y1 - y) * scale

    def path_of(rings):
        parts = []
        for pts in rings:
            px = rdp([to_px(x, y) for x, y in pts], EPS)
            if len(px) < 3:
                continue
            parts.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in px) + "Z")
        return " ".join(parts)

    provinces, highlight = [], []
    for name, rings in projected:
        d = path_of(rings)
        if d:
            (highlight if name in HIGHLIGHT else provinces).append((name, d))

    cx, cy = to_px(*albers(CITY["lon"], CITY["lat"]))

    seg = []
    for lon in GRID_LON:
        seg.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (to_px(*albers(lon, lat)) for lat in range(15, 55))))
    for lat in GRID_LAT:
        seg.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (to_px(*albers(lon, lat)) for lon in range(70, 140))))
    grid_d = " ".join(seg)

    lon_ticks = "\n".join(
        f'    <text x="{to_px(*albers(lon, 17.0))[0]:.0f}" y="{H - 9}" text-anchor="middle">{lon}°E</text>'
        for lon in GRID_LON if 76 <= lon <= 132
    )
    lat_ticks = "\n".join(
        f'    <text x="6" y="{to_px(*albers(73.0, lat))[1] + 3:.0f}">{lat}°N</text>'
        for lat in GRID_LAT
    )
    lon_ticks_marks = "\n".join(
        f'    <path d="M{to_px(*albers(lon, 17.0))[0]:.0f},{H - 18} v6"/>'
        for lon in GRID_LON if 76 <= lon <= 132
    )
    lat_ticks_marks = "\n".join(
        f'    <path d="M14,{to_px(*albers(73.0, lat))[1]:.0f} h6"/>'
        for lat in GRID_LAT
    )

    themes = {
        "light": dict(
            bg="#ffffff", prov_fill="#eef3f8", prov_stroke="#c1cedd", hl_fill="#3ba55d",
            hl_stroke="#1f7a3d", grid="#dde6ef", text="#5b6b7c", accent="#3ba55d",
            chip_fill="#ffffff", chip_stroke="#d7e0ea",
        ),
        "dark": dict(
            bg="#0d1117", prov_fill="#161d26", prov_stroke="#2e3947", hl_fill="#3fb950",
            hl_stroke="#7ee787", grid="#1c2632", text="#7d8b9c", accent="#3fb950",
            chip_fill="#0d1117", chip_stroke="#28323f",
        ),
    }

    for theme, c in themes.items():
        prov_paths = "\n".join(f'    <path d="{d}"/>' for _, d in provinces)
        hl_paths = "\n".join(f'    <path class="hl" d="{d}"/>' for _, d in highlight)
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Xuhui, Shanghai on the map of China, 31.1650N 121.4050E">
  <style>
    .prov {{ fill: {c["prov_fill"]}; stroke: {c["prov_stroke"]}; stroke-width: 0.55; stroke-linejoin: round; }}
    .hl   {{ fill: {c["hl_fill"]}; stroke: {c["hl_stroke"]}; stroke-width: 0.7; }}
    .grid {{ fill: none; stroke: {c["grid"]}; stroke-width: 0.5; stroke-dasharray: 2 5; }}
    text  {{ fill: {c["text"]}; font: 10.5px/1 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .cap  {{ font-size: 10px; letter-spacing: 0.14em; }}
    .big  {{ font-size: 13px; font-weight: 600; letter-spacing: 0.02em; paint-order: stroke; stroke: {c["bg"]}; stroke-width: 3px; }}
    .accent {{ fill: {c["accent"]}; font-weight: 700; }}
  </style>
  <defs>
    <clipPath id="box"><rect x="{PAD - 10}" y="{PAD - 10}" width="{W - 2 * PAD + 20}" height="{H - 2 * PAD - 44}"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" fill="{c["bg"]}"/>
  <g stroke="{c["grid"]}" stroke-width="1">
{lon_ticks_marks}
{lat_ticks_marks}
  </g>
{lon_ticks}
{lat_ticks}
  <g class="prov">
{prov_paths}
  </g>
  <g>
{hl_paths}
  </g>
  <text class="cap" x="{PAD}" y="20">GEO · PROFILE ／ 34 PROVINCE-LEVEL UNITS</text>
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" fill="{c["accent"]}"/>
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" fill="none" stroke="{c["accent"]}" stroke-width="1.2">
    <animate attributeName="r" values="4;14" dur="2.6s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.8;0" dur="2.6s" repeatCount="indefinite"/>
  </circle>
  <text class="big" x="{cx + 9:.0f}" y="{cy - 8:.0f}">徐汇</text>
  <g transform="translate(18,{H - 84})">
    <rect x="0" y="0" width="272" height="50" rx="8" fill="{c["chip_fill"]}" stroke="{c["chip_stroke"]}"/>
    <text class="big" x="13" y="20">XUHUI · 上海</text>
    <text x="13" y="36">{CITY["lat"]}°N  {CITY["lon"]}°E  ·  Albers 25°N/47°N</text>
  </g>
  <g transform="translate({W - 32},{H - 84})">
    <path d="M0,-17 L6,7 L0,1.5 L-6,7 Z" fill="{c["text"]}"/>
    <text x="0" y="24" text-anchor="middle" class="cap">N</text>
  </g>
</svg>
'''
        target = os.path.join(OUT, f"china-map-{theme}.svg")
        with open(target, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(svg)
        print(f"wrote {target} ({os.path.getsize(target)} bytes, {len(provinces)} provinces + {len(highlight)} highlight)")


if __name__ == "__main__":
    sys.exit(main())
