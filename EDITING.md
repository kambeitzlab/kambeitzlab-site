# Editing the website

All content is plain text in this repository. Commit a change to `main` (on github.com or locally) and the site rebuilds and goes live in about two minutes (see the **Actions** tab). If a build fails, the old version stays online and the Actions log names the file and field that is wrong.

**Editing on github.com:** open the folder, click **Add file → Create new file** (or the pencil icon on an existing file), paste a template, then **Commit changes**. To upload a photo, open the image folder and use **Add file → Upload files**.

**Editing locally:** `npm install` once, then `npm run dev` and open http://localhost:4321. Changes appear instantly.

| What | Where |
|---|---|
| News posts | `src/content/news/` |
| Team members | `src/content/team/` |
| Alumni | `src/content/alumni/` |
| Projects | `src/content/projects/` |
| Publications | `content/publications.bib` |
| Images | `src/assets/news/`, `src/assets/team/`, `src/assets/projects/` |
| Open positions | `positions` list at the top of `src/pages/join.astro` |
| Code repositories | `src/data/code.ts` |
| Contact email, GitHub, ORCID, partner logos | `src/data/site.ts` |
| Impressum / Datenschutz | `src/pages/impressum.md`, `src/pages/datenschutz.md` |

Good to know:
- Text between `---` lines is "frontmatter": `key: value`, one per line. Put values containing a colon in quotes: `title: "Paper: a new model"`.
- Images: upload JPG or PNG (max. ~2000 px wide is plenty). The site creates small, fast AVIF/WebP versions automatically. Reference them relative to the Markdown file: `../../assets/news/my-photo.jpg`.
- `<!-- comments -->` in Markdown files are **visible in the public page source**. Don't put private notes there.

---

## Add a news post

Create `src/content/news/2026-11-20-short-title.md`. The file name becomes the URL, so use lowercase letters, numbers and hyphens only.

```markdown
---
title: New paper in Nature Mental Health
date: 2026-11-20
type: paper            # paper | award | people | event | media
image: ../../assets/news/2026-11-20-nature-mh.jpg   # optional
image_alt: Figure 1 of the paper showing …            # describe the image; leave '' if purely decorative
excerpt: One sentence shown in the news list.
gallery: []            # optional extra photos: [../../assets/news/a.jpg, ../../assets/news/b.jpg]
---

Two or three short paragraphs. Link the paper:
[Read the paper](https://doi.org/10.xxxx/xxxxx)
```

The home page always shows the three newest posts. The news list shows 10 per page.

## Add a team member

1. Upload a square-ish photo to `src/assets/team/firstname-lastname.jpg`.
2. Create `src/content/team/firstname-lastname.md` (no umlauts in file names: ö → oe):

```markdown
---
name: Firstname Lastname
title: MSc.            # Prof. | PD Dr. | Dr. | MSc. | cand. med. | '' (shown before the role)
role: phd              # lead | senior | postdoc | phd | student
position: PhD student  # text shown on the card
order: 4               # sorting within the group (smaller = earlier)
photo: ../../assets/team/firstname-lastname.jpg
photo_focus: 50% 30%   # optional: which part of the photo stays visible in the square crop
show_photo: true       # false hides the photo (initials are shown instead)
email: ''
orcid: ''              # full URL, e.g. https://orcid.org/0000-0000-0000-0000
---

Short bio in the first person or third person, 80–150 words.
```

Groups on the team page: `lead` → Lab leads, `senior` and `postdoc` → Senior researchers & postdocs, `phd` → PhD students, `student` → MSc & MD students.

**When someone leaves:** move their file from `src/content/team/` to `src/content/alumni/` and reduce the frontmatter to:

```markdown
---
name: Firstname Lastname
degree: Dr.            # degree they hold / earned here
photo: ../../assets/team/firstname-lastname.jpg   # kept, but not shown
---

(old bio can stay here; it is not displayed)
```

## Add a publication

Paste the BibTeX entry (e.g. exported from Zotero, PubMed or Google Scholar) into `content/publications.bib` and add the site's extra fields:

```bibtex
@article{lastname2026keyword,
  author   = {Lastname, A. and Kambeitz, J.},
  title    = {Title of the paper},
  journal  = {Journal Name},
  volume   = {12},
  pages    = {1--10},
  year     = {2026},
  doi      = {10.xxxx/xxxxx},
  theme    = {prediction},          % prediction | language-digital | modeling | interventions (comma-separate several)
  keywords = {selected},            % optional: shown on the home page and under "Selected only"
  pdf      = {https://…},           % optional badges
  preprint = {https://…},
  code     = {https://github.com/…},
  data     = {https://…},
}
```

To replace the whole list from a new reference-manager export in Vancouver style (one reference per paragraph, like `publications.txt`), run `python3 scripts/txt2bib.py publications.txt --doi`. It keeps existing `theme`/`selected` tags and looks up missing DOIs.

Lab members (everyone in `team/` and `alumni/`) are highlighted automatically, matched by last name and first initial. The home page shows the three newest entries with `keywords = {selected}`. If an entry has a syntax error, the build log shows a `[publications.bib]` warning.

## Add a project

1. Upload an image to `src/assets/projects/my-project.png`.
2. Create `src/content/projects/my-project.md`:

```markdown
---
title: Short project title
full_title: ''         # optional long/official title, shown on the project page
theme: prediction      # prediction | language-digital | modeling | interventions
status: active         # active | completed | '' (no badge)
years: 2025–2028
funder: DFG
partners: [University of Bonn, King's College London]
url: https://project-website.org/   # optional
image: ../../assets/projects/my-project.png
image_alt: Logo of the … project
image_fit: contain     # contain = logos/figures (shown whole), cover = photos (fill the frame)
summary: One or two sentences, at most 40 words, shown on the project card.
order: 13              # position within the research page
---

Full project description (Markdown).
```

The project appears on the Research page, its theme page, and in the project count on the home page.

## Other quick edits

- **Open position:** add an entry to `positions` at the top of `src/pages/join.astro`, e.g.
  `{ title: 'PhD position: language models in psychosis', text: 'Fully funded, 3 years, start 2027.', href: 'https://…/ad.pdf', deadline: '2026-12-15' }`.
  Remove it again when the position is filled.
- **Hide a team photo:** set `show_photo: false`.
- **Partner logos:** put monochrome SVG/PNG files in `public/partners/` and list them in `src/data/site.ts`:
  `{ name: 'DFG', logo: '/partners/dfg.svg', url: 'https://www.dfg.de' }`. The strip appears on the home page automatically.
