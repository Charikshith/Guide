# Guide

A mastery roadmap — from computer science foundations to AI systems engineering — organized as six volumes and delivered as 142 single-concept chapters.

Start at **[roadmap.md](roadmap.md)** for the index, prerequisite ordering, and per-volume exit criteria.

## Volumes

| # | Volume |
|---|--------|
| 0 | [Math & Mental Models](volumes/volume-0-math/index.md) |
| 1 | [Computer Science Foundations](volumes/volume-1-cs-foundations/index.md) |
| 2 | [Software Engineering](volumes/volume-2-software-engineering/index.md) |
| 3 | [Low-Level Design](volumes/volume-3-low-level-design/index.md) |
| 4 | [High-Level Design](volumes/volume-4-high-level-design/index.md) |
| 5 | [AI Systems Engineering](volumes/volume-5-ai-systems/index.md) |

## Reading it in the browser

Open **`index.html`** in a browser. Every volume and chapter has its own page, in the same theme as the AI Library: a sidebar with the chapter's sections and the volume's chapters, light and dark mode, zoomable diagrams, collapsible solutions, and a progress tracker (checklists and "mark chapter complete" are saved in your browser).

The Markdown files are the source of truth. After editing any of them, regenerate the pages:

```bash
python tools/build_pages.py   # rewrites index.html, roadmap.html and the .html next to each .md
```

The look lives in `assets/` (`system-design.css`, `home.css` and `system-design.js` are the AI Library theme; `guide.css` and `guide.js` hold the Guide-only parts). Pages load the Markdown renderer, diagram library and code highlighter from a CDN, so they need an internet connection.

**Online preview:** GitHub shows `.html` files as source code, so these links render the pages through [htmlpreview.github.io](https://htmlpreview.github.io/):

| # | Volume |
|---|--------|
| 0 | [Math & Mental Models](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-0-math/index.html) |
| 1 | [Computer Science Foundations](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-1-cs-foundations/index.html) |
| 2 | [Software Engineering](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-2-software-engineering/index.html) |
| 3 | [Low-Level Design](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-3-low-level-design/index.html) |
| 4 | [High-Level Design](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-4-high-level-design/index.html) |
| 5 | [AI Systems Engineering](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-5-ai-systems/index.html) |

[Open the home page online](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/index.html)

> The older generated site in `site/` (and `tools/build_site.py`) is no longer updated; the pages above replace it. The handwritten-notes pages (`*.notes.html`) have been removed.
