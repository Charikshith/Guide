# Guide

A mastery roadmap — from computer science foundations to AI systems engineering — organized as six volumes and delivered as 139 single-concept chapters.

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

**HTML preview:** [open the site home page online](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/site/index.html). The built site is committed in `site/`. For the full experience, clone the repo and open `site/index.html` locally. The online previewer may not load the map or the chapter text.

Each chapter also has a handwritten-notes page (`*.notes.html`). Open `volumes/<volume>/index.notes.html` for a volume's contents. To re-apply the skill template after it changes, run `python tools/apply_handwritten_template.py`.

### Online preview (handwritten notes)

GitHub shows `.html` files as source code, not as a page. These links render the committed notes pages through [htmlpreview.github.io](https://htmlpreview.github.io/):

| # | Volume notes |
|---|--------------|
| 0 | [Math & Mental Models](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-0-math/index.notes.html) |
| 1 | [Computer Science Foundations](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-1-cs-foundations/index.notes.html) |
| 2 | [Software Engineering](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-2-software-engineering/index.notes.html) |
| 3 | [Low-Level Design](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-3-low-level-design/index.notes.html) |
| 4 | [High-Level Design](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-4-high-level-design/index.notes.html) |
| 5 | [AI Systems Engineering](https://htmlpreview.github.io/?https://github.com/Charikshith/Guide/blob/main/volumes/volume-5-ai-systems/index.notes.html) |
