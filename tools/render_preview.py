# -*- coding: utf-8 -*-
"""Render README.md to a GitHub-like HTML page for visual QA.

Uses cmark-gfm (the same markdown engine GitHub uses) plus GitHub's own
sanitizer-ish behaviour: raw HTML is kept, mermaid fences are rendered by
the browser from CDN.
"""
import html
import os
import re
import sys

import cmarkgfm
from cmarkgfm.cmark import Options as CmarkOptions

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "README.md")
OUT = os.path.join(ROOT, "preview-readme.html")

CSS = """
* { box-sizing: border-box; }
body { margin:0; background:#fff; color:#1f2328;
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", Helvetica, Arial, sans-serif; }
.markdown-body { max-width: 1012px; margin: 0 auto; padding: 40px 32px 80px; }
h1, h2, h3 { font-weight: 600; line-height: 1.25; }
h1 { font-size: 2em; border-bottom: 1px solid #d1d9e0; padding-bottom: .3em; margin: .67em 0 .5em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #d1d9e0; padding-bottom: .3em; margin-top: 40px; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { height: 1px; background: #d1d9e0; border: 0; margin: 32px 0; }
img { max-width: 100%; vertical-align: middle; }
table { border-collapse: collapse; margin: 16px 0; font-size: 14px; display: inline-block; }
th, td { border: 1px solid #d1d9e0; padding: 8px 12px; text-align: left; }
th { background: #f6f8fa; font-weight: 600; }
tr:nth-child(2n) td { background: #fbfcfd; }
code { background: hsla(210,18%,87%,1); padding: .2em .4em; border-radius: 6px; font-size: 85%;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
pre { background: #f6f8fa; padding: 16px; border-radius: 8px; overflow: auto; }
pre code { background: none; padding: 0; }
details { margin: 12px 0; border: 1px solid #d1d9e0; border-radius: 8px; padding: 10px 16px; background: #fbfcfd; }
summary { cursor: pointer; font-weight: 600; }
sub { color: #59636e; font-size: 12px; }
blockquote { margin: 0 0 16px; padding: 0 1em; color: #59636e; border-left: .25em solid #d1d9e0; }
"""


def main():
    with open(SRC, "r", encoding="utf-8") as fh:
        text = fh.read()

    blocks = []

    def stash(match):
        blocks.append(match.group(1).strip())
        return f"MERMAIDBLOCK{len(blocks) - 1}END"

    text = re.sub(r"```mermaid\n(.*?)```", stash, text, flags=re.S)
    text = text.replace("<details>", "<details open>")  # QA only: see inside every accordion

    options = (
        CmarkOptions.CMARK_OPT_UNSAFE
        | CmarkOptions.CMARK_OPT_TABLE_PREFER_STYLE_ATTRIBUTES
    )
    rendered = cmarkgfm.markdown_to_html_with_extensions(
        text, options=options, extensions=["table", "strikethrough", "autolink", "tagfilter"]
    )

    for index, block in enumerate(blocks):
        rendered = rendered.replace(
            f"<p>MERMAIDBLOCK{index}END</p>",
            f'<pre class="mermaid">{html.escape(block)}</pre>',
        )
        rendered = rendered.replace(
            f"MERMAIDBLOCK{index}END", f'<pre class="mermaid">{html.escape(block)}</pre>'
        )

    page = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>README preview (cmark-gfm)</title>
<style>{CSS}</style></head>
<body><div class="markdown-body">{rendered}</div>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({{ startOnLoad: true, theme: "neutral", flowchart: {{ htmlLabels: true }} }});
</script>
</body></html>
"""
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    print(f"wrote {OUT} ({len(page)} chars, {len(blocks)} mermaid blocks)")


if __name__ == "__main__":
    sys.exit(main())
