import type { APIRoute } from 'astro';
import { isProduction } from '../lib/url';

// Only the real domain is indexed; preview deployments (github.io, netlify.app) are not.
export const GET: APIRoute = ({ site }) => {
  const body = isProduction(site)
    ? `User-agent: *\nAllow: /\n\nSitemap: ${new URL(`${import.meta.env.BASE_URL.replace(/\/$/, '')}/sitemap-index.xml`, site)}\n`
    : 'User-agent: *\nDisallow: /\n';
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
