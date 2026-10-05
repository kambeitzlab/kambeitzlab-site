# kambeitzlab.com – content export from Wix

Exported 2026-10-05 from the Wix site "Prediction Lab" (site ID 7d1dcbb7-abad-4dd0-9a31-809e10ad808f).
Live site: https://josephkambeitz.wixsite.com/website (kambeitzlab.com)

| File | Content | Items |
|---|---|---|
| team.yaml | Current team, bios as Markdown | 16 |
| alumni.yaml | Lab alumni | 17 |
| projects.yaml | Research projects | 11 |
| news.yaml | News posts, newest first | 35 |
| download_images.py | Fetches all 81 referenced images from the Wix CDN into ./images | – |

**Not included:**
- Wix CMS collection "Talks" is empty.
- "Prospective Research" contains only Lorem-ipsum placeholders.
- The "Contact" collection holds form submissions (personal data), so it is not part of the site content.
- Static page text (home page, about, contact, any publications page) is not in the CMS. Claude Code should scrape it from the live site.

## Content issues to decide on (flagged during export)

- **Team vs. alumni overlap:** Badde, Völkel, Walter, Zubair, Hoheisel and Rosen appear in both lists. Several others on the team list (e.g. Chakraborty, Baştürk, Hacker) were Master's students in 2023 and are probably also alumni by now.
- **Stale or broken content:**
  - The PRESCIENT project link is truncated ("ampscz.or").
  - The "Normaler als du denkst" post is cut off mid-word.
  - There are duplicate "Welcome Hannah!" posts.
  - Two news items announce job openings from 2021 and 2023.
  - One project title ends in " Copy".
- **New project without image:** Digital Twins and Generative Agents.

## Prompt for Claude Code

Start Claude Code in an empty folder that contains this export as `content-export/`, then paste:

> Build a new website for my research lab (Kambeitz Lab, University Hospital Cologne) as a static site with Astro, deployable to GitHub Pages or Netlify.
>
> 1. Run `content-export/download_images.py`, then convert the YAML files in `content-export/` into Astro content collections (one Markdown file per team member, alumnus, project and news post). Optimize and resize the images.
> 2. Scrape the remaining static text (home, about, contact, publications if present) from https://josephkambeitz.wixsite.com/website and put it into Markdown pages.
> 3. Pages: Home (lab mission, latest 3 news, featured projects), Research, Team (current + alumni section), News (with pagination), Publications (generated from a `publications.bib` file; create a placeholder for now), Contact.
> 4. Design: clean, modern, academic, fast. Light and dark mode, responsive, accessible. No tracking or cookies; a privacy-friendly contact link (mailto) instead of a form.
> 5. Set up a GitHub Actions workflow for deployment and give me the steps to preview it on a test URL. Do not touch DNS for kambeitzlab.com.
> 6. Add a short `EDITING.md` explaining how to add a news post or a team member.
>
> Before building, read `content-export/DESIGN_BRIEF.md` (layout, structure and design requirements; it takes precedence over the points above) and the "Content issues" section in `content-export/README.md`, then ask me how to resolve each open issue.
