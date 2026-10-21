#!/usr/bin/env python3
"""Turn the extracted regional recipes into full corpus records.

The sources are old cookbooks written in prose: "Cut beef into small
pieces.  Heat some dripping in a saucepan; add the meat, salt and
black pepper; cover and let stew half an hour."

We need three things the app can use:
  1. an ingredient list, with a quantity and a pantry key,
  2. method steps,
  3. a cuisine tag and an era.

The prose is broken into clauses.  Each clause is examined for a known
ingredient and a quantity.  The *sentence* stays whole as a method
step, so the user gets the source's own voice, while the ingredient
list is built clause by clause.  Where a clause names a food but gives
no number ("some parsley", "a pinch of nutmeg") we record it as
"to taste" rather than inventing a quantity.

Output: region_generated.json (records) ready for build.py.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "data"))

from pantry import PANTRY, ALIASES  # noqa: E402

RAW = os.path.join(BASE, "region_raw.json")

# ------------------------------------------------------------ era routing
def era_for(year):
    if year < 1900:
        return "victorian"
    if year < 1918:
        return "edwardian"
    if year < 1946:
        return "wartime"
    return "postwar"


# ---------------------------------------------------------- pantry rules
RULES = [
    (r"\b(corned beef|bully beef)\b", "corned_beef"),
    (r"\b(beef|steak|brisket|sirloin|shank|round of beef|ox|tongue|"
     r"short ribs?|flank)\b", "beef_roast"),
    (r"\b(veal|calf)\b", "veal"),
    (r"\b(lamb|mutton)\b", "mutton"),
    (r"\b(pork|ham|bacon|lard|ham hock|pork belly)\b", "pork"),
    (r"\b(chicken|fowl|hen|poultry|turkey|duck|goose|guinea fowl|"
     r"guinea|pheasant|partridge|quail)\b", "chicken"),
    (r"\b(sausage)\b", "sausage"),
    (r"\b(egg|eggs|yolk|whites)\b", "eggs"),
    (r"\b(liver|brains?|kidney|offal)\b", "beef_roast"),
    (r"\b(smoked roe|smoked fish|caviar|caviare|roe|anchov|"
     r"salmon|trout|herring|mackerel|carp|pike|sole|cod|halibut|"
     r"perch|bream|eel|shad|white fish|pike|perch|plaice|haddock|"
     r"sardine|halibut|mussel|oyster)\b", "fish"),
    (r"\b(butter|ghee|drippings?)\b", "butter"),
    (r"\b(milk|cream|sour cream|smetana)\b", "cream"),
    (r"\b(parmesan|parmigiano|cheddar|ricotta|feta|cheese)\b", "parmesan"),
    (r"\bhoney\b", "honey"),
    (r"\b(molasses|treacle|syrup)\b", "molasses"),
    (r"\b(onion|onions|shallot|shallots|leek|garlic)\b", "onion"),
    (r"\b(carrot|carrots)\b", "carrots"),
    (r"\b(potato|potatoes)\b", "potato"),
    (r"\bcelery\b", "celery"),
    (r"\b(cabbage|cauliflower|brussels sprouts|kale)\b", "cabbage"),
    (r"\b(tomato|tomatoes)\b", "tomatoes"),
    (r"\b(paprika|paprikas)\b", "paprika"),
    (r"\b(chile|chili|chilli|red pepper|black pepper|white pepper|"
     r"peppercorns?|pepper)\b", "paprika"),
    (r"\b(beans?|haricot|lentils?|chickpeas?|peas|pea)\b", "beans"),
    (r"\b(squash|pumpkin|gourd|marrow)\b", "squash"),
    (r"\b(beetroot|beets|beet)\b", "beets"),
    (r"\b(apples?|pomme)\b", "apple"),
    (r"\b(lemon|lime|orange|citron)\b", "lemon"),
    (r"\b(cherries|cherry)\b", "cherries"),
    (r"\b(dates?)\b", "dates"),
    (r"\b(raisins?|currants?)\b", "raisins"),
    (r"\b(olives?|olive oil)\b", "olive_oil"),
    (r"\b(mushrooms?)\b", "mushrooms"),
    (r"\b(spinach|greens|lettuce|watercress)\b", "spinach"),
    (r"\b(asparagus|artichokes?|broccoli|cucumber|radish|parsnip|"
     r"turnips?|salsify|okra|aubergine|eggplant|celery root|"
     r"celery roots)\b", "mixed_veg"),
    (r"\b(corn|maize|cornmeal|polenta|oatmeal|oats|barley)\b", "cornmeal"),
    (r"\b(herbs?|parsley|thyme|rosemary|sage|basil|mint|dill|"
     r"marjoram|oregano|tarragon|coriander|bay leaf|bay leaves|"
     r"chervil|savory)\b", "herbs"),
    (r"\bvanilla\b", "vanilla"),
    (r"\b(breadcrumbs?|bread crumbs|pastry)\b", "flour"),
    (r"\b(flour)\b", "flour"),
    (r"\b(dough)\b", "flour"),
    (r"\brice\b", "rice"),
    (r"\b(brown sugar|caster sugar|confectioner(?:'s)? sugar|sugar)\b",
     "sugar"),
    (r"\b(starch|cornstarch)\b", "cornstarch"),
    (r"\b(baking powder|baking soda|yeast)\b", "baking_powder"),
    (r"\b(nuts?|almonds?|walnuts?|pistachios?|hazelnuts?|"
     r"pine nuts?|cashews?)\b", "nuts"),
    (r"\b(chocolate|cocoa)\b", "chocolate"),
    (r"\bcoconut\b", "coconut"),
    (r"\b(tea|coffee)\b", "tea"),
    (r"\b(wine|vermouth|brandy|rum|whiskey|whisky|gin|beer|ale|cider|"
     r"port|sherry|burgundy|claret|cognac|kirsch|calvados|champagne)\b",
     "white_wine"),
    (r"\b(wine vinegar)\b", "white_vinegar"),
    (r"\bvinegar\b", "vinegar"),
    (r"\bsalt\b", "salt"),
    (r"\bcinnamon\b", "cinnamon"),
    (r"\b(nutmeg|mace)\b", "nutmeg"),
    (r"\bcloves\b", "cloves"),
    (r"\bginger\b", "ginger"),
    (r"\b(allspice|cumin|coriander seed|cardamom|turmeric|mustard|"
     r"saffron|spice)\b", "spices_misc"),
    (r"\b(water|stock|broth|consomme)\b", "broth"),
    (r"\bsuet\b", "lard"),
    (r"\b(macaroni|spaghetti|noodles)\b", "pasta"),
    (r"\b(gelatine|gelatin)\b", "gelatine"),
    (r"\b(bread|toast)\b", "bread"),
    (r"\b(wheat|biscuits?)\b", "flour"),
]
COMPILED = [(re.compile(p, re.I), k) for p, k in RULES]
# Words that mark a clause as pure instruction, not an ingredient list.
VERB_RE = re.compile(
    r"\b(?:add|stir|cook|boil|simmer|fry|bake|roast|grill|season|mix|"
    r"combine|place|cover|remove|heat|take|have|make|prepare|beat|"
    r"whisk|strain|drain|rub|roll|sprinkle|scatter|chop|mince|slice|"
    r"peel|wash|dust|grease|garnish|pour|fill|divide|serve|let|mix|"
    r"melt|cream|fold|rub|knead|shape|form|set|turn|reduce|season|"
    r"arrange|spoon|pour|put|let)\b", re.I)

# Words that mark a clause as a heading or instruction only.
JUNK_CLAUSE = re.compile(
    r"^(?:serves?|serve|let|add|put|stir|cook|boil|simmer|fry|bake|"
    r"roast|grill|season|mix|combine|place|cover|remove|heat|take|"
    r"have|make|prepare|beat|whisk|strain|drain|rub|roll|sprinkle|"
    r"scatter|chop|mince|slice|peel|wash|dust|grease|garnish|pour|"
    r"fill|divide|melt|fold|knead|shape|arrange|to serve|for the|"
    r"for serving|for garnish)\b", re.I)

NUM_WORDS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "dozen": 12, "half": 0.5, "quarter": 0.25,
}
FRACTIONS = {"1/2": 0.5, "1/3": 0.333, "2/3": 0.667, "1/4": 0.25,
             "3/4": 0.75, "1/8": 0.125, "1/16": 0.0625, "2/4": 0.5}

UNITS = [
    (r"tablespoonfuls?f?ull", "tbsp"), (r"tablespoons?", "tbsp"),
    (r"teaspoonfuls?f?ull", "tsp"), (r"teaspoons?", "tsp"),
    (r"\bcups?\b", "cup"), (r"\bpints?\b", "pint"),
    (r"\bquarts?\b", "quart"), (r"\bgills?\b", "gill"),
    (r"\bpounds?\b", "lb"), (r"\blbs?\b", "lb"),
    (r"\bounces?\b", "oz"), (r"\boz\b", "oz"),
    (r"\bdozens?\b", "dozen"), (r"\bcloves\b", "clove"),
    (r"\bsprigs?\b", "sprig"), (r"\bsticks?\b", "stick"),
    (r"\bheads?\b", "head"), (r"\bbunch(?:es)?\b", "bunch"),
    (r"\bpecks?\b", "peck"), (r"\bbarrels?\b", "barrel"),
    (r"\bdashes?\b", "dash"), (r"\bhandfuls?\b", "handful"),
    (r"\bpackets?\b", "packet"), (r"\bjars?\b", "jar"),
    (r"\bcans?\b", "can"), (r"\bpackages?\b", "package"),
    (r"\bmedium\b", "ea"), (r"\blarge\b", "ea"), (r"\bsmall\b", "ea"),
]
UNIT_RE = re.compile("|".join(p for p, _ in UNITS), re.I)
UNIT_MAP = [(re.compile("^" + p + "$", re.I), u) for p, u in UNITS]

QTY_RE = re.compile(
    r"(?P<q>\d+(?:\s*/\s*\d+)?(?:\s*-\s*\d+(?:\s*/\s*\d+)?)?|"
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
    r"twelve|dozen|half|quarter)\b)", re.I)

# a bare "salt", "pepper", "sugar" is seasoning, not a measured ingredient
SEASONING = {"salt", "paprika", "pepper", "spices_misc"}


def qty_value(s):
    s = s.strip().lower()
    if s in NUM_WORDS:
        return NUM_WORDS[s]
    s = s.replace(" ", "")
    if s in FRACTIONS:
        return FRACTIONS[s]
    if "/" in s:
        try:
            a, b = s.split("/")
            return float(a) / float(b)
        except Exception:
            return None
    if "-" in s:
        try:
            a, b = s.split("-")
            return (float(a) + float(b)) / 2
        except Exception:
            return None
    try:
        return float(s)
    except Exception:
        return None


def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\b(pkg|lbs|oz|approx|etc|tsp|tbsp)\.", r"\1<DOT>", text)
    parts = re.split(r"(?<=[.;:])\s+(?=[A-Z0-9])", text)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def split_clauses(sent):
    """Break a sentence into the fragments that could each name a food."""
    s = re.sub(r"\s+", " ", sent).strip()
    # protect decimals and abbreviations
    s = re.sub(r"(\d+)\.(\d+)", r"\1<DOT>\2", s)
    parts = re.split(r"\s*[;,]\s*|\s+and\s+|\s+with\s+", s)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def find_pantry(name):
    for pat, key in COMPILED:
        if pat.search(name):
            if key in PANTRY or key in ALIASES:
                return key
    return None


def find_pantry_span(name):
    """Return (key, start, end) for the first matching pantry rule."""
    for pat, key in COMPILED:
        m = pat.search(name)
        if m and (key in PANTRY or key in ALIASES):
            return key, m.start(), m.end()
    return None, -1, -1


# The canonical display name for a pantry key.  When the clause is a
# garbled fragment we fall back to this, which is much better than
# showing the user "Heat some dripping in a saucepan" as an ingredient.
CANONICAL = {
    "beef_roast": "Beef", "veal": "Veal", "mutton": "Mutton",
    "pork": "Pork", "chicken": "Chicken", "sausage": "Sausage",
    "corned_beef": "Corned beef", "eggs": "Eggs", "fish": "Fish",
    "butter": "Butter", "cream": "Cream or sour cream",
    "parmesan": "Cheese", "honey": "Honey", "molasses": "Molasses",
    "onion": "Onion or garlic", "carrots": "Carrots",
    "potato": "Potatoes", "celery": "Celery", "cabbage": "Cabbage",
    "tomatoes": "Tomatoes", "paprika": "Paprika and pepper",
    "beans": "Beans or lentils", "squash": "Squash or pumpkin",
    "beets": "Beetroot", "apple": "Apple", "lemon": "Lemon or citrus",
    "cherries": "Cherries", "dates": "Dates", "raisins": "Raisins",
    "olive_oil": "Olive oil", "mushrooms": "Mushrooms",
    "spinach": "Spinach or greens", "mixed_veg": "Vegetables",
    "cornmeal": "Cornmeal or oats", "herbs": "Herbs",
    "vanilla": "Vanilla", "flour": "Flour", "rice": "Rice",
    "sugar": "Sugar", "cornstarch": "Starch", "baking_powder": "Yeast",
    "nuts": "Nuts", "chocolate": "Chocolate", "coconut": "Coconut",
    "tea": "Tea or coffee", "white_wine": "Wine or spirits",
    "white_vinegar": "Vinegar", "vinegar": "Vinegar", "salt": "Salt",
    "cinnamon": "Cinnamon", "nutmeg": "Nutmeg or mace",
    "cloves": "Cloves", "ginger": "Ginger",
    "spices_misc": "Mixed spices", "broth": "Stock or water",
    "lard": "Lard or suet", "pasta": "Pasta or noodles",
    "gelatine": "Gelatine", "bread": "Bread", "brandy": "Brandy",
    "sherry": "Sherry", "red_wine": "Red wine",
}

# Adjectives that legitimately travel with a food name.
MODIFIERS = {
    "green", "red", "white", "brown", "black", "yellow", "sour", "smoked",
    "dried", "fresh", "ripe", "large", "small", "medium", "sweet", "lean",
    "ripe", "boiled", "cooked", "raw", "withered", "pickled", "canned",
    "browned", "chopped", "minced", "grated", "melted", "soft", "stale",
    "whole", "boneless", "skinless", "thick", "thin", "new", "old",
}

# Words that must never appear in an ingredient name.
BAD_NAME_WORDS = re.compile(
    r"\b(?:heat|add|stir|cook|boil|simmer|fry|bake|roast|grill|season|"
    r"mix|combine|place|cover|remove|take|have|make|prepare|beat|"
    r"whisk|strain|drain|rub|roll|sprinkle|scatter|chop|mince|slice|"
    r"peel|wash|dust|grease|garnish|pour|fill|divide|melt|fold|knead|"
    r"shape|arrange|serve|serving|serves|let|put|seasoned|into|"
    r"saucepan|pan|pot|bowl|dish|plate|kettle|oven|fire|heat|slowly|"
    r"until|together|then|well|very|good|best|like|such|more|less|"
    r"enough|sufficient|about|approximately|with|"
    r"the|a|an|of|for|and|or|in|on|to|at|from|is|are|be|it|its|"
    r"this|that|these|those|other|last|first|next|one|hour|half|"
    r"quarter|all|both|each|every|some|many|much|more|most|very)\b",
    re.I)

# Words that can follow a food name to make a fuller label.
TAIL_WORDS = re.compile(
    r"^(?:pieces?|chunks?|slices?|cubes?|dices?|sticks?|stalks?|"
    r"leaves?|cloves?|sprigs?|heads?|roots?|squares?|rounds?|"
    r"grains?|tablespoons?|teaspoons?|cups?|pounds?|ounces?)\b",
    re.I)


def clean_name(raw, key, span=None):
    """Turn a clause fragment into a readable ingredient name.

    The most reliable signal is the food word itself, so we use the
    matched text and, where there is a clear adjective in front of it,
    keep that too.  "5 medium-sized beets" -> "Beets";  "1 large onion
    sliced thin" -> "Large onion".  If the match is unusable we fall
    back to the canonical label for the pantry key.
    """
    canon = CANONICAL.get(key, key.replace("_", " "))

    if span is not None:
        _, s, e = span
        if s >= 0 and e <= len(raw):
            word = raw[s:e].strip(" .,:;-")
            if word and len(word) <= 40:
                # look for an adjective just before
                before = raw[max(0, s - 20):s]
                bw = [w.strip(" .,:;-").lower() for w in before.split()]
                bw = [w for w in bw if w]
                label = word
                if bw and bw[-1] in MODIFIERS:
                    label = f"{bw[-1]} {word}"
                return label[0].upper() + label[1:]

    n = " ".join(raw.split())
    n = BAD_NAME_WORDS.sub(" ", n)
    n = re.sub(r"\s+", " ", n).strip(" .,:;-()")
    n = re.sub(r"^(?:a|an|the|some|and|of)\s+", "", n, flags=re.I).strip()
    if not n or len(n) < 2:
        return canon
    if BAD_NAME_WORDS.search(n) and len(n.split()) > 2:
        return canon
    if len(n) > 40:
        return canon
    n = re.sub(r"^\d+(?:\s*/\s*\d+)?\s*", "", n).strip()
    if not n:
        return canon
    return n[0].upper() + n[1:]


def parse_clause(clause):
    """Try to turn one clause into an ingredient record."""
    c = clause.strip().rstrip(".;,")
    if not c or len(c) > 120:
        return None
    # Strip a leading instruction verb and look at what follows it.
    # "add 3 potatoes cut into dice pieces" -> "3 potatoes cut into dice"
    c2 = re.sub(r"^\s*(?:add|put|stir in|beat in|beat|sprinkle|scatter|"
                r"throw in|sear|fry|boil|bake|use|season with|season|"
                r"cover|drain|serve)\s+", "", c, flags=re.I)
    c2 = c2.strip() or c

    key, sp_s, sp_e = find_pantry_span(c2)
    if not key:
        return None

    unit = "ea"
    qty = None
    um = UNIT_RE.search(c2)
    if um:
        for pat, u in UNIT_MAP:
            if pat.match(um.group(0)):
                unit = u
                break
        # the number usually sits just before the unit
        pre = c2[:um.start()]
        pm = QTY_RE.search(pre)
        if pm:
            v = qty_value(pm.group("q"))
            if v is not None:
                qty = v
    if qty is None:
        # "a pinch of nutmeg", "some parsley", "salt to taste"
        pm = QTY_RE.search(c2)
        if pm:
            v = qty_value(pm.group("q"))
            if v is not None:
                qty = v
    if qty is None:
        if re.search(r"\b(some|a little|a few|a pinch|pinch|sufficient|"
                     r"as needed|to taste|enough|handful)\b", c2, re.I):
            qty = 1
            unit = "to taste"
        else:
            return None

    # build the display name: strip quantity, unit, and prep words
    name = c2
    if um:
        name = name.replace(um.group(0), " ", 1)
    name = QTY_RE.sub(" ", name, count=1)
    name = re.sub(
        r"\b(?:of|for the|for|fresh|dried|ground|chopped|minced|"
        r"sliced|diced|cut|well|very|small|medium|large|big|to taste|"
        r"whole|cold|warm|hot|raw|ripe|fine|finely|coarsely|thinly|"
        r"pieces?|chunks?|slices?|leaves?|stalks?|sprigs?|cloves?)\b",
        " ", name, flags=re.I)
    name = re.sub(r"\s+", " ", name).strip(" .,:;-")
    name = re.sub(r"^(?:a|an|the|some|and)\s+", "", name, flags=re.I).strip()
    if not name or len(name) < 2:
        return None
    if len(name) > 55:
        name = name[:55].rstrip()
    # A clause like "cut into dice pieces" carries no food name.
    if len(name.split()) < 1:
        return None
    return {"name": clean_name(name, key, find_pantry_span(name)),
            "qty": qty, "unit": unit, "pantry": key, "note": ""}


def build_history(r, ings, steps):
    """A short provenance note for each dish, written from the source."""
    who = r["source_author"]
    book = r["source_title"]
    yr = r["source_year"]
    cui = r["cuisine"]
    lead = {
        "Hungarian": "Hungarian cooking at the turn of the century was "
                     "built on paprika and fat, and the dishes here are "
                     "the ones that crossed the border with the "
                     "touring Austro-Hungarian cooks and stuck.",
        "Russian": "Russian cookery of this period leans on the whole "
                   "fish, the roast, and the sour-sweet soup that made "
                   "its way west as borscht.",
        "Polish": "Polish cooking of the old manor houses prized the "
                  "roast joint and the sharp, vinegared vegetables that "
                  "accompanied it.",
        "German": "German cooking of this period was the reference "
                  "cookery of the middle European kitchen, and its "
                  "sauces and roasts were copied everywhere.",
        "Jewish (Ashkenazi)": "Ashkenazi cooking of the early twentieth "
                              "century, written for a kitchen that was "
                              "still cooking for a holiday table every "
                              "week of the year.",
        "Slavic / Eastern European": "From the eastern European "
                                     "cookery that fed the great "
                                     "migration of the 1880s and 1890s.",
        "Turkish / Ottoman": "Ottoman and Turkish cooking as it reached "
                             "Western kitchens in the late nineteenth "
                             "century, usually through the embassy "
                             "table and the shipping trade.",
        "Greek": "Greek island and mainland cooking as the Mediterranean "
                 "trade brought it north.",
        "Italian": "Italian cooking as it was being written down in "
                   "English for the first time, and often not quite "
                   "right.",
        "French": "French provincial cookery of the period, in the "
                  "plain style that the English kitchen copied and then "
                  "sometimes got wrong.",
    }.get(cui, "From a cookery book of the period.")
    return (f"{lead} This recipe comes from {book} ({yr}), by {who}. "
            f"The book gives it in the plain prose that cookbooks used "
            f"before they learned to print ingredients as a list.")


def main():
    raw = json.load(open(RAW))
    out = []
    seen = set()

    for r in raw:
        title = r["title"].strip()
        if title.isupper():
            title = title.title()
        tkey = " ".join(title.lower().split())
        if tkey in seen:
            continue

        sents = split_sentences(r["body"])
        ings, seen_ing = [], set()
        for sent in sents:
            for clause in split_clauses(sent):
                ing = parse_clause(clause)
                if not ing:
                    continue
                sig = (ing["pantry"], ing["name"].lower())
                if sig in seen_ing:
                    continue
                seen_ing.add(sig)
                ings.append(ing)

        if len(ings) < 2:
            continue

        # Method: the source's own sentences, lightly tidied.
        steps = []
        for s in sents:
            s = s.strip()
            if len(s) < 15:
                continue
            steps.append(s[0].upper() + s[1:] if s else s)
        if not steps:
            continue
        if len(steps) > 14:
            steps = steps[:14]

        yr = r["source_year"]
        era = era_for(yr)

        seen.add(tkey)
        # The method already carries the source's own prose, so we do
        # not also ship it as a separate quote.  And the history note
        # is the same shape for every dish in a book, so it is kept
        # short -- the source line above the card does the citing.
        out.append({
            "id": f"reg-{r['source_id']}-{abs(hash(tkey)) % 10**8}",
            "title": title,
            "era": era,
            "year": str(yr),
            "region": r["cuisine"],
            "source": f"{r['source_title']} ({yr}), {r['source_author']}",
            "source_url": r["source_url"],
            "servings": 4,
            "tags": [r["cuisine"].lower().split(" ")[0]] +
                   (["stew"] if "stew" in title.lower() else
                    ["soup"] if "soup" in title.lower() else
                    ["dessert"] if any(w in title.lower() for w in
                                       ("cake", "pudding", "roll", "torte"))
                    else ["traditional"]),
            "confidence": "sourced",
            "history": build_history(r, ings, steps),
            "source_text": "",
            "method": steps,
            "ingredients": ings,
            "funky": [],
            "ingredient_source": "sourced",
            "gloss": "",
        })

    with open(os.path.join(BASE, "region_generated.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    from collections import Counter
    print(f"Converted {len(out)} regional recipes")
    for k, v in Counter(x["region"] for x in out).most_common():
        print(f"  {v:>5}  {k}")
    print("  ingredients total:",
          sum(len(x["ingredients"]) for x in out))


if __name__ == "__main__":
    main()
