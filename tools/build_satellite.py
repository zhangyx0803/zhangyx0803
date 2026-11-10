# -*- coding: utf-8 -*-
"""Generate the satellite-uplink panel as a standalone animated SVG.

The original profile README used inline <svg>, which GitHub's sanitizer strips.
Shipping it as a file lets the <animate> elements actually run.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets")

W, H = 720, 190
LAT, LON = "31.1650", "121.4050"

THEMES = {
    "light": dict(
        bg="#ffffff", panel="#f6f8fa", border="#d1d9e0", grid="#e4eaf0",
        text="#59636e", accent="#3ba55d", dim="#8b949e",
    ),
    "dark": dict(
        bg="#0d1117", panel="#11161d", border="#28323c", grid="#1b232c",
        text="#8b949e", accent="#3ba55d", dim="#6e7681",
    ),
}


def build(theme, c):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Satellite link panel: {LAT}N {LON}E, Xuhui, Shanghai">
  <defs>
    <pattern id="g-{theme}" width="18" height="18" patternUnits="userSpaceOnUse">
      <path d="M18 0 H0 V18" fill="none" stroke="{c["grid"]}" stroke-width="1"/>
    </pattern>
  </defs>

  <rect width="{W}" height="{H}" rx="10" fill="{c["panel"]}" stroke="{c["border"]}"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{c["border"]}"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="url(#g-{theme})" opacity="0.55"/>

  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
    <text x="18" y="26" font-size="10.5" letter-spacing="1.6" fill="{c["dim"]}">SAT-LINK / TELEMETRY</text>
    <text x="18" y="56" font-size="13" fill="{c["text"]}">LAT <tspan fill="{c["accent"]}">{LAT}</tspan>° N</text>
    <text x="18" y="78" font-size="13" fill="{c["text"]}">LON <tspan fill="{c["accent"]}">{LON}</tspan>° E</text>
    <text x="18" y="104" font-size="12" fill="{c["text"]}">TARGET <tspan fill="{c["accent"]}">XUHUI · SHANGHAI</tspan></text>
    <text x="18" y="126" font-size="11" fill="{c["dim"]}">STATUS <tspan fill="{c["accent"]}">Crunching spatial data…</tspan></text>
    <text x="18" y="152" font-size="10" fill="{c["dim"]}">EPSG:4326 · WGS 84 · ALT 4 m</text>
  </g>

  <g stroke="{c["accent"]}" fill="none" stroke-linecap="round">
    <path d="M300,104 L312,100 L324,106 L336,96 L348,108 L360,99 L372,105 L384,95 L396,107 L408,101 L420,104"
          stroke-width="1.4" opacity="0.75">
      <animate attributeName="opacity" values="0.75;0.3;0.75" dur="3.2s" repeatCount="indefinite"/>
    </path>
    <path d="M300,116 L420,116" stroke-width="1" stroke-dasharray="2 4" opacity="0.35"/>
    <text x="300" y="134" font-family="ui-monospace, monospace" font-size="9.5" fill="{c["dim"]}" stroke="none">SIGNAL · 1.696 GHz · LOCKED</text>
  </g>

  <g transform="translate(560,95)">
    <circle r="46" fill="none" stroke="{c["border"]}" stroke-dasharray="2 5"/>
    <circle r="30" fill="none" stroke="{c["grid"]}" stroke-width="6"/>
    <circle r="30" fill="none" stroke="{c["accent"]}" stroke-width="1.4" stroke-dasharray="3 7">
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/>
    </circle>

    <circle r="8" fill="none" stroke="{c["accent"]}" stroke-width="2">
      <animate attributeName="r" values="8;44" dur="2.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.9;0" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle r="8" fill="none" stroke="{c["accent"]}" stroke-width="2">
      <animate attributeName="r" values="8;44" dur="2.4s" begin="1.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.9;0" dur="2.4s" begin="1.2s" repeatCount="indefinite"/>
    </circle>

    <circle r="5" fill="{c["accent"]}"/>
    <circle r="5" fill="{c["accent"]}" opacity="0.45">
      <animate attributeName="opacity" values="0.45;0.1;0.45" dur="2.4s" repeatCount="indefinite"/>
    </circle>

    <path d="M-62,58 L-14,14" stroke="{c["accent"]}" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  </g>
</svg>
'''


def main():
    for theme, colors in THEMES.items():
        path = os.path.join(OUT, f"satellite-{theme}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(build(theme, colors))
        print(f"wrote {path} ({os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    sys.exit(main())
