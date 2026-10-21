#!/usr/bin/env python3
"""Extract Hungarian, Slavic and Central-European recipes from the
cookbook sources.

The user asked for stews, Hungarian food and Slavic food, and for the
gothic/classic-book connection.  Two different things are needed:

  A. REAL RECIPES from cookbooks — with ingredients and method, so they
     live in the corpus beside everything else and can be scaled and
     pantry-matched.

  B. A classification of each extracted dish by its cuisine, so the app
     can offer a "cuisine" axis alongside the era axis.

Sources and their formats:

  365 Foreign Dishes (1914)   "12.--Hungarian Beef Stew." then prose
  Allied Cookery (1890s)      "RUSSIAN PIROG KULBAK" then prose
  International Jewish Cook Book (1925)  "HUNGARIAN GOULASH" then prose
  The Art of German Cooking and Baking (Meier)  "CHAPTER" + "No. 1"

Only dishes whose text we can read in full are kept.
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "data", "sources", "cookery")

# --------------------------------------------------------------- sources
SOURCES = [
    {
        "id": 10011,
        "file": "pg10011.txt",
        "title": "365 Foreign Dishes",
        "author": "Mrs. W. E. (ed.)",
        "year": 1914,
        "publisher": "F. H. Burt / Home Publishing Co.",
        "style": "numbered",
        "url": "https://www.gutenberg.org/ebooks/10011",
    },
    {
        "id": 44947,
        "file": "pg44947.txt",
        "title": "Allied Cookery: British, French, Italian, Belgian, Russian",
        "author": "Grace Clergue Harrison",
        "year": 1895,
        "publisher": "G. P. Putnam's Sons",
        "style": "caps",
        "url": "https://www.gutenberg.org/ebooks/44947",
    },
    {
        "id": 12350,
        "file": "pg12350.txt",
        "title": "The International Jewish Cook Book",
        "author": "Florence Kreisberg Greenbaum",
        "year": 1925,
        "publisher": "The Jewish Publication Society of America",
        "style": "caps",
        "url": "https://www.gutenberg.org/ebooks/12350",
    },
    {
        "id": 63883,
        "file": "pg63883.txt",
        "title": "The Art of German Cooking and Baking",
        "author": "Lina Meier",
        "year": 1912,
        "publisher": "G. P. Putnam's Sons",
        "style": "caps",
        "url": "https://www.gutenberg.org/ebooks/63883",
    },
]

# ------------------------------------------------------- cuisine keyword
# Two tiers, and the order matters.  A demonym in the title always
# beats a dish word, so "RUSSIAN GOULASH" is Russian and not Hungarian.
# Tier 1: the country or people is named.
CUISINE_PATTERNS = [
    ("Hungarian", re.compile(r"\b(hungar\w*|magyar)\b", re.I)),
    ("Russian", re.compile(r"\b(russian|russia\w*)\b", re.I)),
    ("Polish", re.compile(r"\b(polish|poland\w*)\b", re.I)),
    ("Slavic / Eastern European", re.compile(
        r"\b(slav\w*|ruthen\w*|czech|moravian|bulgarian|serbian|romanian|"
        r"yugoslav|croatian|slovak|silesian)\b", re.I)),
    ("Jewish (Ashkenazi)", re.compile(r"\b(jew\w*|kosher)\b", re.I)),
    ("Turkish / Ottoman", re.compile(
        r"\b(turkish|turkey|ottoman|constantinople)\b", re.I)),
    ("Greek", re.compile(r"\b(greek|greece|athen\w*)\b", re.I)),
    ("Italian", re.compile(r"\b(italian|italy)\b", re.I)),
    ("French", re.compile(r"\b(french|france\w*|paris\w*)\b", re.I)),
    ("German", re.compile(
        r"\b(german|germany\w*|prussian|bavarian|saxon|swiss|austrian|"
        r"viennese|vienna|tyrol\w*|bohemian)\b", re.I)),
]

# Tier 2: the dish itself names the cuisine.
CUISINE_BY_DISH = [
    ("Hungarian", re.compile(
        r"\b(goulash|goulach|goulasch|goulash|paprikas?|csarne\w*|schnitzel|halasz\w*|kifli\w*|d\xf3l\w*|p\xf6r\w*)\b",
        re.I)),
    ("Russian", re.compile(
        r"\b(pirog\w*|blini|borsch\w*|borscht|zakus\w*|zakouska|"
        r"strogonoff|oliv\w*|koulitch\w*|koulak|schtschi|shchi|"
        r"vareniki)\b", re.I)),
    ("Polish", re.compile(
        r"\b(pierogi|pyre\w*|bigos|kopytka|kolacky|rozgal\w*|"
        r"zapiekank\w*|barszcz|sauerkraut)\b", re.I)),
    ("Slavic / Eastern European", re.compile(
        r"\b(holub\w*|smetana|rus)\b", re.I)),
    ("Jewish (Ashkenazi)", re.compile(
        r"\b(passover|shabbath|sabbath|hanukkah|blintz\w*|kugel|"
        r"cholent|tsholent)\b", re.I)),
    ("Turkish / Ottoman", re.compile(
        r"\b(kebob|kebab|pilaf|pilaff|shish)\b", re.I)),
    ("Greek", re.compile(r"\b(spanakopita)\b", re.I)),
    ("Italian", re.compile(r"\b(macaroni|spaghetti)\b", re.I)),
    ("French", re.compile(r"\b(beefsteak)\b", re.I)),
    ("German", re.compile(r"\b(sauerkraut)\b", re.I)),
]

# Words that appear inside a body but never justify a cuisine label
# on their own.
BODY_ONLY_OK = {
    "Hungarian": re.compile(r"\b(goulash|goulach|paprika|paprikas|"
                            r"hungarian)\b", re.I),
    "Russian": re.compile(r"\b(pirog\w*|borsch\w*|borscht|strogonoff|"
                          r"koulitch\w*|zakouska|russian)\b", re.I),
    "Polish": re.compile(r"\b(polish|pierogi|bigos|sauerkraut)\b", re.I),
    "Slavic / Eastern European": re.compile(
        r"\b(slav\w*|czech|serbian|romanian|yugoslav|holub\w*|"
        r"koulak\w*|smetana)\b", re.I),
    "German": re.compile(r"\b(german\w*|prussian|bavarian|viennese)\b", re.I),
    "Jewish (Ashkenazi)": re.compile(
        r"\b(jew\w*|kosher|passover|shabbath|blintz\w*|cholent|"
        r"tsholent)\b", re.I),
    "Turkish / Ottoman": re.compile(
        r"\b(turkish|ottoman|kebob|kebab|pilaf|pilaff)\b", re.I),
    "Greek": re.compile(r"\b(greek|athen\w*)\b", re.I),
    "Italian": re.compile(r"\b(italian|macaroni|spaghetti)\b", re.I),
    "French": re.compile(r"\b(french|paris\w*|beefsteak)\b", re.I),
}

# dishes we always want, even if the country word is absent
FORCE = re.compile(
    r"\b(goulash|goulach|borscht|borsch|betwarmed|"
    r"beefsteak|strogonoff|paprika|borsh)\b", re.I)


def clean(t):
    t = re.sub(r"\r\n?", "\n", t)
    t = t.replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"')
    t = t.replace("—", "--").replace("–", "-")
    return t


def strip_gutenberg(text):
    m = re.search(r"\*\*\*\s*START OF TH[EI][\s\S]*?\*\*\*", text)
    if m:
        text = text[m.end():]
    m = re.search(r"\*\*\*\s*END OF TH[EI][\s\S]*?\*\*\*", text)
    if m:
        text = text[:m.start()]
    return text


def norm(s):
    return " ".join(s.lower().split())


def classify(title, body):
    """Cuisine label, or None if we cannot place the dish.

    Title wins.  Body is only consulted for the words that are genuinely
    diagnostic.  Anything we cannot place is dropped rather than guessed
    at — a wrong cuisine label is worse than a missing recipe.
    """
    # A dish word that names a cuisine is more specific than a country
    # demonym, so "Austrian Goulasch" is Hungarian goulash and not
    # Austrian.  Check the dish tier first, but only for words that
    # genuinely pin a cuisine.
    for name, pat in CUISINE_BY_DISH:
        if pat.search(title):
            return name
    for name, pat in CUISINE_PATTERNS:
        if pat.search(title):
            return name
    for name, pat in BODY_ONLY_OK.items():
        if pat.search(body[:400]):
            return name
    if FORCE.search(title):
        return "Hungarian"
    return None


# headings that are front-matter, not dishes
JUNK_TITLE = re.compile(
    r"\b(contents|index|preface|introduction|foreword|appendix|"
    r"chapter|menu|advertis|publishers|list of illustrations|"
    r"errata|glossary|bibliography)\b", re.I)


# ---------------------------------------------------------- per style
def extract_numbered(text, src):
    """'12.--Hungarian Beef Stew.' heading, prose body."""
    out = []
    pat = re.compile(r"^(\d+)\.--(.+?)\.\s*$", re.M)
    ms = list(pat.finditer(text))
    for i, m in enumerate(ms):
        title = m.group(2).strip()
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[start:end].strip()
        # body should be prose only
        body = re.sub(r"^[_\*]{3,}.*$", "", body, flags=re.M).strip()
        if len(body) < 60:
            continue
        out.append((title, body))
    return out


def extract_caps(text, src):
    """'RUSSIAN PIROG KULBAK' heading, prose body, ALL CAPS."""
    out = []
    # headings: 2-6 lines of all caps, each 3-70 chars
    pat = re.compile(r"^([A-Z][A-Z0-9 ,'&\-\.\(\)]{2,70})\s*$", re.M)
    ms = []
    for m in pat.finditer(text):
        h = m.group(1).strip()
        if len(h.split()) > 9:
            continue
        # must be followed by blank line then prose
        tail = text[m.end():m.end() + 200].strip()
        if not tail or tail[0].isupper() and len(tail.split()) < 12:
            continue
        ms.append(m)
    for i, m in enumerate(ms):
        title = m.group(1).strip()
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"^[_\*]{3,}.*$", "", body, flags=re.M).strip()
        if len(body) < 80:
            continue
        out.append((title, body))
    return out


def parse_ingredients(body):
    """Pull an ingredient list out of prose, when it reads like one.

    Many old recipes are pure prose.  When the prose starts with a list
    of 'n unit' patterns we can read it as an ingredient list.  When it
    doesn't, we return None and the recipe is stored as prose-only.
    """
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    if len(lines) < 2:
        return None
    # Heuristic: the first lines look like a list if they mostly contain
    # a quantity word/number and a unit.
    qty = re.compile(
        r"^\s*(?:about\s+|approximately\s+)?"
        r"(?:\d+(?:\s*/\s*\d+)?|\bone|two|three|four|five|six|seven|eight|"
        r"nine|ten|twelve|dozen|half a|quarter a|pint|quart|gill)\b",
        re.I)
    hits = 0
    for l in lines[:6]:
        if qty.match(l):
            hits += 1
    if hits < 2:
        return None
    return lines


def main():
    all_recipes = []
    for src in SOURCES:
        path = os.path.join(SRC, src["file"])
        if not os.path.exists(path):
            print(f"MISSING {src['file']}")
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            text = clean(strip_gutenberg(f.read()))

        if src["style"] == "numbered":
            pairs = extract_numbered(text, src)
        else:
            pairs = extract_caps(text, src)

        kept = 0
        for title, body in pairs:
            if JUNK_TITLE.search(title):
                continue
            # A bare ingredient word is a section heading, not a dish.
            if len(title.split()) <= 2 and not re.search(
                    r"(stew|soup|cake|pudding|pie|roll|goulash|goulach|"
                    r"roast|boil|fish|chicken|beef|mutton|pork|lamb|"
                    r"baked|fried|potato|apple|bread|pancake|omelet|"
                    r"omelette|tongue|chop|pud|cream|broth|duck|"
                    r"salmon|pike|carp|herring|mackerel|sausage|ham|"
                    r"eggs|meat|veal)", title, re.I):
                continue
            # A single word is a category heading ("Chicken", "Soups"),
            # never a dish.
            if len(title.split()) == 1:
                continue
            cuisine = classify(title, body)
            if not cuisine:
                continue
            kept += 1
            all_recipes.append({
                "source_id": src["id"],
                "source_title": src["title"],
                "source_author": src["author"],
                "source_year": src["year"],
                "source_publisher": src["publisher"],
                "source_url": src["url"],
                "title": title,
                "cuisine": cuisine,
                "body": body,
            })
        print(f"{src['title'][:45]:45} parsed={len(pairs):>5} kept={kept:>4}")

    out = os.path.join(BASE, "region_raw.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(all_recipes, f, ensure_ascii=False, indent=1)
    print(f"\nTotal kept: {len(all_recipes)}")
    from collections import Counter
    for k, v in Counter(r["cuisine"] for r in all_recipes).most_common():
        print(f"  {v:>5}  {k}")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
