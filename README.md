# kambeitzlab.com

Static website of the Kambeitz Lab, built with [Astro](https://astro.build). No cookies, no tracking, no third-party requests.

- **Editing content:** see [EDITING.md](EDITING.md)
- **Open items** (content to supply, decisions): see [OPEN_ITEMS.md](OPEN_ITEMS.md) and [LEGAL_TODO.md](LEGAL_TODO.md)

## Run locally

Requires Node.js 22+.

```sh
npm install
npm run dev       # http://localhost:4321, live reload
npm run build     # production build into dist/
npm run preview   # serve dist/ locally
```

## Preview on a test URL (GitHub Pages)

The workflow in `.github/workflows/deploy.yml` builds and publishes the site on every push to `main`. Nothing here touches the DNS of kambeitzlab.com; the preview lives at `https://<github-user>.github.io/<repo>/`.

1. Create a new repository on GitHub (e.g. `kambeitzlab-site`). On the free GitHub plan, Pages only works for **public** repositories; use Netlify (below) if the repository must stay private.
2. Push this folder:
   ```sh
   git init -b main
   git add .
   git commit -m "Initial website"
   git remote add origin https://github.com/<github-user>/kambeitzlab-site.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Open the **Actions** tab, wait for "Deploy to GitHub Pages" to finish (about 1–2 minutes; re-run it once if the first run happened before step 3). The URL is shown in the run summary.

Preview deployments are marked `noindex` and their `robots.txt` blocks crawlers, so search engines only index the site once it runs on kambeitzlab.com.

### Alternative: Netlify

**Add new site → Import an existing project → GitHub → this repository.** Netlify reads `netlify.toml`; the preview URL is `https://<name>.netlify.app`. Works with private repositories.

## Structure

```
content/publications.bib       publications (BibTeX)
src/content/{team,alumni,projects,news}/   one Markdown file per entry
src/assets/                    images (optimized automatically at build time)
src/data/site.ts               contact details, navigation, partners
src/data/themes.ts             the four research themes
src/data/about.md              research intro text (Focus / Methods / Aims)
src/pages/                     page templates and the legal pages
scripts/import_wix.py          one-off import from the Wix export (already done)
content-export/                original Wix export (images not committed)
```
