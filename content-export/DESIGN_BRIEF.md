# Design brief: kambeitzlab.com rebuild

Read this together with README.md before building. Where this brief and README.md disagree, this brief wins.

## Goal

Replace the Wix site with a fast, modern, low-maintenance static site (Astro). It should communicate in seconds what the lab does: methods-first computational psychiatry (prediction, digital and language markers, computational modeling, generative agents), anchored in early psychosis, with transdiagnostic reach.

## Audiences

The home page serves a balanced mix, and every audience must find its path within one click:

| Audience | Needs | Entry point |
|---|---|---|
| Researchers / collaborators | Themes, projects, papers, code | Research, Publications |
| Prospective students / PhDs / MD theses | What positions exist, how to apply | Join us |
| Funders / institution | Profile, impact, partners | Home, About |
| Patients / families | Clinical help, not research | Prominent link to FETZ |

## Site map

- **/** Home
- **/research**: theme overview → **/research/[theme]** → **/projects/[slug]**
- **/publications**
- **/team**: current team plus alumni section → **/team/[slug]** for bios
- **/news** → **/news/[slug]**
- **/join**: Join us
- **/code**: Code & tools (only public repositories)
- **/contact**
- **/impressum** and **/datenschutz**: legally required in Germany; create placeholders and flag them for me to fill in
- German versions for **/join** (Doktorarbeit) and the patient notice. Everything else is English only.

## Home page layout (top to bottom)

1. **Hero:** lab name, a one-sentence mission (draft three options for me to choose from), and a subtle abstract network or graph visual (SVG or canvas, no stock brain photos). Two buttons: "Our research" and "Join us".
2. **Patient notice band:** a small, calm, clearly separated band, e.g. "Looking for support? Our early recognition centre FETZ helps young people with mental health concerns →", with the text in German and English.
3. **Research themes:** 4 tiles, each with an icon or mini-visual, a one-line description and the number of projects.
4. **Latest news (3) and Selected publications (3)** side by side on desktop, stacked on mobile.
5. **Join us teaser:** one sentence plus a link.
6. **Partners strip:** monochrome logos of partner institutions; I will supply them, so use placeholders.
7. **Footer:** address, contact, Impressum, Datenschutz, GitHub, ORCID links.

## Research structure

Group projects into themes (propose a final mapping for me to confirm):

- **Prediction & precision psychiatry:** CHR prediction, PRESCIENT / AMP SCZ, CARE, personalized cognitive training.
- **Language & digital markers:** LAMBDA, PhenoNetz (EMA).
- **Computational modeling & generative agents:** TVB connectome modeling, symptom networks, Digital Twins and Generative Agents.
- **Clinical interventions:** PsyLetics, cannabis-induced psychosis.

Project frontmatter: `title, slug, theme, status (active|completed), years, funder, partners, url, image, summary (≤ 40 words)`. Fill in only the fields the export contains; leave the rest empty and list them for me.

Project cards show the image, title, summary, a status badge and the theme tag.

## Team page

- Group the grid by role: Lab leads → Senior researchers → Postdocs → PhD students → MSc / MD students.
- Use square photos with a consistent crop (object-fit, face-centered where possible) and grayscale-to-color on hover, but only if it doesn't hurt accessibility.
- A card shows name, title and role. Clicking opens the bio page.
- **Alumni:** a compact list (name, degree earned here, "now at") with no full bios.
- Show photos for all team members. Still add a `show_photo: true|false` field per person (default `true`) so an individual photo can be hidden later.

## News

- A list view with date, a type tag (paper | award | people | event | media), a thumbnail and a one-line excerpt. Paginate at 10 items.
- Drop the "Welcome X" posts and the outdated job ads, but list them for me before deleting.
- Rewrite the long LinkedIn-style post into a short news item with a link to the paper.

## Publications

- Generate the page from `content/publications.bib` (start with a placeholder; I will provide the file).
- Filter by year and theme, and add a "Selected" toggle.
- Badges for each paper: PDF, Preprint, Code, Data, DOI.
- Highlight lab members' names in author lists.

## Join us page

- Sections: Open positions (can be empty, with a "none at the moment" text), PhD, MD thesis (Doktorarbeit, in German), MSc thesis, internships / visiting researchers.
- Each section says what we look for, what to send, and to whom (use a placeholder email I will confirm).
- No contact form. Use mailto links only.

## Visual design

- Typography-led and calm: one serif or humanist font for headings and a clean sans for body text, self-hosted with no Google Fonts call (GDPR).
- One accent color (propose 2–3 options) plus neutrals; support light and dark mode.
- Generous white space, a max content width of about 72ch for text and a 12-column grid for cards.
- Subtle motion only, respecting `prefers-reduced-motion`.
- Accessibility: WCAG 2.1 AA contrast, keyboard navigation, alt text on all images, semantic HTML.

## Technical requirements

- Astro with content collections, deployable to GitHub Pages or Netlify via GitHub Actions.
- No tracking, no cookies, no third-party embeds. If video is needed, use a click-to-load YouTube placeholder.
- Optimize images: AVIF/WebP, responsive sizes, lazy loading.
- Add SEO meta tags, Open Graph images and structured data (Organization, Person, ScholarlyArticle).
- Lighthouse score ≥ 95 in all four categories.
- Add `EDITING.md` explaining how to add a news post, a team member, a publication and a project, with copy-paste templates.

## Process

1. Ask me about the open content issues listed in README.md.
2. Build a static mockup of the Home and Team pages first and show me before building everything else.
3. Then build the full site and deploy it to a preview URL. Do not touch the DNS for kambeitzlab.com.
