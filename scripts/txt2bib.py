"""Convert a Vancouver-style publication list (one reference per paragraph, as
exported by Zotero/EndNote/PubMed) into content/publications.bib.

    python3 scripts/txt2bib.py publications.txt            # parse + write
    python3 scripts/txt2bib.py publications.txt --doi      # also look up missing DOIs (Crossref)

- `keywords = {selected}` and `theme` of entries already in publications.bib are
  kept (matched by DOI or title); new entries get themes from keyword rules below.
- References that cannot be parsed are printed; nothing is silently dropped.
"""
import json
import re
import ssl
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "content" / "publications.bib"
CACHE = ROOT / "scripts" / ".doi-cache.json"

THEME_RULES = {
    "modeling": r"generative agent|digital twin|large language model|language model|simulat|computational model|"
                r"brain network|virtual brain|network model|symptom network|dynamic functional connectivity|neuregulin",
    "language-digital": r"\blanguage\b|speech|linguistic|smartphone|ecological momentary|\bEMA\b|digital|"
                        r"\bapps?\b|wearable|sensing|facial expression|questionnaire",
    "interventions": r"training|therap|trial|exercise|intervention|cannabis|treatment|remediation|"
                     r"psychoeducation|prevention|preventive",
    "prediction": r"predict|machine learning|classif|prognos|biomarker|multivariate|pattern recognition|"
                  r"risk calculator|polyrisk|generalizab|algorithmic fairness|clinical high[- ]risk",
}

# Typos in the source list (wrong spelling breaks lab-member highlighting).
NAME_FIXES = {"Bastruk Ö": "Baştürk Ö"}

GROUP_WORDS = re.compile(r"consortium|group|partnership|network|initiative|study|investigators|task force|"
                         r"schizophrenia|collaborat|\(amp|on behalf", re.I)
UP = "A-ZÀ-ÖØ-Þ"
NAME = re.compile(rf"^(?P<last>[^\s,][^,]*?) (?P<ini>[{UP}][{UP}a-z]{{0,3}}(?:-[{UP}][{UP}a-z]{{0,2}})?)(?: (?P<suf>3rd|2nd|Jr|Sr|Iii|III|II))?$")


def fold(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def split_authors(entry):
    """Return (authors, rest) – authors end at the first '. ' after a valid name list."""
    for wrong, right in NAME_FIXES.items():
        entry = entry.replace(f", {wrong},", f", {right},")
    for m in re.finditer(r"\. ", entry):
        items = [a.strip() for a in entry[: m.start()].split(", ")]
        if all(NAME.match(a) or GROUP_WORDS.search(a) for a in items):
            return items, entry[m.end():]
    return None, entry


def initials(ini):
    # "AB" -> "A. B.", "S-W" -> "S.-W.", "K-IK" -> "K.-I. K."
    if "-" in ini:
        head, tail = ini.split("-", 1)
        caps = [c for c in tail if c.isupper()]
        return f"{head[0]}.-{caps[0]}." + "".join(f" {c}." for c in caps[1:])
    return " ".join(f"{c}." for c in ini if c.isupper())


def bib_author(a):
    m = NAME.match(a)
    if m and not GROUP_WORDS.search(a):
        last, suf = m["last"], m["suf"]
        suf = {"3rd": "III", "Iii": "III", "2nd": "II"}.get(suf, suf)
        return f"{last}, {suf}, {initials(m['ini'])}" if suf else f"{last}, {initials(m['ini'])}"
    name = re.sub(r"^on behalf of (the )?", "", a, flags=re.I)
    return "{" + name + "}"


def expand_pages(p):
    m = re.fullmatch(r"(\d+)[–-](\d+)", p)
    if not m:
        return p.replace("–", "--")
    a, b = m.groups()
    if len(b) < len(a):
        b = a[: len(a) - len(b)] + b
    return f"{a}--{b}"


VENUE = re.compile(
    r"^(?P<title>.+?[.?!])\s+(?P<journal>[^.;]+?)\s(?P<year>(?:19|20)\d\d)"
    r"(?:;(?P<vol>[^:.;]+))?(?::(?P<pages>[^\s]+?))?\.?"
    r"(?:\s+https?://doi\.org/(?P<doi>\S+?))?\.?$"
)
CHAPTER = re.compile(
    r"^(?P<title>.+?[.?!])\s+(?P<book>.+?),\s*(?P<place>[^,:]+(?:, [^,:]+)*):\s*(?P<publisher>[^;]+);\s*"
    r"(?P<year>(?:19|20)\d\d)(?:, p\. (?P<pages>[\d–-]+))?\.?(?:\s+https?://doi\.org/(?P<doi>\S+?))?\.?$"
)


def parse(entry):
    authors, rest = split_authors(entry)
    if not authors:
        return None
    seen, uniq = set(), []
    for a in authors:  # drop duplicated group authors
        if a not in seen:
            seen.add(a)
            uniq.append(a)
    m = VENUE.match(rest)
    kind = "article"
    if not m or "," in m["journal"] and ":" in rest:
        mc = CHAPTER.match(rest)
        if mc:
            m, kind = mc, "incollection"
    if not m:
        return None
    d = m.groupdict()
    title = d["title"]
    if title.endswith("."):
        title = title[:-1]
    return {
        "type": kind,
        "authors": uniq,
        "title": title.strip(),
        "journal": (d.get("journal") or "").strip(),
        "booktitle": (d.get("book") or "").strip(),
        "publisher": (d.get("publisher") or "").strip(),
        "address": (d.get("place") or "").strip(),
        "year": d["year"],
        "volume": (d.get("vol") or "").strip(),
        "pages": expand_pages(d["pages"]) if d.get("pages") else "",
        "doi": (d.get("doi") or "").rstrip("."),
    }


def guess_themes(title):
    return [t for t, rx in THEME_RULES.items() if re.search(rx, title, re.I)]


def crossref_doi(p, cache):
    key = fold(p["title"])
    if key in cache:
        return cache[key]
    q = f"{p['title']} {p['journal']} {p['year']} {p['authors'][0]}"
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": q, "rows": 3})
    req = urllib.request.Request(url, headers={"User-Agent": "kambeitzlab-site/1.0 (publication list import)"})
    doi = ""
    try:
        try:
            import certifi  # python.org builds on macOS ship without CA certificates
            ctx = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            ctx = None
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            items = json.load(r)["message"]["items"]
        for it in items:
            t = " ".join(it.get("title") or [])
            sim = SequenceMatcher(None, fold(t), key).ratio()
            yr = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
            if sim >= 0.93 and (yr is None or abs(int(yr) - int(p["year"])) <= 1):
                doi = it["DOI"]
                break
    except Exception as e:  # network problems: just skip
        print("  crossref error:", e)
        return ""
    cache[key] = doi
    time.sleep(1.0)
    return doi


def existing_flags():
    """theme/selected from the current bib, keyed by DOI and folded title."""
    flags = {}
    if not BIB.exists():
        return flags
    for block in re.split(r"\n@", BIB.read_text(encoding="utf-8")):
        title = re.search(r"\btitle\s*=\s*\{(.+?)\},\n", block, re.S)
        if not title:
            continue
        theme = re.search(r"\btheme\s*=\s*\{(.*?)\}", block)
        doi = re.search(r"\bdoi\s*=\s*\{(.*?)\}", block)
        sel = "selected" in (re.search(r"keywords\s*=\s*\{(.*?)\}", block) or [""])[0]
        v = {"theme": theme[1] if theme else "", "selected": sel}
        flags[fold(re.sub(r"[{}\\\"]", "", title[1]))] = v
        if doi:
            flags[doi[1].lower()] = v
    return flags


def bib_escape(s):
    return s.replace("&", r"\&").replace("%", r"\%")


def main():
    src = Path(sys.argv[1])
    lookup = "--doi" in sys.argv
    entries = [e.strip() for e in re.split(r"\n\s*\n", src.read_text(encoding="utf-8")) if e.strip()]
    flags = existing_flags()
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    out, failed, keys = [], [], set()
    stats = {"doi_given": 0, "doi_found": 0, "kept_flags": 0}
    for e in entries:
        p = parse(e)
        if not p:
            failed.append(e)
            continue
        if p["doi"]:
            stats["doi_given"] += 1
        elif lookup:
            p["doi"] = crossref_doi(p, cache)
            stats["doi_found"] += bool(p["doi"])
        prev = flags.get(p["doi"].lower()) if p["doi"] else None
        prev = prev or flags.get(fold(p["title"]))
        if prev:
            stats["kept_flags"] += 1
            themes = [t for t in prev["theme"].split(",") if t] or guess_themes(p["title"])
            selected = prev["selected"]
        else:
            themes, selected = guess_themes(p["title"]), False
        first = fold(re.sub(r"^\{|\}$", "", bib_author(p["authors"][0])).split(",")[0]).replace(" ", "")
        word = next((w for w in fold(p["title"]).split() if len(w) > 3), "x")
        key = f"{first}{p['year']}{word}"
        while key in keys:
            key += "b"
        keys.add(key)
        fields = [("author", " and ".join(bib_author(a) for a in p["authors"])), ("title", p["title"])]
        if p["type"] == "article":
            fields.append(("journal", p["journal"]))
        else:
            fields += [("booktitle", p["booktitle"]), ("publisher", p["publisher"]), ("address", p["address"])]
        fields += [("volume", p["volume"]), ("pages", p["pages"]), ("year", p["year"]), ("doi", p["doi"]),
                   ("theme", ",".join(themes))]
        if selected:
            fields.append(("keywords", "selected"))
        body = ",\n".join(f"  {k:<9}= {{{bib_escape(v)}}}" for k, v in fields if v)
        out.append(f"@{p['type']}{{{key},\n{body},\n}}\n")
    if lookup:
        CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
    header = (
        f"% Generated from {src.name} by scripts/txt2bib.py on {time.strftime('%Y-%m-%d')}.\n"
        "% You can edit this file directly (see EDITING.md for the extra fields theme/keywords/pdf/code/data).\n"
        "% `theme` was assigned by keyword rules for entries that were not on the site before – please review.\n\n"
    )
    BIB.write_text(header + "\n".join(out), encoding="utf-8")
    print(f"{len(out)} entries written, {len(failed)} failed; {stats}")
    for e in failed:
        print("FAILED:", e[:300])


if __name__ == "__main__":
    main()
