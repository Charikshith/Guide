# Guide

A mastery roadmap — from computer science foundations to AI systems engineering — organized as six volumes and delivered as 135 single-concept chapters.

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

## HTML view

Each volume folder holds an `index.md` (the contents) and one file per chapter. To browse them as a site with rendered diagrams, sidebar navigation, and checklist tracking:

```bash
python tools/build_site.py   # writes site/ (git-ignored)
```

Then open `site/index.html` in a browser.
