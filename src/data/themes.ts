import type { THEME_IDS } from '../content.config';

export type ThemeId = (typeof THEME_IDS)[number];

export interface Theme {
  id: ThemeId;
  title: string;
  short: string;
  description: string;
}

export const themes: Theme[] = [
  {
    id: 'prediction',
    title: 'Prediction & precision psychiatry',
    short: 'Prediction',
    description: 'Machine-learning models that forecast individual outcomes in people at clinical high risk.',
  },
  {
    id: 'language-digital',
    title: 'Language & digital markers',
    short: 'Language & digital',
    description: 'Speech, language and smartphone data as scalable markers of mental health.',
  },
  {
    id: 'modeling',
    title: 'Computational modeling & generative agents',
    short: 'Modeling',
    description: 'Brain-network simulations, symptom networks, digital twins and LLM-based agents.',
  },
  {
    id: 'interventions',
    title: 'Clinical interventions',
    short: 'Interventions',
    description: 'Trials and cohorts that turn insights into better treatment for young people.',
  },
];

export const themeById = Object.fromEntries(themes.map((t) => [t.id, t])) as Record<ThemeId, Theme>;
