# -*- coding: utf-8 -*-
"""Build a three-panel "Figure 1 · Study area locator" atlas for the GitHub profile.

Panels: China (provinces) -> Yangtze River Delta (1 deg graticule) -> Shanghai (districts).
One projection for all panels (Albers equal-area, 25N/47N, lon0=105E), three viewports,
so the plate reads like a real cartographic figure: neatlines, graticule, scale bars,
legend, zoom callouts.

Outputs assets/geo-atlas-{light,dark}.svg
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "assets")

W, H = 980, 456
PANEL_Y, PANEL_H = 54, 340
PAD = 15

PANELS = [
    # key, x, w, title_en, title_cn, bbox, grid step, label step, simplify(px)
    ("cn", 26, 330, "A · China", "中国", (73.0, 17.5, 135.5, 53.8), 10.0, 20.0, 0.70),
    ("yrd", 372, 258, "B · Yangtze River Delta", "长江三角洲", (117.6, 29.4, 122.4, 33.0), 1.0, 2.0, 1.00),
    ("sh", 646, 308, "C · Shanghai Municipality", "上海市域", (120.83, 30.67, 122.02, 31.88), 0.25, 0.5, 0.25),
]
PHI1, PHI2, PHI0, LAM0 = 25.0, 47.0, 35.0, 105.0
CAMPUS = (121.4050, 31.1650)

# name, lon, lat, highlighted, dx, dy, anchor
CITIES = [
    ("上海 Shanghai", 121.4737, 31.2304, True, 0, -13, "middle"),
    ("南京 Nanjing", 118.7969, 32.0603, False, 6, -5, "start"),
    ("杭州 Hangzhou", 120.1551, 30.2741, False, 6, 8, "start"),
    ("合肥 Hefei", 117.2809, 31.8639, False, 7, 8, "start"),
    ("苏州 Suzhou", 120.5853, 31.2989, False, -6, 7, "end"),
    ("宁波 Ningbo", 121.5503, 29.8746, False, 6, 9, "start"),
]
HIGHLIGHT_CITY = "上海 Shanghai"
HIGHLIGHT_DISTRICT = "徐汇区"


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
    dx, dy = last[0] - first[0], last[1] - first[1]
    norm = math.hypot(dx, dy)
    dmax, index = 0.0, 0
    for i in range(1, len(points) - 1):
        px, py_ = points[i]
        dist = (abs(dy * px - dx * py_ + last[0] * first[1] - last[1] * first[0]) / norm
                if norm else math.hypot(px - first[0], py_ - first[1]))
        if dist > dmax:
            dmax, index = dist, i
    if dmax > eps:
        return rdp(points[: index + 1], eps)[:-1] + rdp(points[index:], eps)
    return [first, last]


def rings_of(geom):
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    if geom["type"] == "MultiPolygon":
        return [r for poly in geom["coordinates"] for r in poly]
    return []


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    out = []
    for feature in doc["features"]:
        props = feature.get("properties") or {}
        name = str(props.get("name") or "")
        if not name:
            continue
        rings = [r for r in rings_of(feature["geometry"]) if len(r) > 3]
        rings = [r for r in rings if sum(pt[1] for pt in r) / len(r) >= 15.0]
        if rings:
            out.append((name, rings))
    return out


class Panel:
    def __init__(self, x, y, w, h, bbox, eps):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.eps = eps
        lon0, lat0, lon1, lat1 = bbox
        self.lon0, self.lat0, self.lon1, self.lat1 = bbox
        corners = [albers(lon0, lat0), albers(lon1, lat0), albers(lon0, lat1), albers(lon1, lat1)]
        xs, ys = [c[0] for c in corners], [c[1] for c in corners]
        self.mnx, self.mxx, self.mny, self.mxy = min(xs), max(xs), min(ys), max(ys)
        inner_w, inner_h = w - 2 * PAD, h - 2 * PAD
        self.scale = min(inner_w / (self.mxx - self.mnx), inner_h / (self.mxy - self.mny))
        self.ox = x + PAD + (inner_w - (self.mxx - self.mnx) * self.scale) / 2
        self.oy = y + PAD + (inner_h - (self.mxy - self.mny) * self.scale) / 2

    def px(self, lon, lat):
        mx, my = albers(lon, lat)
        return self.ox + (mx - self.mnx) * self.scale, self.oy + (self.mxy - my) * self.scale

    def path(self, rings):
        parts = []
        for ring in rings:
            pts = [self.px(x, y) for x, y in ring]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            if (max(xs) - min(xs)) < 2.0 and (max(ys) - min(ys)) < 2.0:
                continue
            pts = rdp(pts, self.eps)
            if len(pts) < 3:
                continue
            parts.append("M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts) + "Z")
        return " ".join(parts)

    def meters_per_px(self):
        lat_mid = (self.lat0 + self.lat1) / 2
        a = self.px(120.0, lat_mid)
        b = self.px(121.0, lat_mid)
        ground = 111320.0 * math.cos(math.radians(lat_mid))
        return ground / math.hypot(b[0] - a[0], b[1] - a[1])

    def scale_bar(self, target_px=78):
        mpp = self.meters_per_px()
        raw = target_px * mpp
        mag = 10 ** math.floor(math.log10(raw))
        nice = min((n * mag for n in (1, 2, 5, 10)), key=lambda v: abs(v - raw))
        return nice, nice / mpp


def nice_label(meters):
    if meters >= 1000:
        return f"{meters / 1000:g} km"
    return f"{meters:g} m"


THEMES = {
    "light": dict(
        bg="#ffffff", sea="#f2f7fb", neat="#b9c7d6", land="#e6edf4", land_stroke="#b8c7d6",
        graticule="#dfe8f1", text="#4a5a6b", muted="#8d9cab", accent="#2f9e56", accent_dark="#1d6b3b",
        city="#7b8d9f", halo="#ffffff",
    ),
    "dark": dict(
        bg="#0d1117", sea="#0b1016", neat="#2b3644", land="#18212b", land_stroke="#334051",
        graticule="#1b2531", text="#94a3b3", muted="#5f6b79", accent="#3fb950", accent_dark="#7ee787",
        city="#6e7d8d", halo="#0d1117",
    ),
}


def build_theme(theme):
    c = THEMES[theme]
    provinces = load(os.path.join(DATA, "china.json"))
    districts = load(os.path.join(DATA, "shanghai.json"))

    panels = {}
    for key, x, w, _en, _cn, bbox, _step, _lstep, eps in PANELS:
        panels[key] = Panel(x, PANEL_Y, w, PANEL_H, bbox, eps)

    body = []

    def graticule(panel, step, label_step):
        lon = math.ceil(panel.lon0 / step) * step
        lat = math.ceil(panel.lat0 / step) * step
        lines, labels = [], []
        while lon <= panel.lon1 + 1e-9:
            x, _ = panel.px(lon, panel.lat0)
            lines.append(f"M{x:.1f},{panel.y} V{panel.y + panel.h}")
            if abs(lon / label_step - round(lon / label_step)) < 1e-6:
                labels.append((x, f"{lon:g}°E", "lon"))
            lon += step
        while lat <= panel.lat1 + 1e-9:
            _, y = panel.px(panel.lon0, lat)
            lines.append(f"M{panel.x},{y:.1f} H{panel.x + panel.w}")
            if abs(lat / label_step - round(lat / label_step)) < 1e-6:
                labels.append((y, f"{lat:g}°N", "lat"))
            lat += step
        return " ".join(lines), labels

    for key, x, w, title_en, title_cn, bbox, step, lstep, eps in PANELS:
        p = panels[key]
        grid_d, labels = graticule(p, step, lstep)

        body.append(f'<g clip-path="url(#clip-{theme}-{key})">')
        body.append(f'  <path class="grid" d="{grid_d}"/>')
        if key == "sh":
            for name, rings in districts:
                cls = "hl" if name == HIGHLIGHT_DISTRICT else "land"
                body.append(f'  <path class="{cls}" d="{p.path(rings)}"/>')
        else:
            for name, rings in provinces:
                cls = "hl" if key == "cn" and name == "上海市" else "land"
                body.append(f'  <path class="{cls}" d="{p.path(rings)}"/>')
        body.append("</g>")

        body.append(f'<rect x="{p.x}" y="{p.y}" width="{p.w}" height="{p.h}" class="neat"/>')
        body.append(f'<text class="ptitle" x="{p.x}" y="{p.y - 11}">{title_en} · {title_cn}</text>')

        for pos, txt, kind in labels:
            if kind == "lon":
                body.append(f'<path class="tick" d="M{pos:.1f},{p.y + p.h} v4"/>')
                body.append(f'<text class="deg" x="{pos:.1f}" y="{p.y + p.h - 6}" text-anchor="middle">{txt}</text>')
            else:
                body.append(f'<path class="tick" d="M{p.x},{pos:.1f} h4"/>')
                body.append(f'<text class="deg" x="{p.x + 7}" y="{pos + 3:.1f}">{txt}</text>')

        meters, bar_px = p.scale_bar()
        bx, by = p.x + 14, p.y + p.h - 24
        body.append('<g class="scale">')
        body.append(f'  <path d="M{bx},{by} h{bar_px / 2:.1f} M{bx + bar_px / 2:.1f},{by} h{bar_px / 2:.1f}" stroke-width="3"/>')
        body.append(f'  <path d="M{bx},{by - 3} V{by + 3} M{bx + bar_px:.1f},{by - 3} V{by + 3}" stroke-width="1"/>')
        body.append(f'  <text x="{bx}" y="{by - 6}">0</text>')
        body.append(f'  <text x="{bx + bar_px:.1f}" y="{by - 6}" text-anchor="middle">{nice_label(meters)}</text>')
        rf = p.meters_per_px() / 0.0002646
        body.append(f'  <text class="rf" x="{bx + bar_px + 8:.1f}" y="{by + 1}">'
                    f'1:{(rf / 1e6):.1f}M</text>' if rf >= 1e6 else
                    f'  <text class="rf" x="{bx + bar_px + 8:.1f}" y="{by + 1}">1:{(rf / 1e3):.0f}k</text>')
        body.append("</g>")

    # Shanghai marker on panel A
    pa = panels["cn"]
    ax, ay = pa.px(121.4737, 31.2304)
    body.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="2.2" class="dot-hl"/>')
    body.append(f'<text class="city" x="{ax + 9:.1f}" y="{ay + 3:.1f}">上海 SH</text>')

    nx, ny = pa.x + pa.w - 20, pa.y + 24
    body.append(f'<g class="north" transform="translate({nx},{ny})">'
                f'<path d="M0,-9 L4.5,6 L0,2.4 L-4.5,6 Z"/><text y="19" text-anchor="middle">N</text></g>')

    # cities on panel B
    py = panels["yrd"]
    sx, sy = py.px(122.12, 30.18)
    body.append(f'<text class="sea" x="{sx:.1f}" y="{sy:.1f}" text-anchor="end">东海 ECS</text>')
    for name, lon, lat, hot, dx, dy, anchor in CITIES:
        x_, y_ = py.px(lon, lat)
        if hot:
            body.append(f'<circle cx="{x_:.1f}" cy="{y_:.1f}" r="4" class="dot-hl"/>')
            body.append(f'<circle cx="{x_:.1f}" cy="{y_:.1f}" r="4" class="pulse"/>')
            body.append(f'<text class="city-hl" x="{x_ + dx:.1f}" y="{y_ + dy:.1f}" text-anchor="{anchor}">{name}</text>')
        else:
            body.append(f'<circle cx="{x_:.1f}" cy="{y_:.1f}" r="2.4" class="dot"/>')
            body.append(f'<text class="city" x="{x_ + dx:.1f}" y="{y_ + dy:.1f}" text-anchor="{anchor}">{name}</text>')

    # campus on panel C
    ps = panels["sh"]
    cx, cy = ps.px(*CAMPUS)
    body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" class="dot-hl"/>')
    body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" class="pulse"/>')
    body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" class="ring"/>')
    body.append(f'<text class="city-hl" x="{cx + 9:.1f}" y="{cy - 7:.1f}">徐汇 Xuhui</text>')
    body.append(f'<text class="coord" x="{cx + 9:.1f}" y="{cy + 5:.1f}">31.1650°N · 121.4050°E</text>')

    # zoom callouts
    bboxes = {key: bbox for key, _x, _w, _en, _cn, bbox, _s, _l, _e in PANELS}
    for src, dst_key in (("cn", "yrd"), ("yrd", "sh")):
        sp, tp = panels[src], panels[dst_key]
        b = bboxes[dst_key]
        x0, y0 = sp.px(b[0], b[3])
        x1, y1 = sp.px(b[2], b[1])
        body.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" class="zoom-box"/>')
        body.append(f'<path d="M{x1:.1f},{y0:.1f} L{tp.x},{tp.y} M{x1:.1f},{y1:.1f} L{tp.x},{tp.y + tp.h}" class="zoom-link"/>')

    # legend
    ly = PANEL_Y + PANEL_H + 26
    items = [("swatch", "land", "省界 / 区界 · Boundary", 26),
             ("swatch", "hl", "研究区 · Study area", 240),
             ("dot", None, "城市 / 站点 · City / Site", 436),
             ("grid", None, "经纬网 · Graticule", 660)]
    body.append('<g class="legend">')
    for kind, cls, label, lx in items:
        if kind == "swatch":
            body.append(f'<rect x="{lx}" y="{ly - 9}" width="10" height="10" class="{cls}"/>')
        elif kind == "dot":
            body.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="3.6" class="dot-hl"/>')
        else:
            body.append(f'<path d="M{lx},{ly - 4} h11 M{lx + 5.5},{ly - 9} v10" class="tick"/>')
        body.append(f'<text x="{lx + 16}" y="{ly}">{label}</text>')
    body.append("</g>")

    body.append('<text class="fig" x="26" y="24">图 1｜研究区位置 · Figure 1 — Study area locator</text>')
    body.append(f'<text class="meta" x="{W - 26}" y="24" text-anchor="end">'
                'EPSG:4326 → Albers 25°N/47°N · λ₀=105°E</text>')
    body.append(f'<text class="meta" x="26" y="{H - 7}">'
                '数据 Data: DataV.GeoAtlas · 33 省级单元 / 16 区县 · 三幅图幅 Three sheets</text>')
    body.append(f'<text class="meta" x="{W - 26}" y="{H - 7}" text-anchor="end">'
                'zhangyx0803 · 31.1650°N 121.4050°E</text>')

    defs = "\n".join(
        f'    <clipPath id="clip-{theme}-{key}"><rect x="{p.x}" y="{p.y}" width="{p.w}" height="{p.h}"/></clipPath>'
        for key, p in panels.items()
    )
    panel_bg = "".join(
        f'<rect x="{p.x}" y="{p.y}" width="{p.w}" height="{p.h}" fill="{c["sea"]}"/>' for p in panels.values()
    )

    style = f"""
    .land {{ fill: {c["land"]}; stroke: {c["land_stroke"]}; stroke-width: .45; stroke-linejoin: round; }}
    .hl   {{ fill: {c["accent"]}; fill-opacity: .9; stroke: {c["accent_dark"]}; stroke-width: .7; stroke-linejoin: round; }}
    .grid {{ fill: none; stroke: {c["graticule"]}; stroke-width: .5; }}
    .neat {{ fill: none; stroke: {c["neat"]}; stroke-width: .9; }}
    .tick {{ stroke: {c["muted"]}; stroke-width: .8; fill: none; }}
    text  {{ fill: {c["text"]}; font: 10px/1 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .ptitle {{ font-size: 12px; font-weight: 600; letter-spacing: .03em; }}
    .deg  {{ font-size: 9px; fill: {c["muted"]}; }}
    .city {{ font-size: 9.4px; fill: {c["city"]}; paint-order: stroke; stroke: {c["halo"]}; stroke-width: 3px; }}
    .city-hl {{ font-size: 10px; font-weight: 700; fill: {c["accent_dark"]}; paint-order: stroke; stroke: {c["halo"]}; stroke-width: 3px; }}
    .coord {{ font-size: 8.6px; fill: {c["muted"]}; paint-order: stroke; stroke: {c["halo"]}; stroke-width: 3px; }}
    .dot {{ fill: {c["city"]}; stroke: {c["halo"]}; stroke-width: .8; }}
    .dot-hl {{ fill: {c["accent"]}; stroke: {c["halo"]}; stroke-width: 1; }}
    .pulse {{ fill: none; stroke: {c["accent"]}; stroke-width: 1.1;
             animation: pulse 2.8s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes pulse {{ 0% {{ r: 4; opacity: .8; }} 100% {{ r: 14; opacity: 0; }} }}
    .ring {{ fill: none; stroke: {c["accent"]}; stroke-width: .8; stroke-dasharray: 2 3; opacity: .75; }}
    .zoom-box {{ fill: none; stroke: {c["accent"]}; stroke-width: 1; stroke-dasharray: 3 2; }}
    .zoom-link {{ fill: none; stroke: {c["accent"]}; stroke-width: .9; stroke-dasharray: 2 3; opacity: .7; }}
    .scale path {{ stroke: {c["text"]}; fill: none; }}
    .scale text {{ font-size: 8.8px; fill: {c["muted"]}; }}
    .legend text {{ font-size: 9.6px; fill: {c["muted"]}; }}
    .north path {{ fill: {c["muted"]}; }}
    .north text {{ font-size: 8px; fill: {c["muted"]}; }}
    .fig {{ font-size: 13px; font-weight: 700; letter-spacing: .02em; }}
    .meta {{ font-size: 9.2px; fill: {c["muted"]}; }}
    .sea {{ font-size: 8.4px; fill: {c["muted"]}; letter-spacing: .16em; opacity: .85; }}
    .rf  {{ font-size: 8.2px; fill: {c["muted"]}; }}
    """

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
     aria-label="Figure 1: study area locator — China, Yangtze River Delta, Shanghai">
  <style>{style}</style>
  <defs>
{defs}
  </defs>
  <rect width="{W}" height="{H}" fill="{c["bg"]}"/>
  {panel_bg}
{chr(10).join(body)}
</svg>
'''
    path = os.path.join(OUT, f"geo-atlas-{theme}.svg")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print(f"wrote {path} ({os.path.getsize(path) / 1024:.1f} KB)")


if __name__ == "__main__":
    for t in ("light", "dark"):
        build_theme(t)
    sys.exit(0)
