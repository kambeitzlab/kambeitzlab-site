// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// SITE_URL / BASE_PATH are set by the deploy workflow, so the same code works
// on a GitHub Pages project URL (…github.io/<repo>/), on Netlify and on the final domain.
export default defineConfig({
  site: process.env.SITE_URL ?? 'https://kambeitzlab.com',
  base: process.env.BASE_PATH ?? '/',
  trailingSlash: 'ignore',
  integrations: [sitemap()],
  image: { responsiveStyles: false },
  build: { format: 'directory', inlineStylesheets: 'always' },
});
