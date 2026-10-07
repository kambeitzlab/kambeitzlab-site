import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

export const THEME_IDS = ['prediction', 'language-digital', 'modeling', 'interventions'] as const;
export const ROLE_IDS = ['lead', 'senior', 'postdoc', 'phd', 'student'] as const;
export const NEWS_TYPES = ['paper', 'award', 'people', 'event', 'media'] as const;

const team = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/team' }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      title: z.string().default(''),
      role: z.enum(ROLE_IDS),
      position: z.string(),
      order: z.number().default(99),
      photo: image().optional().nullable(),
      photo_focus: z.string().default('50% 30%'),
      show_photo: z.boolean().default(true),
      email: z.string().default(''),
      orcid: z.string().default(''),
      // Own research group led by this person (shown on card, bio and research page)
      group: z
        .object({ name: z.string(), url: z.string().default(''), description: z.string().default('') })
        .optional(),
    }),
});

const alumni = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/alumni' }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      degree: z.string().default(''),
      photo: image().optional().nullable(),
    }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      full_title: z.string().default(''),
      theme: z.enum(THEME_IDS),
      status: z.enum(['active', 'completed', '']).default(''),
      years: z.string().default(''),
      funder: z.string().default(''),
      partners: z.array(z.string()).default([]),
      url: z.string().default(''),
      image: image().optional().nullable(),
      image_alt: z.string().default(''),
      // 'contain' for logos/figures (shown whole on a light panel), 'cover' for photos
      image_fit: z.enum(['contain', 'cover']).default('contain'),
      summary: z.string().refine((s) => s.split(/\s+/).length <= 40, 'summary must be ≤ 40 words'),
      order: z.number().default(99),
    }),
});

const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      date: z.coerce.date(),
      type: z.enum(NEWS_TYPES),
      image: image().optional().nullable(),
      image_alt: z.string().default(''),
      excerpt: z.string().default(''),
      gallery: z.array(image()).default([]),
      lang: z.string().optional(), // e.g. 'de' for posts written in German
    }),
});

export const collections = { team, alumni, projects, news };
