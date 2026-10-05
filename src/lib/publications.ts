import fs from 'node:fs';
import path from 'node:path';
import { parse, type Creator } from '@retorquere/bibtex-parser';
import { getCollection } from 'astro:content';
import type { ThemeId } from '../data/themes';

const BIB_FILE = path.resolve('content/publications.bib');

export interface Author {
  display: string;
  isMember: boolean;
}

export interface Publication {
  key: string;
  title: string;
  authors: Author[];
  venue: string;
  year: number;
  volume: string;
  pages: string;
  themes: ThemeId[];
  selected: boolean;
  links: { label: 'PDF' | 'Preprint' | 'Code' | 'Data' | 'DOI'; href: string }[];
  doi: string;
}

const fold = (s: string) =>
  s.normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/ß/g, 'ss').toLowerCase().trim();

/** "lastname|initial" keys for everyone on the team and alumni lists. */
async function memberKeys(): Promise<Set<string>> {
  const people = [...(await getCollection('team')), ...(await getCollection('alumni'))];
  const keys = new Set<string>();
  for (const { data } of people) {
    const parts = data.name.split(/\s+/);
    const first = parts[0];
    // "Pedro Costa Klein" is cited as "Klein, P. C." or "Costa Klein, P."
    for (let i = 1; i < parts.length; i++) {
      keys.add(`${fold(parts.slice(i).join(' '))}|${fold(first)[0]}`);
    }
  }
  return keys;
}

function formatAuthor(c: Creator, members: Set<string>): Author {
  if (c.name) return { display: c.name, isMember: false };
  const last = [c.prefix, c.lastName].filter(Boolean).join(' ');
  const initials = (c.firstName ?? '')
    .split(/[\s.]+/)
    .filter(Boolean)
    .map((p) => p.split('-').map((q) => `${q[0]}.`).join('-'))
    .join(' ');
  const key = `${fold(c.lastName ?? '')}|${fold(c.firstName ?? '')[0] ?? ''}`;
  return { display: initials ? `${last}, ${initials}` : last, isMember: members.has(key) };
}

/** Bibtex-parser renders some fields as HTML; keep only harmless inline tags. */
const cleanHtml = (s = '') => s.replace(/<(?!\/?(i|em|b|strong|sub|sup)>)[^>]*>/g, '');

let cache: Promise<Publication[]> | undefined;

export function getPublications(): Promise<Publication[]> {
  cache ??= load();
  return cache;
}

async function load(): Promise<Publication[]> {
  if (!fs.existsSync(BIB_FILE)) return [];
  const members = await memberKeys();
  const lib = parse(fs.readFileSync(BIB_FILE, 'utf-8'), { sentenceCase: false, english: false });
  for (const err of lib.errors) console.warn(`[publications.bib] ${err.error}`);

  const pubs = lib.entries.map((e): Publication => {
    const f = e.fields as Record<string, any>;
    const doi = (f.doi ?? '').replace(/^https?:\/\/(dx\.)?doi\.org\//, '');
    const links: Publication['links'] = [];
    if (f.pdf) links.push({ label: 'PDF', href: f.pdf });
    if (f.preprint || f.eprint) links.push({ label: 'Preprint', href: f.preprint ?? f.eprint });
    if (f.code) links.push({ label: 'Code', href: f.code });
    if (f.data) links.push({ label: 'Data', href: f.data });
    if (doi) links.push({ label: 'DOI', href: `https://doi.org/${doi}` });
    return {
      key: e.key,
      title: cleanHtml(f.title),
      authors: (f.author ?? []).map((c: Creator) => formatAuthor(c, members)),
      venue: cleanHtml(f.journal ?? f.journaltitle ?? f.booktitle ?? f.publisher?.[0] ?? ''),
      year: Number.parseInt(f.year ?? f.date ?? '0', 10),
      volume: f.volume ?? '',
      pages: (f.pages ?? '').replace(/--/g, '–'),
      themes: String(f.theme ?? '')
        .split(/[,;]\s*/)
        .filter(Boolean) as ThemeId[],
      selected: (f.keywords ?? []).some((k: string) => k.toLowerCase() === 'selected'),
      links,
      doi,
    };
  });
  return pubs.sort((a, b) => b.year - a.year || a.authors[0]?.display.localeCompare(b.authors[0]?.display ?? '') || 0);
}
