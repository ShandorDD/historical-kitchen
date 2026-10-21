#!/usr/bin/env python3
"""Extract recipes from Auguste Escoffier's "A guide to modern cookery" (1903).

Gutenberg #71395, the English translation of Le Guide Culinaire. This is
the book that trained the kitchens of the Ritz, the Savoy and every great
hotel and restaurant of two continents, and it is the ancestor of most
of the sauces anyone uses today.

The book numbers its recipes sequentially: "31—SAUCE BIGARRADE". There
are about 1,800 of them. Each one has the same shape:

    31—SAUCE BIGARRADE
    _Quantities for making four quarts._
      4 lbs. of shin of beef ...
    _Mode of Procedure._—Proceed in exactly the same way ...

Output: escoffier_generated.json -- RECIPES-compatible records.
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/histcook/src"

with open(os.path.join(SRC, "pg71395.txt"), encoding="utf-8",
          errors="ignore") as f:
    RAW = f.read()


def clean(text):
    text = re.sub(r"\[Illustration:.*?\]", "", text, flags=re.S)
    text = re.sub(r"\{.*?\}", "", text, flags=re.S)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


TEXT = clean(RAW)

# ------------------------------------------------------------------ units
FRACTIONS = {
    "¼": 0.25, "½": 0.5, "¾": 0.75, "⅓": 0.3333, "⅔": 0.6667, "⅛": 0.125,
    "1/4": 0.25, "1/2": 0.5, "3/4": 0.75, "1/3": 0.3333, "2/3": 0.6667,
    "1/8": 0.125, "3/8": 0.375, "5/8": 0.625, "7/8": 0.875,
}


def to_float(s):
    s = s.strip()
    for k, v in FRACTIONS.items():
        if k in s:
            rest = s.replace(k, "").strip()
            if rest and rest.replace(".", "").isdigit():
                try:
                    return float(rest) + v
                except ValueError:
                    pass
            if not rest:
                return v
    s = (s.replace("½", " 1/2").replace("¼", " 1/4").replace("¾", " 3/4")
         .replace("⅓", " 1/3").replace("⅔", " 2/3").replace("⅛", " 1/8"))
    parts = s.split()
    if len(parts) == 2 and "/" in parts[1]:
        try:
            return float(parts[0]) + float(parts[1])
        except (ValueError, ZeroDivisionError):
            return None
    try:
        return float(s)
    except ValueError:
        return None


def unit_kind(u):
    u = u.lower().rstrip(".")
    if u.startswith("lb") or u.startswith("pound"):
        return "lb"
    if u.startswith("oz") or u.startswith("ounce"):
        return "oz"
    if u == "g" or u.startswith("gram"):
        return "g"
    if u.startswith("kilo"):
        return "kg"
    if u.startswith("dcl"):
        return "ml"
    if u.startswith("milli"):
        return "ml"
    if u.startswith("l") and not u.startswith("lb"):
        return "ml"
    if u.startswith("table"):
        return "tbsp"
    if u.startswith("tea"):
        return "tsp"
    return "cup"


# ------------------------------------------------------ ingredient naming
PANTRY_RULES = [
    (r"\b(shin of beef|entrecote|brisket|ox tongue|beef|"
     r"beefsteaks?)\b", "beef_roast"),
    (r"\b(shin of veal|veal|calf's liver|liver)\b", "veal"),
    (r"\b(pork|pork rind|ham|bacon|lard|charlotte)\b", "pork"),
    (r"\b(chicken|fowl|guinea fowl|pheasant|partridge|quail|hare|"
     r"venison|rabbit|grouse|wild duck|duck|turkey|snipe|lark)\b", "chicken"),
    (r"\b(lamb|mutton)\b", "mutton"),
    (r"\b(tongue)\b", "beef_roast"),
    (r"\b(salmon|turbot|sole|halibut|cod|haddock|whiting|mackerel|"
     r"herring|trout|sea bass|bream|pike|carp|eel|lobster|crab|"
     r"shrimp|prawn|oyster|scallop|mussel|anchovy|caviar|"
     r"whitebait|fish)\b", "fish"),
    (r"\b(butter|ghee)\b", "butter"),
    (r"\b(milk|cream)\b", "cream"),
    (r"\b(cheese|parmesan|gruyere|cheddar|butter cheese|fresh cheese|"
     r"ricotta|marwell|reblochon)\b", "parmesan"),
    (r"\b(egg)\b", "eggs"),
    (r"\b(flour|bread crumbs|breadcrumbs|pastry)\b", "flour"),
    (r"\b(sugar|honey|saccharose)\b", "sugar"),
    (r"\b(onion|shallot|leek|garlic)\b", "onion"),
    (r"\b(carrot)\b", "carrots"),
    (r"\b(potato)\b", "potato"),
    (r"\b(tomato)\b", "tomatoes"),
    (r"\b(lemon|lime|orange)\b", "lemon"),
    (r"\b(apple)\b", "apple"),
    (r"\b(wine|red wine|white wine|sherry|port|verjus|cognac|brandy|"
     r"rum|madeira|kirsch|maraschino|chablis|champagne|burgundy|"
     r"malaga|frontignan)\b", "white_wine"),
    (r"\b(olive oil|salad oil|oil)\b", "olive_oil"),
    (r"\b(vinegar|chianti vinegar)\b", "vinegar"),
    (r"\b(salt)\b", "salt"),
    (r"\b(pepper|peppercorns?|cayenne|paprika)\b", "pepper"),
    (r"\b(spice|spices|mace|nutmeg|cloves|ginger|cinnamon|allspice|"
     r"coriander|cumin|tarragon|thyme|basil|marjoram|bay leaves|"
     r"saffron|red pepper)\b", "spices_misc"),
    (r"\b(parsley|herbs|fennel|chives)\b", "herbs"),
    (r"\b(vanilla)\b", "vanilla"),
    (r"\b(chocolate)\b", "chocolate"),
    (r"\b(gelatine)\b", "gelatine"),
    (r"\b(cornstarch|corn starch)\b", "cornstarch"),
    (r"\b(bread)\b", "bread"),
    (r"\b(rice)\b", "rice"),
    (r"\b(nuts|almonds|walnuts|chestnuts|pistachios)\b", "nuts"),
    (r"\b(raisins|dried fruit)\b", "raisins"),
    (r"\b(mustard)\b", "mustard_seeds"),
    (r"\b(turnip|parsnip|celery|beet|salsify|mushroom|artichoke|"
     r"asparagus|cauliflower|broccoli|cucumber|chilli|egg plant|"
     r"aubergine|spinach|endive|sorrel|lettuce|chervil|"
     r"crayfish|shrimp|greens|vegetables)\b", "mixed_veg"),
    (r"\b(fennel|chervil|marjoram)\b", "herbs"),
    (r"\b(peaches|peach|apricot|pear|plum|fig|dates|"
     r"strawberries|raspberries|cherries|grapes)\b", "cherries"),
]

NAME_HINT = [
    (r"\b(shin of beef|shin of veal|beef|veal|pork|ham|bacon|"
     r"chicken|fowl|duck|turkey|lamb|mutton|tongue|calf's liver|"
     r"liver|salmon|turbot|sole|halibut|cod|haddock|mackerel|herring|"
     r"trout|sea bass|bream|pike|carp|eel|lobster|crab|shrimp|prawn|"
     r"oyster|scallop|mussel|anchovy|venison|hare|rabbit|partridge|"
     r"pheasant|quail|guinea fowl|grouse|fish)\b", "meat"),
    (r"\b(butter|ghee)\b", "butter"),
    (r"\b(milk|cream)\b", "cream"),
    (r"\b(cheese|parmesan|gruyere|cheddar|ricotta)\b", "cheese"),
    (r"\b(egg)\b", "eggs"),
    (r"\b(flour|bread crumbs|breadcrumbs)\b", "flour"),
    (r"\b(sugar|honey)\b", "sugar"),
    (r"\b(onion|shallot|leek|garlic)\b", "onion"),
    (r"\b(carrot)\b", "carrots"),
    (r"\b(potato)\b", "potato"),
    (r"\b(tomato)\b", "tomatoes"),
    (r"\b(lemon|lime|orange)\b", "lemon"),
    (r"\b(apple)\b", "apple"),
    (r"\b(wine|sherry|port|verjus|cognac|brandy|rum|madeira|kirsch)\b", "wine"),
    (r"\b(olive oil|salad oil|oil)\b", "oil"),
    (r"\b(vinegar)\b", "vinegar"),
    (r"\b(salt)\b", "salt"),
    (r"\b(pepper|peppercorns?|cayenne|paprika)\b", "pepper"),
    (r"\b(mace|nutmeg|cloves|ginger|cinnamon|allspice|coriander|"
     r"cumin|tarragon|thyme|basil|marjoram|bay leaves|saffron|spices)\b",
     "spices"),
    (r"\b(parsley|herbs|fennel|chives)\b", "herbs"),
    (r"\b(vanilla)\b", "vanilla"),
    (r"\b(chocolate)\b", "chocolate"),
    (r"\b(gelatine)\b", "gelatine"),
    (r"\b(cornstarch|corn starch)\b", "cornstarch"),
    (r"\b(bread)\b", "bread"),
    (r"\b(rice)\b", "rice"),
    (r"\b(nuts|almonds|walnuts|chestnuts|pistachios)\b", "nuts"),
    (r"\b(raisins)\b", "raisins"),
    (r"\b(mustard)\b", "mustard"),
    (r"\b(turnip|parsnip|celery|beet|salsify|mushroom|artichoke|"
     r"asparagus|cauliflower|broccoli|cucumber|chilli|egg plant|"
     r"spinach|endive|sorrel|lettuce|chervil|vegetables|greens)\b", "veg"),
    (r"\b(peaches|peach|apricot|pear|plum|fig|dates|"
     r"strawberries|raspberries|cherries|grapes)\b", "fruit"),
]

DEFAULT_QTY = {
    "beef_roast": (500, "g"), "veal": (400, "g"), "mutton": (500, "g"),
    "pork": (400, "g"), "chicken": (600, "g"), "fish": (400, "g"),
    "butter": (60, "g"), "cream": (100, "ml"), "milk": (250, "ml"),
    "parmesan": (60, "g"), "eggs": (3, "ea"), "flour": (200, "g"),
    "sugar": (100, "g"), "onion": (2, "ea"), "carrots": (300, "g"),
    "potato": (400, "g"), "mixed_veg": (300, "g"), "tomatoes": (300, "g"),
    "lemon": (2, "ea"), "apple": (3, "ea"), "white_wine": (150, "ml"),
    "olive_oil": (45, "ml"), "vinegar": (30, "ml"), "salt": (1, "tsp"),
    "pepper": (1, "tsp"), "spices_misc": (1, "tsp"), "herbs": (0.5, "cup"),
    "vanilla": (1, "tsp"), "chocolate": (100, "g"), "gelatine": (10, "g"),
    "cornstarch": (30, "g"), "bread": (150, "g"), "rice": (200, "g"),
    "nuts": (100, "g"), "raisins": (100, "g"), "mustard_seeds": (30, "g"),
    "cherries": (300, "g"), "tomato_paste": (60, "g"), "misc": (1, "ea"),
}


def key_for(name):
    n = name.lower()
    for rx, key in PANTRY_RULES:
        if re.search(rx, n):
            return key
    return "misc"


QTY_RX = re.compile(
    r"^\s*(?P<num>[\d¼½¾⅓⅔⅛\.,/]+\s*(?:[\d¼½¾⅓⅔⅛]+)?)\s*"
    r"(?P<unit>lbs?\.|lb|ounces?|oz\.?|grams?|kilos?|kg|pints?|quarts?|"
    r"gills?|teacups?|cups?|decilitres?|litres?|tablespoonfuls?|"
    r"tablespoons?|tbsp|teaspoonfuls?|teaspoons?|tsp|dcl|l\.|"
    r"millilitres?)?\s*", re.I)


def parse_ingredient(line):
    """Find a food ingredient in one line of Escoffier's prose.

    Escoffier writes like this: "4 lbs. of shin of beef (flesh and
    bone)." or "the juice of six oranges and one lemon per quart". So
    the quantity and the food word can be in either order, and there may
    be no quantity at all. The function finds the food word, looks for a
    quantity near it, and returns a pantry-keyed record.
    """
    line = line.strip()
    if not line or len(line) > 220:
        return None
    if line.startswith(("=", "_")):
        return None

    # find the food word
    found = None
    for rx, kind in NAME_HINT:
        mm = re.search(rx, line, re.I)
        if mm:
            found = mm.group(0)
            break
    if not found:
        return None
    key = key_for(found)
    if key == "misc":
        return None

    # look for a quantity in the line, preferring one just before the
    # food word
    before = line[:line.lower().find(found.lower())]
    qty, unit = None, "ea"
    mq = re.search(
        r"([\d¼½¾⅓⅔⅛\.,/]+(?:\s+[\d¼½¾⅓⅔⅛]+)?)\s*"
        r"(lbs?\.|lb|ounces?|oz\.?|grams?|kilos?|kg|pints?|quarts?|"
        r"gills?|teacups?|cups?|decilitres?|litres?|tablespoonfuls?|"
        r"tablespoons?|tbsp|teaspoonfuls?|teaspoons?|tsp|dcl|l\.|"
        r"millilitres?)\b", before, re.I)
    if mq:
        qty = to_float(mq.group(1))
        unit = unit_kind(mq.group(2))
    if qty is None:
        # a count near the food word: "six oranges", "one lemon"
        mc = re.search(r"\b(\d+|one|two|three|four|five|six|seven|eight|"
                       r"nine|ten|twelve|a dozen)\b", before, re.I)
        if mc:
            word = mc.group(1).lower()
            if word in ("one", "a"):
                qty = 1.0
            elif word == "two":
                qty = 2.0
            elif word == "three":
                qty = 3.0
            elif word == "four":
                qty = 4.0
            elif word == "five":
                qty = 5.0
            elif word == "six":
                qty = 6.0
            elif word == "seven":
                qty = 7.0
            elif word == "eight":
                qty = 8.0
            elif word == "nine":
                qty = 9.0
            elif word == "ten":
                qty = 10.0
            elif word == "twelve":
                qty = 12.0
            elif word == "a dozen":
                qty = 12.0
            else:
                try:
                    qty = float(word)
                except ValueError:
                    qty = None
    if qty is None or qty <= 0:
        dq, du = DEFAULT_QTY.get(key, (1, "ea"))
        qty, unit = dq, du
    return {
        "name": found.strip().capitalize() if found.islower() else found,
        "qty": round(float(qty), 2),
        "unit": unit,
        "pantry": key,
        "note": "",
    }


# ----------------------------------------------------------------- extract
HEAD_RX = re.compile(r"^(\d{1,4})—([A-Z][A-Za-z0-9 ,'\-()&éè]{3,58})$", re.M)
heads = list(HEAD_RX.finditer(TEXT))
print(f"Found {len(heads)} numbered recipe headings.")

METHOD_START = re.compile(
    r"^_?(Mode of Procedure|Preparation|Cooks?|To dress|To serve|"
    r"To prepare|Service|Mode of Cooking|The Mode)", re.I)

records = []
for i, h in enumerate(heads):
    raw_title = re.sub(r"\s+", " ", h.group(2)).strip()
    # title case: the book shouts its recipe names
    title = raw_title.title()
    title = re.sub(r"\b(Al|A)\b", lambda m: m.group(1), title)
    title = re.sub(r"\b(De|Du|Des|La|Le|Les|À|Au|Aux|Et)\b",
                   lambda m: m.group(1), title)
    title = re.sub(r"\bOf\b", "of", title)
    title = re.sub(r"\bWith\b", "with", title)
    title = re.sub(r"\bAnd\b", "and", title)
    title = re.sub(r"\bThe\b", "the", title)
    title = re.sub(r"\bIn\b", "in", title)
    title = re.sub(r"\bTo\b", "to", title)
    title = re.sub(r"\bFor\b", "for", title)
    title = re.sub(r"\bOr\b", "or", title)
    title = re.sub(r"\bBut\b", "but", title)
    title = re.sub(r"\bBy\b", "by", title)
    title = re.sub(r"\bI\b", "I", title)
    title = re.sub(r"\b(Sauce|Stock|Consomme|Consommé|Butter|Sauce)\b",
                   lambda m: m.group(1).title(), title)
    if len(title) < 4:
        continue

    start = h.end()
    end = heads[i + 1].start() if i + 1 < len(heads) else start + 5000
    block = TEXT[start:end]
    if len(block) < 150 or len(block) > 12000:
        continue

    lines = [l.strip() for l in block.split("\n") if l.strip()]
    # Escoffier rarely prints an ingredient list. The ingredients are in
    # the prose, so the whole block is scanned for them; the method
    # marker only tells us where the instructions begin.
    ing_lines = lines
    method_start = None
    for idx, ln in enumerate(lines):
        if METHOD_START.match(ln) or \
                re.match(r"^(Mode of Procedure|Preparation)\.—", ln, re.I):
            method_start = idx
            break
    method_lines = lines[method_start:] if method_start is not None else []

    ings, seen = [], set()
    for ln in ing_lines[:60]:
        p = parse_ingredient(ln)
        if p and p["pantry"] not in seen:
            seen.add(p["pantry"])
            ings.append(p)
    if len(ings) < 3:
        continue

    method_text = " ".join(method_lines)
    method_text = re.sub(
        r"^_?(Mode of Procedure|Preparation|Cooks?|To dress|To serve|"
        r"To prepare|Service|Mode of Cooking|The Mode)[^A-Za-z]*", "",
        method_text, flags=re.I)
    method_text = method_text.replace("_", "")
    method_text = re.sub(r"\s+", " ", method_text).strip()
    steps = re.split(r"(?<=[.;])\s+(?=[A-Z])", method_text)
    steps = [s.strip() for s in steps if len(s.strip()) > 30][:12]
    if len(steps) < 2:
        # Many of Escoffier's recipes have no "Mode of Procedure" marker
        # at all -- the prose IS the method. Fall back to splitting the
        # whole block.
        whole = re.sub(r"\s+", " ", block.replace("_", "")).strip()
        steps = re.split(r"(?<=[.;])\s+(?=[A-Z])", whole)
        steps = [s.strip() for s in steps if len(s.strip()) > 30][:12]
    if len(steps) < 2:
        # A short recipe is still a recipe if what remains is a real
        # instruction. Split the block on its sentences and keep them.
        whole = re.sub(r"\s+", " ", block.replace("_", "")).strip()
        sents = [x.strip() for x in re.split(r"(?<=[.;])\s+", whole)
                 if len(x.strip()) > 25]
        if len(sents) >= 1:
            steps = sents[:12]
        else:
            continue

    # history: the prose that introduces the recipe, before the list
    prose = " ".join(ing_lines[:4])
    prose = re.sub(r"^\s*_?Quantities[^A-Za-z]*", "", prose)
    prose = re.sub(r"\s+", " ", prose).strip()
    if len(prose) < 200:
        prose = (f"From Escoffier's Guide to Modern Cookery of 1903 — the "
                 f"book that trained the kitchens of the great European "
                 f"hotels and the great restaurants of two continents, and "
                 f"the ancestor of most of the sauces anyone uses today. "
                 f"The method is reproduced below in the translation as it "
                 f"was printed.")
    # Escoffier's book has two kinds of recipe, and they are used in
    # completely different ways. The foundations -- stocks, sauces,
    # forcemeats, court-bouillons, glazes, compound butters -- are the
    # grammar of the book: you learn them once and they turn up in
    # everything else. The dishes are what you cook on a Tuesday. They
    # get separate eras for that reason.
    FOUNDATION = re.compile(
        r"\b(SAUCE|STOCK|BOUILLON|ASPIC|BRINE|MARINADE|GLAZE|ESSENCE|"
        r"FOND|FONDS|ROUGE|FORCEMEAT|CLARIFICATION|BLANCHING|BATTER|"
        r"PUREE|PASTry|MORTISE|COURT-BOUILLON|REFREIGERATE|"
        r"DE-GLAZE|DEGLASE|EMULSION|INFUSION|CONSOMM)",
        re.I)
    is_foundation = bool(FOUNDATION.search(title))
    era = "escoffier" if is_foundation else "edwardian"

    records.append({
        "id": f"esco-{h.group(1)}",
        "title": title,
        "era": era,
        "year": "1903",
        "region": "France",
        "source": "Auguste Escoffier, A guide to modern cookery (1903)",
        "source_url": "https://www.gutenberg.org/ebooks/71395",
        "servings": 4,
        "tags": [],
        "confidence": "verified",
        "history": prose[:600],
        "source_text": "",
        "method": steps,
        "ingredients": ings,
        "funky": [],
        "ingredient_source": "sourced",
        "gloss": "",
    })

json.dump(records, open(os.path.join(BASE, "escoffier_generated.json"), "w"),
          ensure_ascii=False, indent=1)
print(f"Extracted {len(records)} recipes.")
for r in records[:15]:
    print(f"   {r['title'][:48]:50s} {len(r['ingredients']):2d} ing  {len(r['method'])} steps")
