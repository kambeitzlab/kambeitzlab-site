"""One-off import: content-export/*.yaml -> Astro content collections (Markdown).

Run from the repo root after `python content-export/download_images.py`:
    python3 scripts/import_wix.py
Images are resized (max 1600 px) and copied to src/assets/<collection>/; Astro
then generates AVIF/WebP in responsive sizes at build time.
Re-running overwrites the generated files, so do not run it after manual edits.
The import was completed on 2026-10-05; the Markdown files in src/content/ are now
the source of truth (and contain hand-added entries), so the script refuses to run
while src/content/ exists.
"""
import pathlib
import re
import unicodedata

import yaml
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPORT = ROOT / "content-export"
IMAGES = EXPORT / "images"
CONTENT = ROOT / "src" / "content"
ASSETS = ROOT / "src" / "assets"
MAX_SIZE = 1600

# --- Decisions agreed with Joseph (2026-10-05) -------------------------------

# On the Wix team list but former members (confirmed) -> alumni only.
# Uses their Wix alumni entry if there is one, otherwise the team entry.
MOVED_TO_ALUMNI = {"linnea-hoheisel", "nina-walter", "alina-zubair", "luzie-badde",
                   "marlene-rosen", "sophie-fengler", "laura-voelkel"}

# Role groups (confirmed); Wix only had a numeric `order`.
ROLES = {
    "joseph-kambeitz": "lead", "lana-kambeitz-ilankovic": "lead",
    "jessica-hartmann": "senior", "lotta-pries": "senior", "theresa-lichtenstein": "senior",
    "annkathrin-boeke": "phd", "hannah-hacker": "phd", "millennia-chakraborty": "phd",
    "oeznur-basturk": "phd",
}
ROLE_LABELS = {"lead": "Lab lead", "senior": "Senior researcher", "postdoc": "Postdoc",
               "phd": "PhD student", "student": "MSc / MD student"}

# Proposed theme mapping (to be confirmed).
THEMES = {
    "individualised-prediction-in-clinical-high-risk": "prediction",
    "prescient-amp-scz": "prediction",
    "care-network": "prediction",
    "personalized-cognitive-training": "prediction",
    "lambda-study": "language-digital",
    "phenonetz": "language-digital",
    "computational-modeling-functional-connectome": "modeling",
    "symptom-networks": "modeling",
    "digital-twins-and-generative-agents-in-mental-health": "modeling",
    "psyletics": "interventions",
    "cannabis-induced-psychosis": "interventions",
}
SHORT_TITLES = {
    "computational-modeling-functional-connectome": "Computational modeling of the functional connectome",
    "phenonetz": "PhenoNetz: transdiagnostic phenotyping with experience sampling",
}
URL_FIXES = {"https://www.ampscz.or": "https://www.ampscz.org/"}

# News posts dropped: duplicate "Welcome Hannah!" (later copy).
DROP_NEWS = {("2023-11-02", "Welcome Hannah!")}

NEWS_TYPES = {
    "PsyAgent": "paper", "Normaler": "media", "Can AI minds": "paper",
    "DGPPN conference in Berlin": "event", "New Preprint": "paper",
    "editorial board": "people", "ECNP": "event", "Summer School": "event",
    "WDR Podcast": "media", "New Homepage": "media", "cover of our work": "media",
    "out in Science": "paper", "Mental Health matters": "event", "Pre-X-Mas": "event",
    "Welcome": "people", "PRESCIENT starts": "event", "Advocating": "event",
    "Award for": "award", "open position": "people", "CARE-network": "event",
    "funding": "award", "X-mas": "event", "Habilitation": "people",
    "Successful PhDs": "people", "PhD thesis": "people", "Award winning": "award",
    "PhD Position": "people",
}

# Body text fixes.
NORMALER_FULL = "A concise and informative overview."  # restored from the live site

AI_MINDS_BODY = """Can artificial minds help us understand what shapes mental health? In our new paper in *npj Digital Medicine*, written with Andreas Meyer-Lindenberg, we propose using **generative agents** (AI entities powered by large language models, after Park et al.) to simulate how environmental and social factors affect mental health. Picture virtual cities with AI citizens: agents that remember past experiences, react to their environment, interact socially and report symptoms.

This makes controlled experiments possible that could never be run in real life, and may help to accelerate intervention development, inform urban planning and advance precision psychiatry.

[Read the paper (doi:10.1038/s41746-024-01422-z)](https://doi.org/10.1038/s41746-024-01422-z)
"""

# -----------------------------------------------------------------------------


def slugify(text):
    text = text.replace("ö", "oe").replace("ä", "ae").replace("ü", "ue").replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def process_image(media_id, collection, name):
    """Resize a downloaded Wix image and return its path relative to the md file."""
    if not media_id or media_id == "None":
        return None
    src = IMAGES / media_id
    if not src.exists():
        raise SystemExit(f"missing image {media_id}; run download_images.py first")
    out_dir = ASSETS / collection
    out_dir.mkdir(parents=True, exist_ok=True)
    img = ImageOps.exif_transpose(Image.open(src))
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    img.thumbnail((MAX_SIZE, MAX_SIZE))
    if has_alpha:
        target = out_dir / f"{name}.png"
        img.save(target, optimize=True)
    else:
        target = out_dir / f"{name}.jpg"
        img.convert("RGB").save(target, quality=86, optimize=True, progressive=True)
    return f"../../assets/{collection}/{target.name}"


def write_md(path, data, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000)
    path.write_text(f"---\n{front}---\n\n{(body or '').strip()}\n", encoding="utf-8")


def summarize(text, limit=40):
    """First sentences of a text, at most `limit` words."""
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    plain = re.sub(r"[*_#>]", "", plain)
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(plain.split()))
    out = []
    for s in sentences:
        if len(" ".join(out + [s]).split()) > limit:
            break
        out.append(s)
    if not out:
        out = [" ".join(sentences[0].split()[: limit - 1]) + "…"]
    return " ".join(out)


def load(name):
    return yaml.safe_load((EXPORT / f"{name}.yaml").read_text(encoding="utf-8"))


def import_team():
    for p in load("team"):
        slug = p["slug"]
        if slug in MOVED_TO_ALUMNI:
            continue
        data = {
            "name": p["name"],
            "title": p["title"],
            "role": ROLES[slug],
            "position": ("MD student" if p["title"] == "cand. med." else "MSc student")
                        if ROLES[slug] == "student" else ROLE_LABELS[ROLES[slug]],
            "order": int(p["order"]),
            "photo": process_image(p.get("photo"), "team", slug),
            "show_photo": True,
            "email": "",
            "orcid": "",
        }
        write_md(CONTENT / "team" / f"{slug}.md", data, p.get("bio"))


def import_alumni():
    alumni = {p["name"]: p for p in load("alumni")}
    for p in load("team"):
        if p["slug"] in MOVED_TO_ALUMNI:
            alumni.setdefault(p["name"], {**p, "bio": p.get("bio")})
    for p in alumni.values():
        slug = slugify(p["name"])
        data = {
            "name": p["name"],
            "degree": p.get("title") or "",
            "photo": process_image(p.get("photo"), "alumni", slug),
        }
        write_md(CONTENT / "alumni" / f"{slug}.md", data, p.get("bio"))


def import_projects():
    for p in load("projects"):
        slug = p["slug"]
        title = p["title"].removesuffix(" Copy")
        image = process_image(p.get("image"), "projects", slug)
        if image is None:
            image = f"../../assets/projects/{slug}.svg"  # generated placeholder
        data = {
            "title": SHORT_TITLES.get(slug, title),
            "full_title": title if slug in SHORT_TITLES else "",
            "theme": THEMES[slug],
            "status": "",
            "years": "",
            "funder": "",
            "partners": [],
            "url": URL_FIXES.get(p.get("url"), p.get("url")) or "",
            "image": image,
            "image_alt": "",
            "summary": summarize(p["body"]),
            "order": int(p["order"]),
        }
        write_md(CONTENT / "projects" / f"{slug}.md", data, p["body"])


def news_type(title):
    for key, kind in NEWS_TYPES.items():
        if key.lower() in title.lower():
            return kind
    raise SystemExit(f"no news type for {title!r}")


def import_news():
    for n in load("news"):
        date, title = str(n["date"]), n["title"].strip()
        if (date, title) in DROP_NEWS:
            continue
        body = n.get("body") or ""
        if title.startswith("“Normaler"):
            body = body.rstrip().removesuffix("A concise and infor").rstrip() + " " + NORMALER_FULL
        if title.startswith("New paper! Can AI minds"):
            body = AI_MINDS_BODY
        slug = f"{date}-{slugify(title)}"[:70].rstrip("-")
        gallery = [process_image(g, "news", f"{slug}-{i}")
                   for i, g in enumerate(n.get("gallery") or [], 1)]
        data = {
            "title": title,
            "date": date,
            "type": news_type(title),
            "image": process_image(n.get("image"), "news", slug),
            "image_alt": "",
            "excerpt": summarize(body, 30) if body.strip() else "",
            "gallery": gallery,
        }
        write_md(CONTENT / "news" / f"{slug}.md", data, body)


if __name__ == "__main__":
    if CONTENT.exists():
        raise SystemExit("src/content/ exists: import already done (see docstring)")
    import_team()
    import_alumni()
    import_projects()
    import_news()
    for c in ("team", "alumni", "projects", "news"):
        print(c, len(list((CONTENT / c).glob("*.md"))))
