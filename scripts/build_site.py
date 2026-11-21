#!/usr/bin/env python3
"""Build the public MCP docs site in site/.

site/mcp.md is the one hand-written source. This script renders it to
site/index.html, with the tool reference shown as collapsible tables.

The tool reference comes from site/tools.json, which is generated from
FULL_MCP_TOOL_EFFECTS in freckle-io/next
(apps/http_api/src/FullMcp/Annotations.ts): every tool the server exposes, its
title and what a write costs. Pass that file to refresh tools.json and the
tool tables in mcp.md:

  git -C ../next fetch origin dev
  git -C ../next show origin/dev:apps/http_api/src/FullMcp/Annotations.ts > /tmp/Annotations.ts
  python3 scripts/build_site.py --annotations /tmp/Annotations.ts

Without --annotations it only re-renders index.html. --check exits 1 if
index.html is stale instead of writing it (CI runs this).
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MD = SITE / "mcp.md"
TOOLS = SITE / "tools.json"
OUT = SITE / "index.html"
START, END = "<!-- tools:start -->", "<!-- tools:end -->"

GROUPS = [
    ("workspace", "Workspace and connections", ("workspace", "connections", "integrationCredentials", "snapshot")),
    ("credits", "Credits", ("creditUsage",)),
    ("workbooks", "Workbooks", ("workbooks",)),
    ("datasets", "Datasets", ("datasets",)),
    ("lists", "List building", ("listBuilds",)),
    ("workflows", "Workflows and enrichment", ("workflowDrafts", "workflowNodes", "workflows")),
    ("runs", "Workflow runs", ("workflowRuns",)),
    (
        "imports",
        "CRM and warehouse imports",
        ("hubspotDatasetSources", "salesforceDatasetSources", "attioDatasetSources", "snowflakeDatasetSources"),
    ),
    ("signals", "Signals", ("signals",)),
    ("ads", "Ads audiences", ("adAudienceSyncs",)),
]

COST_LABEL = {
    "": "Read only",
    "free": "Free write",
    "freeStart": "Starts work, free",
    "later": "Enables later spend",
    "spend": "May spend credits",
}

ENTRY = re.compile(r"(\w+):\s*(read|write)\(\s*'([^']+)'(?:,\s*(?:hints\([^)]*\)|[A-Z_]+),\s*'(\w+)')?\s*\)")


# --- tools -------------------------------------------------------------------


def parse_annotations(source: str) -> list[dict]:
    body = re.sub(r"//[^\n]*", "", source[source.index("FULL_MCP_TOOL_EFFECTS") :])
    tools = [{"name": n, "title": t, "cost": c} for n, _k, t, c in ENTRY.findall(body)]
    if len(tools) < 50:
        sys.exit(f"parsed only {len(tools)} tools; has Annotations.ts changed shape?")
    return tools


def group_tools(tools: list[dict]) -> list[tuple[str, str, list[dict]]]:
    out, seen = [], set()
    for key, label, prefixes in GROUPS:
        rows = [t for t in tools if t["name"].split("_")[0] in prefixes]
        seen.update(t["name"] for t in rows)
        if rows:
            out.append((key, label, rows))
    missing = [t["name"] for t in tools if t["name"] not in seen]
    if missing:
        sys.exit(f"tools with no group in GROUPS: {missing}")
    return out


def tools_md(groups, total: int) -> str:
    parts = [f"{total} tools, generated from the server's tool annotations.", ""]
    for _key, label, rows in groups:
        parts += [f"### {label}", "", "| Tool | What it does | Effect |", "| --- | --- | --- |"]
        parts += [f"| `{t['name']}` | {t['title']} | {COST_LABEL[t['cost']]} |" for t in rows]
        parts.append("")
    return "\n".join(parts).rstrip()


def tools_html(groups, total: int) -> str:
    parts = [f'<p class="muted">{total} tools, generated from the server\'s tool annotations.</p>']
    for key, label, rows in groups:
        parts.append(
            f'<details id="tools-{key}"><summary>{html.escape(label)} <span class="count">{len(rows)}</span></summary>'
        )
        parts.append("<table><thead><tr><th>Tool</th><th>What it does</th><th>Effect</th></tr></thead><tbody>")
        for t in rows:
            badge = "read" if not t["cost"] else ("spend" if t["cost"] == "spend" else "write")
            parts.append(
                f"<tr><td><code>{html.escape(t['name'])}</code></td><td>{html.escape(t['title'])}</td>"
                f'<td><span class="badge {badge}">{COST_LABEL[t["cost"]]}</span></td></tr>'
            )
        parts.append("</tbody></table></details>")
    return "\n".join(parts)


# --- markdown ------------------------------------------------------------------
# A small renderer for the subset mcp.md uses: headings, paragraphs, lists,
# fenced code, bold, italics, inline code and links.


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def inline(text: str) -> str:
    codes: list[str] = []

    def stash(m):
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\0{len(codes) - 1}\0"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(.+?)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>',
        text,
    )
    text = re.sub(r"\b([\w.+-]+@freckle\.io)\b", r'<a href="mailto:\1">\1</a>', text)
    return re.sub(r"\0(\d+)\0", lambda m: codes[int(m.group(1))], text)


def render(md: str, tools_block: str) -> tuple[str, str, list[tuple[str, str]]]:
    lines = md.splitlines()
    out: list[str] = []
    toc: list[tuple[str, str]] = []
    title = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == START:
            while lines[i].strip() != END:
                i += 1
            out.append(tools_block)
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            i += 1
            code = []
            while not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{lang}"' if lang else ""
            out.append(
                f'<div class="code"><button class="copy" type="button">Copy</button>'
                f"<pre><code{cls}>{html.escape(chr(10).join(code))}</code></pre></div>"
            )
            continue
        m = re.match(r"(#{1,3}) (.*)", line)
        if m:
            level, text = len(m.group(1)), m.group(2)
            if level == 1:
                title = text
                out.append(f"<h1>{inline(text)}</h1>")
            else:
                sid = slug(text)
                if level == 2:
                    toc.append((sid, text))
                out.append(f'<h{level} id="{sid}">{inline(text)}<a class="anchor" href="#{sid}">#</a></h{level}>')
            i += 1
            continue
        if re.match(r"(- |\d+\. )", line):
            ordered = not line.startswith("- ")
            items: list[str] = []
            while i < len(lines) and lines[i].strip():
                if re.match(r"(- |\d+\. )", lines[i]):
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if not line.strip():
            i += 1
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#|```|- |\d+\. |<!--)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return title, "\n".join(out), toc


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Docs</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="freckle.png">
<link rel="icon" href="freckle.png">
<link rel="alternate" type="text/markdown" href="mcp.md">
<style>
:root {{ --fg:#16161a; --muted:#62626e; --bg:#fff; --soft:#f5f5f7; --line:#e4e4e9; --accent:#4b3df5;
  --read:#e7f6ec; --read-fg:#17663a; --write:#eef0ff; --write-fg:#3a33b8; --spend:#fff3e0; --spend-fg:#8a4b00; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fg:#ececf1; --muted:#a0a0ad; --bg:#111114; --soft:#1b1b20;
  --line:#2c2c34; --accent:#9d95ff; --read:#12301e; --read-fg:#7ad79c; --write:#1e1f3d; --write-fg:#aaa4ff;
  --spend:#33240e; --spend-fg:#f0b465; }} }}
* {{ box-sizing:border-box }}
body {{ margin:0; font:16px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; color:var(--fg); background:var(--bg) }}
a {{ color:var(--accent) }}
header.top {{ border-bottom:1px solid var(--line); padding:14px 24px; display:flex; align-items:center; gap:12px }}
header.top img {{ height:28px; width:28px; border-radius:6px }}
header.top .spacer {{ flex:1 }}
header.top a {{ text-decoration:none; color:var(--muted); font-size:14px }}
.layout {{ display:grid; grid-template-columns:220px minmax(0,760px); gap:48px; max-width:1080px; margin:0 auto; padding:32px 24px 80px }}
nav.toc {{ position:sticky; top:24px; align-self:start; font-size:14px }}
nav.toc a {{ display:block; color:var(--muted); text-decoration:none; padding:3px 0 }}
nav.toc a:hover {{ color:var(--fg) }}
@media (max-width:860px) {{ .layout {{ grid-template-columns:1fr }} nav.toc {{ position:static }} }}
h1 {{ font-size:2.1rem; line-height:1.2; margin:0 0 12px }}
h2 {{ margin-top:48px; padding-top:8px; border-top:1px solid var(--line) }}
h3 {{ margin-top:28px }}
.anchor {{ margin-left:8px; color:var(--line); text-decoration:none; font-weight:400 }}
h2:hover .anchor, h3:hover .anchor {{ color:var(--muted) }}
code {{ font:0.88em ui-monospace,SFMono-Regular,Menlo,monospace; background:var(--soft); padding:1px 5px; border-radius:4px }}
.code {{ position:relative }}
pre {{ background:var(--soft); border:1px solid var(--line); border-radius:8px; padding:14px 16px; overflow:auto }}
pre code {{ background:none; padding:0 }}
.copy {{ position:absolute; top:8px; right:8px; font-size:12px; border:1px solid var(--line); background:var(--bg); color:var(--muted); border-radius:6px; padding:2px 8px; cursor:pointer }}
.muted {{ color:var(--muted) }}
details {{ border:1px solid var(--line); border-radius:8px; margin:10px 0; padding:0 14px }}
summary {{ cursor:pointer; padding:10px 0; font-weight:600 }}
.count {{ color:var(--muted); font-weight:400; margin-left:6px }}
table {{ width:100%; border-collapse:collapse; font-size:14px; margin-bottom:12px }}
th, td {{ text-align:left; padding:6px 8px; border-top:1px solid var(--line); vertical-align:top }}
th {{ color:var(--muted); font-weight:500 }}
td code {{ word-break:break-all }}
.badge {{ font-size:12px; padding:1px 8px; border-radius:999px; white-space:nowrap }}
.badge.read {{ background:var(--read); color:var(--read-fg) }}
.badge.write {{ background:var(--write); color:var(--write-fg) }}
.badge.spend {{ background:var(--spend); color:var(--spend-fg) }}
footer {{ border-top:1px solid var(--line); padding:20px 24px; text-align:center; color:var(--muted); font-size:14px }}
</style>
</head>
<body>
<header class="top">
  <a href="https://freckle.io"><img src="freckle.png" alt="Freckle"></a>
  <strong>Freckle Docs</strong>
  <span class="spacer"></span>
  <a href="mcp.md">Markdown</a>
  <a href="llms.txt">llms.txt</a>
  <a href="https://github.com/freckle-io/agent-plugins-mcp">GitHub</a>
  <a href="https://freckle.io">freckle.io</a>
</header>
<div class="layout">
<nav class="toc">{toc}</nav>
<main>
{body}
</main>
</div>
<footer>
  <a href="https://freckle.io">Freckle</a> ·
  <a href="https://freckle.io/privacy-policy">Privacy policy</a> ·
  <a href="https://freckle.io/terms-of-service">Terms of service</a> ·
  <a href="mailto:support@freckle.io">support@freckle.io</a>
</footer>
<script>
document.querySelectorAll('.copy').forEach(b => b.addEventListener('click', () => {{
  navigator.clipboard.writeText(b.nextElementSibling.innerText).then(() => {{
    b.textContent = 'Copied'; setTimeout(() => (b.textContent = 'Copy'), 1500)
  }})
}}))
if (location.hash.startsWith('#tools-')) document.querySelector(location.hash)?.setAttribute('open', '')
</script>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--annotations", type=Path, help="Annotations.ts from freckle-io/next")
    ap.add_argument("--check", action="store_true", help="fail if index.html is stale; write nothing")
    args = ap.parse_args()

    md = MD.read_text()
    if args.annotations:
        tools = parse_annotations(args.annotations.read_text())
        TOOLS.write_text(json.dumps(tools, indent=2) + "\n")
        block = tools_md(group_tools(tools), len(tools))
        md = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _m: f"{START}\n{block}\n{END}", md, flags=re.S)
        MD.write_text(md)
    tools = json.loads(TOOLS.read_text())

    title, body, toc = render(md, tools_html(group_tools(tools), len(tools)))
    first_para = re.search(r"<p>(.*?)</p>", body, re.S).group(1)
    description = html.escape(re.sub(r"<[^>]+>", "", first_para), quote=True)
    page = PAGE.format(
        title=html.escape(title),
        description=description,
        toc="\n".join(f'<a href="#{sid}">{html.escape(text)}</a>' for sid, text in toc),
        body=body,
    )
    if args.check:
        if not OUT.exists() or OUT.read_text() != page:
            sys.exit("site/index.html is stale: run python3 scripts/build_site.py")
        print("site/index.html is up to date")
        return
    OUT.write_text(page)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(tools)} tools)")


if __name__ == "__main__":
    main()
