"""Re-wrap every *.notes.html page in the current handwritten skill template.

The chapter content (everything from <main class="page"> to </main>) is kept
byte-for-byte. Only the shell changes: head/CSS, SVG defs, and the sketch script.
A small block of extra CSS (h3, nav, code, pagebreak ...) is added after the
skill's CSS, because the chapter pages use classes the skill template lacks.

Usage:  python tools/apply_handwritten_template.py     (safe to re-run)
"""
import glob
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / ".claude/skills/handwritten/assets/template.html"
EXTRA_MARK = "/* ===== Extras for long chapter notes */"
EXTRA_CSS = EXTRA_MARK + """
pre.code.ascii{border-color:var(--green)}
code{font-family:Consolas,'Courier New',monospace;font-size:.82em;background:rgba(0,0,0,.06);padding:0 3px;border-radius:3px}
pre.code code{background:none;padding:0;font-size:inherit}
.lang{font-family:var(--title);font-size:18px;color:var(--red)}
h3{font-family:var(--title);font-weight:700;color:var(--ink2);font-size:26px;line-height:var(--line);margin:calc(var(--line)*.5) 0 0}
h3::before{content:"✎ ";font-size:18px;color:var(--red)}
.nav{display:flex;justify-content:space-between;gap:12px;font-family:var(--title);font-size:22px;line-height:var(--line)}
.nav a{color:var(--red);text-decoration:none}
.nav a:hover{text-decoration:underline wavy}
.pagebreak{border-top:3px dashed var(--margin);margin:var(--line) 0;text-align:center;font-family:var(--title);color:var(--red);line-height:var(--line)}
li.todo::before{content:"☐";color:var(--ink2)}
a{color:var(--ink);text-decoration:underline dotted}
"""
MAIN = re.compile(r'<main class="page">.*?</main>', re.S)


def wrap(title_text, main_block):
    t = TEMPLATE.read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = t.replace("{{TITLE}}", title_text)          # <title> only; <h1> sits inside main_block
    return MAIN.sub(lambda m: main_block, t, count=1)


def main():
    done = skipped = 0
    for f in sorted(glob.glob(str(ROOT / "volumes/*/*.notes.html"))):
        p = Path(f)
        text = p.read_text(encoding="utf-8")
        if EXTRA_MARK in text and "Sketch: redraw every .sk shape" in text:
            skipped += 1
            continue
        m = re.search(r"<title>(.*?) [—-] Notes</title>", text, re.S)
        title = m.group(1) if m else html.escape(p.stem)
        block = MAIN.search(text).group(0)
        p.write_text(wrap(title, block), encoding="utf-8")
        done += 1
    print(f"rewrapped {done}, already current {skipped}")


if __name__ == "__main__":
    main()
