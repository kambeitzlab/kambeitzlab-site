# Open items (as of 2026-10-05)

## Content to supply
- [ ] **Publications – themes:** the 158 entries from `publications.txt` got their `theme` from keyword rules; 65 match no rule and only appear under "All themes". Please review/add `theme = {…}` in `content/publications.bib`.
- [ ] **Publications – DOIs:** 24 entries still have no DOI (none in the list and no confident Crossref match). DOIs found via Crossref (105) were accepted only with a near-identical title; spot-check if in doubt.
- [x] **Publications – selected:** Penzel et al. 2026 (Mol Psychiatry), Vogel & Kambeitz 2026 (Psychiatry Res), Kambeitz & Meyer-Lindenberg 2025 (npj Digit Med); set 2026-10-07. Change via `keywords = {selected}`.
- [ ] **Project details:** status, years, funder and partners are empty for all 11 projects; a project URL is missing for 8 (PsyLetics, CHR prediction, CIP, cognitive training, PhenoNetz, symptom networks, TVB connectome, Digital Twins).
- [ ] **Project summaries** (card text) were taken from the first sentences of each description. Please review; ≤ 40 words.
- [ ] **Kathrin Seeger:** photo, and check the drafted bio.
- [ ] **PhD students' bios** (Böke, Chakraborty) still describe their 2023 Master's theses (Hacker updated 2026-10-06, Baştürk 2026-10-07).
- [ ] **Image alt texts:** `image_alt` is empty for news and project images (empty = treated as decorative).
- [ ] **Partner logos:** later; the strip stays hidden until `partners` in `src/data/site.ts` has entries.
- [ ] **Lab GitHub and ORCID links** (`src/data/site.ts`): hidden until set. Code page: list public repositories in `src/data/code.ts`.

## To confirm
- [ ] **Application email** on the Join page (`applyEmail` in `src/data/site.ts`), currently fetz@uk-koeln.de.
- [ ] **Join us texts** (requirements, what to send) are drafts; the Doktorarbeit section is in German.
- [ ] **Theme mapping:** follows the design brief; personalized cognitive training is under Prediction (could also go under Interventions).
- [ ] **Address** in footer/contact: Kerpener Str. 62, 50937 Köln.

## Legal (before going live)
- [x] Legal pages final and live (draft banner removed 2026-10-07); see LEGAL_TODO.md.

## Done / decided
- Team, alumni, roles and section structure confirmed (2026-10-05).
- Accent: deep teal. Mission text supplied by Joseph.
- PRESCIENT link fixed; "Normaler als du denkst" ending restored from the live site; duplicate "Welcome Hannah!" removed; LinkedIn-style post shortened with DOI link; TVB project shortened title; generated image for Digital Twins.
