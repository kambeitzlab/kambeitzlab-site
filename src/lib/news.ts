import { getCollection } from 'astro:content';

export const NEWS_PER_PAGE = 10;

/** All news posts, newest first. */
export async function getNews() {
  return (await getCollection('news')).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}
