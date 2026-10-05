// Public repositories shown on /code. Only list PUBLIC repositories.
// { name: 'psyagent', description: 'One sentence.', url: 'https://github.com/…', language: 'Python', paper?: 'https://doi.org/…' }
export interface Repo {
  name: string;
  description: string;
  url: string;
  language?: string;
  paper?: string;
}

export const repos: Repo[] = [];
