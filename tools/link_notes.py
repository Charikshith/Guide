"""Fill prev/next/contents links in the handwritten chapter notes and write a
notes contents page per volume (volumes/<vol>/index.notes.html).

Usage:  python tools/link_notes.py     (safe to re-run)
"""
import html
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "volumes"
TEMPLATE = Path(__file__).resolve().parent.parent / ".claude/skills/handwritten/assets/template.html"
NAV = "<!--NAV-->"
BLOCK = re.compile(r'<nav class="nav">.*?</nav>|<!--NAV-->', re.S)


def title_of(page):
    m = re.search(r"<h1>(.*?)</h1>", page.read_text(encoding="utf-8"), re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else page.stem


for vol in sorted(p for p in SRC.iterdir() if p.is_dir()):
    pages = sorted(vol.glob("ch*.notes.html"))
    if not pages:
        continue
    titles = [title_of(p) for p in pages]
    for i, p in enumerate(pages):
        prev = f'<a href="{pages[i-1].name}">← {html.escape(titles[i-1])}</a>' if i else "<span></span>"
        nxt = f'<a href="{pages[i+1].name}">{html.escape(titles[i+1])} →</a>' if i + 1 < len(pages) else "<span></span>"
        nav = f'<nav class="nav">{prev}<a href="index.notes.html">☰ Contents</a>{nxt}</nav>'
        text = p.read_text(encoding="utf-8")
        parts = BLOCK.split(text)
        assert len(parts) == 3, (p, len(parts))
        p.write_text(parts[0] + nav + parts[1] + nav + parts[2], encoding="utf-8")
    def item(p, t):
        return f'<li class="arrow"><a href="{p.name}">{html.escape(t)}</a></li>'

    # Group by the "## Part N — Title" headings in the volume's index.md (volumes without Parts stay flat).
    part_of, part = {}, None
    for line in (vol / "index.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (Part \d+ — .+)", line)
        if m:
            part = m.group(1).strip()
            continue
        m = re.match(r"^#{2,3} Chapter (\d+) — ", line)
        if m and part:
            part_of[int(m.group(1))] = part
    if part_of:
        groups = []
        for p, t in zip(pages, titles):
            name = part_of.get(int(re.match(r"ch(\d+)-", p.name).group(1)))
            if not groups or groups[-1][0] != name:
                groups.append((name, []))
            groups[-1][1].append(item(p, t))
        content = "\n".join((f"<h2>{html.escape(n)}</h2>\n" if n else "") + "<ul>\n" + "\n".join(li) + "\n</ul>" for n, li in groups)
    else:
        content = "<ul>\n" + "\n".join(item(p, t) for p, t in zip(pages, titles)) + "\n</ul>"
    idx = TEMPLATE.read_text(encoding="utf-8")
    vtitle = vol.name.replace("-", " ").title()
    idx = idx.replace("{{TITLE}}", f"{vtitle} — Contents").replace("{{DATE}}", "2026-10-10")
    idx = idx.replace("<!-- CONTENT GOES HERE -->", content)
    (vol / "index.notes.html").write_text(idx, encoding="utf-8")
print("done")
