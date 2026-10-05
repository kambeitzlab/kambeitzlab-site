/** Prefix an absolute site path with the configured base (needed on GitHub Pages project URLs). */
export function url(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}${path.startsWith('/') ? path : `/${path}`}`;
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
}

export const PRODUCTION_HOST = 'kambeitzlab.com';

/** True only when building for the real domain (not a preview URL). */
export function isProduction(site: URL | undefined): boolean {
  return site?.hostname === PRODUCTION_HOST || site?.hostname === `www.${PRODUCTION_HOST}`;
}
