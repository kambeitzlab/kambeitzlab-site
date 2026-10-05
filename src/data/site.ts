// Central place for lab-wide facts. Items marked TODO need confirmation.
export const site = {
  name: 'Kambeitz Lab',
  longName: 'Kambeitz Lab – Prevention and Prediction in Mental Health',
  tagline: 'AI and computational research in mental health',
  mission:
    'We combine clinical expertise with artificial intelligence and computational modelling to understand mental illness and improve how we predict its course. Our goal is to translate these insights into earlier recognition, more personalised treatment and better prevention.',
  description:
    'AI and computational research in mental health at the University Hospital Cologne: prediction, language and digital markers, computational modelling and generative agents.',
  // TODO: confirm the public lab address
  institution: 'Department of Psychiatry and Psychotherapy, University Hospital Cologne',
  address: ['Kerpener Str. 62', '50937 Köln', 'Germany'],
  email: 'fetz@uk-koeln.de',
  // TODO: confirm where applications should go (Join us page)
  applyEmail: 'fetz@uk-koeln.de',
  // Links are hidden while empty.
  github: '', // TODO: lab GitHub organisation, e.g. https://github.com/kambeitzlab
  orcid: '', // TODO: Joseph's ORCID iD, e.g. https://orcid.org/0000-…
  fetz: 'https://psychiatrie-psychotherapie.uk-koeln.de/klinik/frueherkennungs-und-therapiezentrum-fetz/',
};

export const nav = [
  { href: '/research/', label: 'Research' },
  { href: '/publications/', label: 'Publications' },
  { href: '/team/', label: 'Team' },
  { href: '/news/', label: 'News' },
  { href: '/join/', label: 'Join us' },
  { href: '/contact/', label: 'Contact' },
];

// Partner/funder logos (monochrome SVG in src/assets/partners/). The strip on the
// home page is hidden while this list is empty.
export const partners: { name: string; logo: string; url?: string }[] = [];
