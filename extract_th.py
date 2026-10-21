#!/usr/bin/env python3
"""Extract Tasting History recipes into schema-conformant records.

The Tasting History pages all share a structure, so the extraction is
mechanical: metadata block (city/region, time period), a prose history
paragraph, a quoted source, an ingredient list, and an instruction list.

Output: data/th_generated.py  -- a RECIPES-compatible list of dicts.

The output still needs the hand-written parts (era assignment, the
period-oddity notes, the modern substitute rationale), which are applied
by a curation pass. This script fills in the mechanical fields.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/histcook/src"
DATA = json.load(open(os.path.join(SRC, "th_data.json")))

# ---- era assignment, keyed by the era the source period falls into.
# The taxonomy is the same nine the app uses.
def era_for(period, city, title):
    """Assign one of the nine eras from the source's own date label."""
    p = (period or "").strip()
    pl = p.lower()
    c = (city or "").lower()
    t = (title or "").lower()

    # ---- explicit ancient material, checked before anything else
    if re.search(r"b\.?c\.?e|bce|bronze|stonehenge|sumer|egypt|"
                 r"babylon|mycenae|assyri|mesopotam|neolithic|"
                 r"iron age|stone age", pl + " " + t):
        return "ancient"
    if re.search(r"\b(\d{1,2}|1[0-9])\s*th century b", pl):
        return "ancient"

    # ---- roman
    if "rome" in c or "roman" in t:
        return "roman"
    if re.search(r"\b[1-5](st|nd|rd|th) century\b", pl) and \
            not re.search(r"\b1[0-9](st|nd|rd|th) century\b", pl):
        return "roman"

    # ---- medieval
    if re.search(r"medieval", pl + " " + t):
        return "medieval"
    if re.search(r"\b1[2-5](st|nd|rd|th) century\b", pl):
        return "medieval"
    if re.search(r"c\. ?1[2-4]\d\d\b", pl):
        return "medieval"

    # ---- renaissance & colonial (1500-1650)
    if re.search(r"\b1[56](st|nd|rd|th) century\b", pl):
        return "renaissance"
    if re.search(r"\b16[0-5]\d\b", pl):
        return "renaissance"
    if re.search(r"\b16\d\d\b", pl):
        return "renaissance"
    if re.search(r"\bc\. ?1[56]\d\d\b", pl):
        return "renaissance"

    # ---- georgian (1700-1830)
    if re.search(r"\b1[78](st|nd|rd|th) century\b", pl):
        return "georgian"
    if re.search(r"\b17[0-9]\d\b", pl):
        return "georgian"
    if re.search(r"\b18[0-3]\d\b", pl):
        return "georgian"
    if re.search(r"\bc\. ?17\d\d\b", pl):
        return "georgian"

    # ---- victorian (1837-1901)
    if re.search(r"\b1[89](st|nd|rd|th) century\b", pl):
        return "victorian"
    if re.search(r"\b18[3-9]\d\b", pl):
        return "victorian"
    if re.search(r"\b190[01]\b", pl):
        return "victorian"

    # ---- edwardian (1901-1914)
    if re.search(r"\b19[0-1]\d\b", pl):
        return "edwardian"

    # ---- wartime (1914-1945)
    if re.search(r"world war|wwi\b|wwii\b", pl + " " + t):
        return "wartime"
    if re.search(r"\b19[1-4]\d\b", pl):
        return "wartime"
    if re.search(r"\b194[2-5]\b", pl):
        return "wartime"

    # ---- post-war (1945-1960)
    if re.search(r"\b194[6-9]\b|\b19[5-6]\d\b", pl):
        return "postwar"
    if re.search(r"\b19[7-9]\d\b", pl):
        return "postwar"
    if "1970s" in pl:
        return "postwar"
    if re.search(r"\b19\d\d\b", pl):
        return "postwar"

    return "victorian"


# ---- unit + qty parsing
UNIT_MAP = [
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*pounds?\b", re.I), "lb"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*oz\b", re.I), "oz"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*cups?\b", re.I), "cup"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*tablespoons?\b", re.I), "tbsp"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*teaspoons?\b", re.I), "tsp"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*(g|grams?)\b", re.I), "g"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*(kg|kilograms?)\b", re.I), "kg"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*(ml|millilitres?|milliliters?)\b", re.I), "ml"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*(l|litres?|liters?)\b", re.I), "l"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*(quarts?|qt)\b", re.I), "quart"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*(pints?|pt)\b", re.I), "pint"),
    (re.compile(r"^\s*([\d./,¼½¾⅓⅔⅛\s-]+)\s*(gallons?|gal)\b", re.I), "gallon"),
]

FRAC = {
    "1/2": 0.5, "1/4": 0.25, "3/4": 0.75, "1/3": 0.3333, "2/3": 0.6667,
    "1/8": 0.125, "3/8": 0.375, "5/8": 0.625, "7/8": 0.875,
    "1/4": 0.25, "¼": 0.25, "½": 0.5, "¾": 0.75, "⅓": 0.3333,
    "⅔": 0.6667, "⅛": 0.125,
}

# conversion to the app's units: g / ml / ea
TO_G = {"lb": 453.6, "oz": 28.35}
TO_ML = {"cup": 240, "tbsp": 15, "tsp": 5, "quart": 946, "pint": 473,
         "gallon": 3785, "l": 1000}


def parse_qty(text):
    """Return (qty_in_app_units, unit) or (None, None)."""
    if not text:
        return None, None
    t = text.strip()
    for rx, unit in UNIT_MAP:
        m = rx.match(t)
        if not m:
            continue
        num = m.group(1).strip().replace(" ", "")
        # handle "1-1/2" and "1 1/2" and "1/2"
        val = None
        if "-" in num and "/" in num:
            whole, rest = num.split("-", 1)
            if rest in FRAC:
                val = float(whole) + FRAC[rest]
        if val is None and "/" in num:
            parts = num.split("/")
            try:
                val = float(parts[0]) / float(parts[1])
            except (ValueError, ZeroDivisionError):
                val = None
        if val is None:
            try:
                val = float(num)
            except ValueError:
                val = None
        if val is None:
            continue
        if unit in TO_G:
            return round(val * TO_G[unit], 1), "g"
        if unit in TO_ML:
            return round(val * TO_ML[unit], 1), "ml"
        return val, unit
    return None, None


# split "1 1/2 cups (300 g) white mustard seeds*, or any other color you like"
QTY_RX = re.compile(
    r"^\s*(?P<qty>to\s+)?"
    # the number: "2", "1/2", "2 1/2", "1.5"
    r"(?P<num>\d+(?:[./]\d+)?(?:\s+\d+[./]\d+)?)"
    # a unit, but only when it stands alone after the number:
    # "2 large eggplants" must not read as "2 l" (2 litres)
    r"(?P<unit>\s+(?:cups?|tbsp|tablespoons?|tsp|teaspoons?|pounds?|lbs?|"
    r"oz|ounces?|g|grams?|kg|ml|millilitres?|milliliters?|l|"
    r"litres?|liters?|quarts?|pints?|gallons?))?"
    r"\s*(?:\((?P<paren>[^)]*)\))?\s*"
    r"(?P<name>[A-Za-z0-9'’&()\-/,.\s]+?)\s*(?P<note>\*.*)?$")


def _unit_name(unit_txt):
    """Map a matched unit word to the app's unit vocabulary."""
    u = unit_txt.strip().lower()
    table = {
        "cup": "cup", "cups": "cup",
        "tbsp": "tbsp", "tablespoon": "tbsp", "tablespoons": "tbsp",
        "tsp": "tsp", "teaspoon": "tsp", "teaspoons": "tsp",
        "pound": "lb", "pounds": "lb", "lb": "lb", "lbs": "lb",
        "oz": "oz", "ounce": "oz", "ounces": "oz",
        "g": "g", "gram": "g", "grams": "g",
        "kg": "kg", "kilogram": "kg", "kilograms": "kg",
        "ml": "ml", "millilitre": "ml", "millilitres": "ml",
        "milliliter": "ml", "milliliters": "ml",
        "l": "l", "litre": "l", "litres": "l", "liter": "l", "liters": "l",
        "quart": "quart", "quarts": "quart",
        "pint": "pint", "pints": "pint",
        "gallon": "gallon", "gallons": "gallon",
    }
    return table.get(u, u)


def parse_ingredient_line(line):
    """Parse one ingredient line into (name, qty, unit, note)."""
    line = line.strip()
    if not line or line.lower() in ("ingredients:", "instructions:"):
        return None
    # strip a leading list marker
    line = re.sub(r"^[-*•]\s*", "", line)
    m = QTY_RX.match(line)
    if not m:
        # no quantity: treat as a pantry staple, qty None
        name = re.sub(r"\s+", " ", line).strip(" .")
        return (name, None, "ea", "") if name else None

    qty_txt = m.group("num")
    unit_txt = (m.group("unit") or "").strip()
    paren = m.group("paren") or ""
    name = re.sub(r"\s+", " ", m.group("name")).strip(" ,.")
    note = (m.group("note") or "").strip()

    qty, unit = parse_qty(qty_txt)
    if qty is not None and unit_txt:
        # the unit was matched separately, so use it
        u2, _ = parse_qty("1" + unit_txt)
        if u2 is not None:
            unit = _unit_name(unit_txt)
    if qty is None and paren:
        qty, unit = parse_qty(paren)
    if qty is None and paren:
        # "(300 g)" style only
        g = re.search(r"([\d.]+)\s*(g|kg|ml|l)\b", paren, re.I)
        if g:
            qty = float(g.group(1))
            unit = g.group(2).lower()
            if unit == "kg":
                qty, unit = qty * 1000, "g"
            if unit == "l":
                qty, unit = qty * 1000, "ml"
    if qty is None:
        # count of items: "3 eggs", "2 lemons"
        n = re.match(r"^(\d+)\s+(.+)$", line)
        if n:
            return n.group(2).strip(), int(n.group(1)), "ea", note
        return (name or line, None, "ea", note)
    return name, qty, unit, note


def clean_history(body):
    """Pull the prose history out of the page body."""
    t = body.replace("Watch the Video", "").strip()
    # the quoted source block starts at a lone "
    idx = t.find('"')
    if idx > 0:
        t = t[:idx].strip()
    # drop the trailing "source" attribution lines
    t = re.sub(r"\s*condiment.*$", "", t, flags=re.S)
    t = re.sub(r"\s*Max Miller\s*$", "", t).strip()
    t = re.sub(r"\s*https://www\.tastinghistory\.com\s*$", "", t).strip()
    t = re.sub(r"\s*Previous\s*$", "", t).strip()
    t = re.sub(r"\s*Next\s*$", "", t).strip()
    t = re.sub(r"\s*Travel with Tasting History\s*$", "", t).strip()
    t = re.sub(r"\s*Cookbook\s*$", "", t).strip()
    t = re.sub(r"\s*Episodes\s*$", "", t).strip()
    t = re.sub(r"\s*Recipes\s*$", "", t).strip()
    t = re.sub(r"\s*Ingredients\s*$", "", t).strip()
    t = re.sub(r"\s*Research\s*$", "", t).strip()
    t = re.sub(r"\s*Store\s*$", "", t).strip()
    t = re.sub(r"\s*Newsletter\s*$", "", t).strip()
    t = re.sub(r"\s*Contact\s*$", "", t).strip()
    t = re.sub(r"\s*Patreon\s*$", "", t).strip()
    t = re.sub(r"\s*Made with\s*$", "", t).strip()
    t = re.sub(r"\s*Squarespace\s*$", "", t).strip()
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t


def clean_instructions(text):
    """Split the instruction blob into steps, dropping the nav tail."""
    # cut the trailing nav junk
    for marker in ["\ncondiment", "\nside dish", "\nmain dish", "\ndessert",
                   "\ndrink", "\nsnack", "\nbreakfast", "\nlunch", "\ndinner",
                   "\nvegetarian", "\nMax Miller"]:
        i = text.find(marker)
        if i > 100:
            text = text[:i]
    text = text.replace("https://www.tastinghistory.com", "")
    # split on sentence-ish boundaries at numbered/bulleted lines
    steps = []
    for para in re.split(r"\n+", text):
        p = para.strip()
        if not p or len(p) < 8:
            continue
        p = re.sub(r"^\d+[.)]\s*", "", p)
        p = re.sub(r"^[-*•]\s*", "", p)
        # break very long paragraphs into sentences
        if len(p) > 320:
            sents = re.split(r"(?<=[.!?])\s+(?=[A-Z])", p)
            buf = ""
            for s in sents:
                if len(buf) + len(s) < 320:
                    buf = (buf + " " + s).strip()
                else:
                    if buf:
                        steps.append(buf)
                    buf = s
            if buf:
                steps.append(buf)
        else:
            steps.append(p)
    return [s for s in steps if len(s) > 10]


# ---- run the extraction
out = []
for slug, v in sorted(DATA.items()):
    title = (v.get("title") or "").replace(" &mdash; Tasting History", "").strip()
    if not title or title.startswith("&"):
        title = slug
    title = title.replace("&mdash;", "—").replace("&amp;", "&")
    title = re.sub(r"\s+", " ", title).strip()

    hist = clean_history(v.get("body", ""))
    if len(hist) < 120:
        print(f"  skip (thin history): {slug}")
        continue

    ing_blob = v.get("ing", "")
    # ingredients section is between "Ingredients:" and "Instructions:"
    m = re.search(r"Ingredients:\s*(.*?)\s*(?:Instructions:|Notes)", ing_blob, re.S)
    if not m:
        print(f"  skip (no ingredients block): {slug}")
        continue
    ing_text = m.group(1)

    ingredients = []
    for line in ing_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("see notes") or line.startswith("*"):
            continue
        parsed = parse_ingredient_line(line)
        if not parsed:
            continue
        name, qty, unit, note = parsed
        if not name or len(name) < 2:
            continue
        if len(name) > 70:
            name = name[:70].rsplit(" ", 1)[0]
        ingredients.append({
            "name": name,
            "qty": qty if qty is not None else 1,
            "unit": unit or "ea",
            "pantry": "",
            "note": (note or "").replace("*", "").strip()[:60],
        })

    if len(ingredients) < 2:
        print(f"  skip (too few ingredients): {slug}")
        continue

    method = clean_instructions(ing_blob.split("Instructions:")[-1]
                               if "Instructions:" in ing_blob else "")
    if len(method) < 3:
        print(f"  skip (too few steps): {slug}")
        continue

    era = era_for(v.get("period"), v.get("city"), title)

    out.append({
        "slug": slug,
        "title": title,
        "era": era,
        "year": v.get("period") or "",
        "region": v.get("city") or "",
        "source": f"Tasting History, '{title}' ({v.get('period') or 'n.d.'})",
        "source_url": f"https://www.tastinghistory.com/recipes/{slug}",
        "history": hist,
        "method": method,
        "ingredients": ingredients,
    })

print(f"\nExtracted {len(out)} recipes from {len(DATA)} pages.")
json.dump(out, open(os.path.join(BASE, "th_extracted.json"), "w"),
          ensure_ascii=False, indent=1)
by_era = {}
for r in out:
    by_era[r["era"]] = by_era.get(r["era"], 0) + 1
print("by era:", json.dumps(by_era, indent=1))
