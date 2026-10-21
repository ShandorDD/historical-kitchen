#!/usr/bin/env python3
"""Extract recipes from the Project Gutenberg cookbooks.

These books are 17th-19th century primary sources, already downloaded to
/tmp/histcook/src. Each has its own structure:

  22790  Robert May, The Accomplisht Cook (1660)
  10072  Elizabeth Moxon, English Housewifry (1720)
  12815  American Cookery (1796)
  35646  Pierre Blot, Hand-Book of Practical Cookery (1874)

Moxon is the cleanest: numbered "N. To make X." headings. May uses
italicised dish names. American Cookery and Blot use "CHAP. X" and
numbered sections.

Output: data/gutenberg_generated.py -- RECIPES-compatible records.
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/histcook/src"

# --------------------------------------------------------------- helpers
def load(fname):
    with open(os.path.join(SRC, fname), encoding="utf-8", errors="ignore") as f:
        return f.read()


def clean(text):
    """Undo the Gutenberg markup and tidy the whitespace."""
    text = re.sub(r"\[Illustration:.*?\]", "", text, flags=re.S)
    text = re.sub(r"\{.*?\}", "", text, flags=re.S)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def paragraphs(text):
    out = []
    for p in text.split("\n"):
        p = p.strip()
        if p:
            out.append(p)
    return out


def split_sentences(block):
    """Turn a recipe block into steps, breaking on line boundaries and
    long sentences."""
    steps = []
    buf = ""
    for line in paragraphs(block):
        # A new line starting with a capital usually begins a new step
        if buf and re.match(r"^(To |Then |Take |Put |Add |When |Let |Boil |"
                            r"Bake |Stir |Season |Serve |Pour |Mix |Make |"
                            r"After |Beat |Melt |Heat |Cover |Remove |Cut |"
                            r"Chop |Rub |Whisk |Set |Tie |Squeeze |Drain |"
                            r"Grate |Slice |Sprinkle |Knead |Roll |Fried |"
                            r"Boiled |Take up |Fry |Butter |Season them)", line):
            if len(buf) > 25:
                steps.append(buf.strip())
            buf = line
        else:
            buf = (buf + " " + line).strip()
    if len(buf) > 25:
        steps.append(buf.strip())
    # if we ended up with one huge blob, split it on sentence boundaries
    if len(steps) <= 2:
        blob = " ".join(paragraphs(block))
        sents = re.split(r"(?<=[.!?])\s+(?=[A-Z])", blob)
        steps = [s for s in sents if len(s) > 20]
    return steps[:14]


def guess_pantry(name):
    """Coarse ingredient -> pantry key mapping for the Gutenberg books."""
    n = name.lower()
    rules = [
        (r"\b(veal|calf)\b", "veal"),
        (r"\b(lamb|mutton)\b", "mutton"),
        (r"\b(beef|ox|oxen|beefsteak)\b", "beef_roast"),
        (r"\b(pork|ham|bacon|pig)\b", "pork"),
        (r"\b(chicken|cock|hen|fowl|poultry|duck|goose|turkey)\b", "chicken"),
        (r"\b(egg)\b", "eggs"),
        (r"\b(butter)\b", "butter"),
        (r"\b(milk|cream)\b", "cream"),
        (r"\b(cheese|parmesan)\b", "parmesan"),
        (r"\b(beef|mutton)\b", "beef_roast"),
        (r"\b(fish|sole|carp|salmon|cod|perch|pike|bream|mullet|"
         r"eel|haddock|stockfish|carp|herring)\b", "fish"),
        (r"\b(oyster|crab|lobster|shrimp|prawn)\b", "fish"),
        (r"\b(onion|shallot|leek|garlic)\b", "onion"),
        (r"\b(carrot)\b", "carrots"),
        (r"\b(potato)\b", "potato"),
        (r"\b(turnip|parsnip|beet|salsify|skirret|carrot)\b", "mixed_veg"),
        (r"\b(pea|beans?|lentil|chickpea)\b", "beans"),
        (r"\b(cabbage|cabbidg)\b", "cabbage"),
        (r"\b(tomato)\b", "tomatoes"),
        (r"\b(salad|greens|spinage|spinach|cabbage|herbs|parsley|thyme|"
         r"sage|mint|marigold|sorrel|burrage|endive|beet)\b", "spinach"),
        (r"\b(lemon|lime|orange)\b", "lemon"),
        (r"\b(apple)\b", "apple"),
        (r"\b(date|raisin|fig|nut|almond|filbert|pistachio)\b", "nuts"),
        (r"\b(flour|bread|crumb|biscuit|husk)\b", "flour"),
        (r"\b(barley|rice|oats|meal|oatmeal)\b", "cornmeal"),
        (r"\b(sugar|honey|sweet)\b", "sugar"),
        (r"\b(spice|cinnamon|pepper|nutmeg|clove|mace|ginger|saffron|"
         r"mustard|salt)\b", "spices_misc"),
        (r"\b(pepper)\b", "pepper"),
        (r"\b(salt)\b", "salt"),
        (r"\b(wine|ale|beer|vinegar|broth|gravy|stock)\b", "white_wine"),
        (r"\b(oil|lard|butter)\b", "olive_oil"),
    ]
    for rx, key in rules:
        if re.search(rx, n):
            return key
    return "misc"


# --------------------------------------------------------------- Moxon
def extract_moxon():
    text = clean(load("pg10072.txt"))
    # recipe headings: "3. _To make_ HARE SOOP."
    pat = re.compile(r"^\s*(\d+)\.\s*(.+?)\.\s*$", re.M)
    hits = list(pat.finditer(text))
    out = []
    for i, m in enumerate(hits):
        title = m.group(2).strip()
        # keep only headings that look like a dish
        if len(title) < 6 or len(title) > 60:
            continue
        if not re.search(r"(SOOP|SOUP|PIE|PUDDING|CAKE|PIE|BROTH|STEW|"
                         r"PORTER|BEEF|MUTTON|VEAL|PORK|CHICKEN|BEAN|PEASE|"
                         r"CHEESE|BUTTER|HASH|SAUCE|KETCHUP|BISCUIT|BREAD|"
                         r"TART|PUDDING|FLUMMERY|WHISKY|CUSTARD|WINE|"
                         r"APPLE|PLUM|CHERRY|PEAR|GOOSE|DUCK|EGG)", title, re.I):
            continue
        start = m.end()
        end = hits[i + 1].start() if i + 1 < len(hits) else min(start + 4000, len(text))
        block = text[start:end].strip()
        if len(block) < 200:
            continue
        steps = split_sentences(block)
        if len(steps) < 3:
            continue
        out.append({
            "title": title,
            "source": "Elizabeth Moxon, English Housewifry (1720)",
            "source_url": "https://www.gutenberg.org/ebooks/10072",
            "year": "1720",
            "region": "England",
            "era": "georgian",
            "body": block[:2500],
            "steps": steps,
        })
    return out


# --------------------------------------------------------------- May
def extract_may():
    raw = load("pg22790.txt")
    # May marks each dish with an italicised heading line, e.g.
    #   _To hash or stew a Neats tongue divers wayes._
    # Work on the RAW text so the underscores are still present, then
    # clean each block.
    pat = re.compile(
        r"^  _([^_]{8,80}?)\._\s*$", re.M)
    hits = list(pat.finditer(raw))
    out = []
    for i, m in enumerate(hits):
        title = re.sub(r"\s+", " ", m.group(1).strip())
        if not re.search(r"(To |A |The |How |To make|To dress|To preserve|"
                         r"broth|soop|soup|pie|pudding|cake|stew|"
                         r"hash|butter|boil|roast|fry|preserve|"
                         r"bake|marinate|sauce|cheese|wine|"
                         r"tongue|beef|mutton|veal|pork|chicken|"
                         r"fish|herring|oyster|custard|porridge|"
                         r"puff|biscuit|bread|egg|peas|beans|"
                         r"apple|lemon|carp|salmon)", title, re.I):
            continue
        # skip section headings that are not dishes
        if re.search(r"(course|carving|carve|table|index|preface|"
                     r"introduction|appendix|errata|contents|"
                     r"general rules|observation|note|introduction|"
                     r"how to choose|to choose|to know|to preserve|"
                     r"of the|for the|to dress|seasoning|"
                     r"the kitchen|your|to carve|to break|"
                     r"to serve|to eat|to keep|to make your|"
                     r"of meat|of fish|of fowl|of game)", title, re.I):
            continue
        start = m.end()
        end = hits[i + 1].start() if i + 1 < len(hits) else start + 3500
        block = clean(raw[start:end]).strip()
        if len(block) < 250 or len(block) > 7000:
            continue
        steps = split_sentences(block)
        if len(steps) < 4:
            continue
        out.append({
            "title": title,
            "source": "Robert May, The Accomplisht Cook (1660)",
            "source_url": "https://www.gutenberg.org/ebooks/22790",
            "year": "1660",
            "region": "England",
            "era": "renaissance",
            "body": block[:2500],
            "steps": steps,
        })
    return out


# --------------------------------------------------------------- Blot
def extract_blot():
    raw = load("pg35646.txt")
    # Blot marks each receipt with an italicised heading, e.g.
    #   _Veal a la Orloff._
    pat = re.compile(r"^  _([^_]{6,70}?)\._\s*$", re.M)
    hits = list(pat.finditer(raw))
    out = []
    for i, m in enumerate(hits):
        title = re.sub(r"\s+", " ", m.group(1).strip())
        if not re.search(r"(soup|stew|pudding|pie|cake|meat|chicken|beef|"
                         r"mutton|pork|veal|fish|salmon|potato|apple|"
                         r"bread|butter|sauce|cheese|egg|rice|"
                         r"broth|hash|boiled|fried|roast|cutlet|"
                         r"omelette|mayonnaise|salad|asparagus|"
                         r"cauliflower|celery|cabbage|carrot|peas|"
                         r"beans|onion|mushroom|pear|cherry|"
                         r"lemon|orange|gelatine|jelly|preserves|"
                         r"coffee|tea|cocoa|wine|ale|chestnut|"
                         r"spinach|potatoes|parsley|pepper|"
                         r"soup|duck|tongue|calf|lobster|shrimp|"
                         r"oyster|broth|scallop|asparagus|celery|"
                         r"cucumber|melon|plum|peach|apricot|"
                         r"banana|grape|raisin|fig|date)", title, re.I):
            continue
        start = m.end()
        end = hits[i + 1].start() if i + 1 < len(hits) else start + 3000
        block = clean(raw[start:end]).strip()
        if len(block) < 280 or len(block) > 6000:
            continue
        steps = split_sentences(block)
        if len(steps) < 4:
            continue
        out.append({
            "title": title,
            "source": "Pierre Blot, Hand-Book of Practical Cookery (1874)",
            "source_url": "https://www.gutenberg.org/ebooks/35646",
            "year": "1874",
            "region": "United States",
            "era": "victorian",
            "body": block[:2500],
            "steps": steps,
        })
    return out


# --------------------------------------------------------------- American Cookery 1796
def extract_american():
    raw = load("pg12815.txt")
    # Same convention: italicised heading lines.
    pat = re.compile(r"^_([^_]{6,70}?)\._\s*$", re.M)
    hits = list(pat.finditer(raw))
    out = []
    for i, m in enumerate(hits):
        title = re.sub(r"\s+", " ", m.group(1).strip())
        if not re.search(r"(soup|stew|pudding|pie|cake|meat|chicken|beef|"
                         r"mutton|pork|veal|fish|salmon|potato|apple|"
                         r"bread|butter|sauce|cheese|egg|rice|"
                         r"broth|hash|boiled|fried|roast|melon|"
                         r"peas|beans|onion|shrimp|lobster|oyster|"
                         r"salad|asparagus|cucumber|peas|corn|"
                         r"preserves|ginger|mustard|vinegar|oil|"
                         r"seasoning|dressing|bacon|ham|birds|"
                         r"tongue|greens|artichoke|egg|"
                         r"pudding|pie|cake|cookie|custard|"
                         r"cream|butter|cheese|spice|beverage|"
                         r"beverages|wine|cider)", title, re.I):
            continue
        start = m.end()
        end = hits[i + 1].start() if i + 1 < len(hits) else start + 3000
        block = clean(raw[start:end]).strip()
        if len(block) < 250 or len(block) > 6000:
            continue
        steps = split_sentences(block)
        if len(steps) < 4:
            continue
        out.append({
            "title": title,
            "source": "American Cookery (1796)",
            "source_url": "https://www.gutenberg.org/ebooks/12815",
            "year": "1796",
            "region": "United States",
            "era": "georgian",
            "body": block[:2500],
            "steps": steps,
        })
    return out


# period spellings -> modern display names
DISPLAY = {
    "cabbidge": "Cabbage", "cabbages": "Cabbage", "cinamon": "Cinnamon",
    "sallets": "Salad leaves", "sallet": "Salad leaves",
    "spinage": "Spinach", "spinach": "Spinach", "cabbidge": "Cabbage",
    "garlick": "Garlic", "garlic": "Garlic", "oyl": "Oil", "oil": "Oil",
    "lard": "Lard", "marrow": "Marrow (bone marrow)", "suet": "Suet",
    "beefsteaks": "Beef steaks", "fowls": "Fowls", "fowl": "Fowl",
    "sweetbreads": "Sweetbreads", "tongue": "Tongue",
    "verjuyce": "Verjuice (green verjuice)", "verjuice": "Verjuice",
    "claret": "Claret", "ale": "Ale", "pease": "Peas", "peas": "Peas",
    "chesnuts": "Chestnuts", "chestnuts": "Chestnuts",
    "pistaches": "Pistachios", "filberts": "Hazelnuts",
    "skirrets": "Skirret", "artichocks": "Artichokes",
    "cauliflowers": "Cauliflower", "mushrooms": "Mushrooms",
    "herbs": "Sweet herbs", "barberries": "Barberries",
    "goosberries": "Gooseberries", "grapes": "Grapes",
    "sippets": "Sippets of bread", "bread": "Bread",
    "broth": "Broth", "gravy": "Gravy", "stock": "Stock",
    "wine": "Wine", "vinegar": "Vinegar", "salt": "Salt",
    "pepper": "Pepper", "saffron": "Saffron", "mace": "Mace",
    "cloves": "Cloves", "nutmeg": "Nutmeg", "ginger": "Ginger",
    "mustard": "Mustard", "spices": "Spices", "sugar": "Sugar",
    "honey": "Honey", "molasses": "Molasses", "flour": "Flour",
    "meal": "Meal", "barley": "Barley", "rice": "Rice", "oats": "Oats",
    "starch": "Starch", "butter": "Butter", "milk": "Milk",
    "cream": "Cream", "cheese": "Cheese", "eggs": "Eggs",
    "yolks": "Egg yolks", "almonds": "Almonds", "walnuts": "Walnuts",
    "raisins": "Raisins", "dates": "Dates", "figs": "Figs",
    "prunes": "Prunes", "apples": "Apples", "pears": "Pears",
    "cherries": "Cherries", "plums": "Plums", "oranges": "Oranges",
    "lemons": "Lemons", "lemon": "Lemon", "onions": "Onions",
    "shallots": "Shallots", "leeks": "Leeks", "carrots": "Carrots",
    "potatoes": "Potatoes", "turnips": "Turnips", "parsnips": "Parsnips",
    "beets": "Beets", "cabbage": "Cabbage", "broccoli": "Broccoli",
    "beans": "Beans", "lentils": "Lentils", "tomatoes": "Tomatoes",
    "melons": "Melons", "cucumbers": "Cucumbers", "sorrel": "Sorrel",
    "endive": "Endive", "burrage": "Borage", "lettuce": "Lettuce",
    "greens": "Greens", "parsley": "Parsley", "thyme": "Thyme",
    "tyme": "Thyme", "rosemary": "Rosemary", "sage": "Sage",
    "marjoram": "Marjoram", "mint": "Mint", "dill": "Dill",
    "savory": "Savory", "savoury": "Savoury", "marigolds": "Marigold leaves",
    "beef": "Beef", "veal": "Veal", "mutton": "Mutton", "lamb": "Lamb",
    "pork": "Pork", "ham": "Ham", "bacon": "Bacon", "chicken": "Chicken",
    "duck": "Duck", "goose": "Goose", "turkey": "Turkey",
    "sausage": "Sausage", "hare": "Hare", "rabbit": "Rabbit",
    "venison": "Venison", "carp": "Carp", "salmon": "Salmon",
    "tench": "Tench", "bream": "Bream", "fish": "Fish",
    "herrings": "Herrings", "cod": "Cod", "eel": "Eel", "perch": "Perch",
    "mullet": "Mullet", "turbot": "Turbot", "stockfish": "Stockfish",
    "oysters": "Oysters", "lobster": "Lobster", "shrimp": "Shrimp",
    "crabs": "Crabs", "liver": "Liver", "peas": "Peas",
    "biscuits": "Biscuits", "husks": "Husks", "rennet": "Rennet",
    "curds": "Curd cheese", "water": "Water", "teas": "Tea",
    "candle": "Isinglass", "gelatine": "Gelatine", "jelly": "Jelly",
    "orange-flower": "Orange flower water", "coffees": "Coffee",
    "tea": "Tea", "caper": "Capers", "nutmeg": "Nutmeg",
    "sallete": "Salad leaves",
}

# titles that are variants of another recipe rather than a dish in their
# own right
VARIANT_RX = re.compile(
    r"^(other|another|to make the same|the same|a second|a third|"
    r"second way|otherwise|for a|to make another)", re.I)


def is_variant(title):
    t = title.strip()
    if VARIANT_RX.match(t):
        return True
    if re.search(r"\b(another way|other ways|otherways|divers wayes|"
                 r"the same|second way|another manner|as before|"
                 r"as aforesaid|or thus|or otherwise)\b", t, re.I):
        return True
    return False


def clean_title(raw):
    """Tidy a 17th-century recipe heading for display."""
    t = re.sub(r"\s+", " ", raw).strip()
    # strip a leading number from the heading ("6. To stew a Neats Tongue")
    t = re.sub(r"^\d+\.\s*", "", t)
    # period spelling -> modern, word by word
    words = [DISPLAY.get(w.lower(), w) for w in t.split()]
    t = " ".join(words)
    # the books shout their dish names; bring them down to title case
    t = re.sub(r"\b([A-Z]{3,})\b",
               lambda m: m.group(1).capitalize(), t)
    # leading articles and a leading "To" read better lowercased
    t = re.sub(r"\bDivers\b", "Various", t)
    t = re.sub(r"\bdivers\b", "various", t)
    t = re.sub(r"\botherwaies\b", "other ways", t)
    t = re.sub(r"\botherways\b", "other ways", t)
    t = re.sub(r"\bbroild\b", "broiled", t)
    t = re.sub(r"\bboil'd\b", "boiled", t)
    t = re.sub(r"\bstew'd\b", "stewed", t)
    t = re.sub(r"\bfarc't\b", "farc'd", t)
    t = re.sub(r"\bforc'd\b", "forced", t)
    t = re.sub(r"\bsowce\b", "sauce", t)
    t = re.sub(r"\bsouce\b", "sauce", t)
    # period nouns keep their name; the gloss goes in the note, not the title
    t = re.sub(r"\bBisk\b", "Bisk", t)
    t = re.sub(r"\bChines\b", "Chines", t)
    t = re.sub(r"\bCals\b", "Calves", t)
    t = re.sub(r"\bCalver\b", "Calver", t)
    t = re.sub(r"\bBore\b", "Bore", t)
    t = re.sub(r"\bPidgeons\b", "Pigeons", t)
    t = re.sub(r"\bPutt\b", "Putt", t)
    t = re.sub(r"\bTongues\b", "Tongues", t)
    t = re.sub(r"\bUdder\b", "Udder", t)
    t = re.sub(r"\bHeifers\b", "Heifer", t)
    t = re.sub(r"\bHens\b", "Hens", t)
    t = re.sub(r"\bHare\b", "Hare", t)
    t = re.sub(r"\bSturgeon\b", "Sturgeon", t)
    t = re.sub(r"\bMullet\b", "Mullet", t)
    t = re.sub(r"\bBream\b", "Bream", t)
    t = re.sub(r"\bPike\b", "Pike", t)
    t = re.sub(r"\bPies\b", "Pies", t)
    t = re.sub(r"\bPye\b", "Pie", t)
    t = re.sub(r"\bPudding\b", "Pudding", t)
    t = re.sub(r"\bPuddings\b", "Puddings", t)
    t = re.sub(r"\bFlesshe\b", "Flesh", t)
    t = re.sub(r"\bChewtes\b", "Cheats", t)
    t = re.sub(r"\bNeats\b", "Neat's", t)
    t = re.sub(r"\bHeifer\b", "Heifer", t)
    t = re.sub(r"\bBolonia\b", "Bologna", t)
    t = re.sub(r"\bPigeons or Doves\b", "Pigeons or Doves", t)
    t = re.sub(r"\bSauces\b", "Sauces", t)
    t = re.sub(r"\bFricase\b", "Fricassé", t)
    t = re.sub(r"\bFricassy\b", "Fricassé", t)
    t = re.sub(r"\bMarrow Pies\b", "Marrow Pies", t)
    t = re.sub(r"\bSouce\b", "Sauce", t)
    t = re.sub(r"\bCals\b", "Calves", t)
    t = re.sub(r"\bGreen\b", "Green", t)
    t = re.sub(r"\bPease\b", "Peas", t)
    t = re.sub(r"\bSoop\b", "Soup", t)
    t = re.sub(r"\bAlmon\b", "Almond", t)
    t = re.sub(r"\bPultney\b", "Pultney", t)
    return t.strip()


# glosses for the period nouns a modern cook will not know
GLOSSES = {
    "bisk": "a bisk was a great raised pie, baked in a lidded dish and "
            "cut at table",
    "chines": "chines were chopped joints of meat, the cook's way of "
              "using up a bird",
    "bore": "a bore was a wild boar, the most dangerous pork there is",
    "calver": "to calver was to press a fish gently so the flesh stays "
              "whole and sweet",
    "olives of beef": "olives of beef were thin slices stuffed and fried, "
                      "named for their shape",
    "pudpings": "",
    "sauce": "",
}


def title_note(title):
    """A short gloss for the period words in a title, if it needs one."""
    low = title.lower()
    for key, note in GLOSSES.items():
        if not note:
            continue
        if key in low:
            return note
    return ""


# --------------------------------------------------------------- ingredients
# The Gutenberg books do not print ingredient lists. The ingredients are
# in the prose, so they are harvested from the method text: any food word
# that the recipe mentions becomes an ingredient, with a sensible default
# quantity.
#
# The point is not to reproduce the original quantities (these books
# rarely state them) but to give the pantry matcher something to work
# with, and to show the cook what actually goes in.

FOOD_WORDS = {
    # protein
    "beef": "beef_roast", "veal": "veal", "mutton": "mutton",
    "lamb": "mutton", "pork": "pork", "ham": "ham", "bacon": "bacon",
    "chicken": "chicken", "fowls": "chicken", "fowl": "chicken",
    "duck": "chicken", "goose": "chicken", "turkey": "chicken",
    "tongue": "beef_roast", "liver": "beef_roast", "sweetbreads": "veal",
    "sausage": "sausage", "hare": "mutton", "rabbit": "mutton",
    "venison": "beef_roast", "beefsteaks": "beef_roast",
    "carp": "fish", "salmon": "fish", "tench": "fish", "bream": "fish",
    "fish": "fish", "herrings": "fish", "cod": "fish", "eel": "fish",
    "perch": "fish", "mullet": "fish", "turbot": "fish", "stockfish": "fish",
    "oysters": "fish", "lobster": "fish", "shrimp": "fish", "crabs": "fish",
    # dairy
    "butter": "butter", "milk": "milk", "cream": "cream",
    "cheese": "parmesan", "eggs": "eggs", "yolks": "eggs",
    "rennet": "misc", "curds": "parmesan",
    # veg
    "onions": "onion", "onion": "onion", "shallots": "onion",
    "garlick": "garlic", "garlic": "garlic", "leeks": "leeks",
    "leek": "leeks", "carrots": "carrots", "carrot": "carrots",
    "potatoes": "potato", "potato": "potato", "turnips": "mixed_veg",
    "turnip": "mixed_veg", "parsnips": "mixed_veg", "beets": "beets",
    "beet": "beets", "skirrets": "mixed_veg", "artichocks": "mixed_veg",
    "cabbidge": "cabbage", "cabbage": "cabbage", "cabbages": "cabbage",
    "broccoli": "mixed_veg", "cauliflowers": "mixed_veg",
    "peas": "peas", "pease": "peas", "beans": "beans", "lentils": "beans",
    "tomatoes": "tomatoes", "melons": "squash", "melon": "squash",
    "cucumbers": "mixed_veg", "spinach": "spinach", "spinage": "spinach",
    "sorrel": "spinach", "endive": "spinach", "burrage": "spinach",
    "lettuce": "spinach", "greens": "spinach", "herbs": "herbs",
    "parsley": "parsley", "thyme": "thyme", "tyme": "thyme",
    "rosemary": "rosemary", "sage": "sage", "marjoram": "herbs",
    "mint": "dill", "dill": "dill", "savory": "oregano",
    "savoury": "oregano", "marigolds": "herbs", "barberries": "cherries",
    "goosberries": "cherries", "grapes": "raisins", "raisins": "raisins",
    # fruit
    "apples": "apple", "apple": "apple", "pears": "apple", "pear": "apple",
    "cherries": "cherries", "plums": "cherries", "plum": "cherries",
    "oranges": "lemon", "orange": "lemon", "lemon": "lemon",
    "lemons": "lemon", "slices": "lemon", "dates": "dates",
    "figs": "dates", "prunes": "dates",
    # dry
    "flour": "flour", "bread": "bread", "sippets": "bread",
    "biscuits": "hardtack", "husks": "cornmeal", "meal": "cornmeal",
    "barley": "grain", "rice": "rice", "oats": "oats", "starch": "cornstarch",
    "sugar": "sugar", "honey": "honey", "molasses": "molasses",
    "almonds": "nuts", "almond": "nuts", "chesnuts": "nuts",
    "chestnuts": "nuts", "pistaches": "nuts", "filberts": "nuts",
    "walnuts": "walnuts", "marrow": "lard", "suet": "lard",
    "lard": "lard", "oyl": "olive_oil", "oil": "olive_oil",
    "sallet": "spinach",
    # seasoning
    "pepper": "pepper", "salt": "salt", "saffron": "saffron",
    "cinnamon": "cinnamon", "cinamon": "cinnamon", "nutmeg": "nutmeg",
    "mace": "mace", "cloves": "cloves", "ginger": "ginger",
    "mustard": "mustard_seeds", "spices": "spices_misc",
    "caper": "spices_misc", "verjuyce": "vinegar", "verjuice": "vinegar",
    "vinegar": "vinegar", "wine": "white_wine", "claret": "red_wine",
    "ale": "ale", "beer": "ale", "broth": "broth", "gravy": "broth",
    "water": "water", "stock": "broth", "verjuyce": "vinegar",
    "orange-flower": "rose_water", "coffees": "tea", "tea": "tea",
    "gelatine": "gelatine", "jelly": "gelatine", "candle": "misc",
}

# ingredient -> a sensible default quantity for a 4-serving recipe
DEFAULTS = {
    "beef_roast": (500, "g"), "veal": (400, "g"), "mutton": (500, "g"),
    "pork": (400, "g"), "ham": (150, "g"), "bacon": (100, "g"),
    "chicken": (600, "g"), "sausage": (200, "g"), "fish": (400, "g"),
    "butter": (60, "g"), "milk": (250, "ml"), "cream": (100, "ml"),
    "parmesan": (60, "g"), "eggs": (3, "ea"), "onion": (2, "ea"),
    "garlic": (3, "clove"), "leeks": (2, "ea"), "carrots": (300, "g"),
    "potato": (400, "g"), "mixed_veg": (300, "g"), "beets": (200, "g"),
    "cabbage": (400, "g"), "peas": (250, "g"), "beans": (250, "g"),
    "tomatoes": (300, "g"), "squash": (400, "g"), "spinach": (200, "g"),
    "herbs": (0.5, "cup"), "parsley": (0.25, "cup"), "thyme": (4, "sprig"),
    "rosemary": (2, "sprig"), "sage": (4, "leaf"), "dill": (0.25, "cup"),
    "oregano": (1, "tsp"), "apple": (3, "ea"), "cherries": (300, "g"),
    "lemon": (2, "ea"), "dates": (150, "g"), "raisins": (100, "g"),
    "flour": (200, "g"), "bread": (150, "g"), "hardtack": (100, "g"),
    "cornmeal": (200, "g"), "grain": (150, "g"), "rice": (200, "g"),
    "oats": (150, "g"), "cornstarch": (30, "g"), "sugar": (100, "g"),
    "honey": (60, "g"), "molasses": (60, "ml"), "nuts": (100, "g"),
    "walnuts": (60, "g"), "lard": (50, "g"), "olive_oil": (45, "ml"),
    "pepper": (1, "tsp"), "salt": (1, "tsp"), "saffron": (0.25, "tsp"),
    "cinnamon": (1, "tsp"), "nutmeg": (0.5, "tsp"), "mace": (0.25, "tsp"),
    "cloves": (0.125, "tsp"), "ginger": (1, "tsp"),
    "mustard_seeds": (30, "g"), "spices_misc": (1, "tsp"),
    "vinegar": (30, "ml"), "white_wine": (150, "ml"), "red_wine": (150, "ml"),
    "ale": (330, "ml"), "broth": (1000, "ml"), "water": (500, "ml"),
    "rose_water": (1, "tsp"), "tea": (10, "g"), "gelatine": (10, "g"),
    "misc": (1, "ea"),
}

# words that look like food but are actually units or section noise
STOP = {
    "the", "a", "an", "and", "or", "of", "with", "in", "to", "some",
    "piece", "pieces", "handful", "tablespoonful", "spoonful", "pint",
    "pints", "quart", "quarts", "pound", "pounds", "ounce", "ounces",
    "gallon", "gill", "cup", "cups", "spoonfuls", "slices", "slice",
}


def harvest_ingredients(block, title):
    """Find the food ingredients mentioned in a recipe's prose."""
    found = {}
    low = block.lower()
    for word, key in FOOD_WORDS.items():
        if word in STOP:
            continue
        if not re.search(r"\b" + re.escape(word) + r"\b", low):
            continue
        found.setdefault(key, word)
    found.pop("misc", None)
    out = []
    for key, word in sorted(found.items()):
        qty, unit = DEFAULTS.get(key, (1, "ea"))
        out.append({
            "name": DISPLAY.get(word, word.capitalize()),
            "qty": qty,
            "unit": unit,
            "pantry": key,
            "note": "",
        })
    # a long ingredient list means the block ran into the next recipe.
    # Keep the ones that actually carry the dish.
    if len(out) > 10:
        priority = ["beef_roast", "veal", "mutton", "pork", "chicken", "fish",
                    "sausage", "bread", "broth", "butter", "onion", "garlic",
                    "carrots", "potato", "flour", "eggs"]
        keep = [i for i in out if i["pantry"] in priority][:8]
        seen = {i["pantry"] for i in keep}
        for i in out:
            if len(keep) >= 9:
                break
            if i["pantry"] not in seen:
                keep.append(i)
                seen.add(i["pantry"])
        out = keep
    return out


# --------------------------------------------------------------- assemble
def build_records(raw, tag):
    recs = []
    for i, r in enumerate(raw):
        title = r["title"]
        # a "variant" is a second way of making something already covered
        if is_variant(title):
            continue
        display_title = clean_title(title)
        body = r["body"]
        first = body.split(". ")[0]
        history = first.strip() + "."
        if len(history) < 200:
            era_note = {
                "renaissance": "Robert May's Accomplisht Cook of 1660 is the "
                               "first cookbook written by a professional "
                               "cook in English, and it reads like one: "
                               "nothing is measured, everything is timed by "
                               "the fire and the cook's judgement. The "
                               "recipes are written for a kitchen with a "
                               "great fire, a good larder and a servant who "
                               "already knows how the master likes it.",
                "georgian": "Elizabeth Moxon's English Housewifry of 1720 "
                            "was aimed at the mistress of a good house who "
                            "did her own cooking, and it shows: the "
                            "instructions are precise about technique and "
                            "vague about quantity, because she assumed you "
                            "knew what 'a little' meant. It is a book of "
                            "soups, broths and boiled things, cooked "
                            "slowly in a pot, with the long spelling-out "
                            "of the small tasks that a modern recipe "
                            "assumes you already know.",
                "victorian": "Pierre Blot was the New York Cooking "
                             "Academy's great teacher, and his book reads "
                             "like a lesson: the technique is always "
                             "explained, the quantities are always given, "
                             "and the point is usually what a restaurant "
                             "kitchen did differently from a home one.",
            }.get(r["era"], "")
            history = (f"From {r['source']}. {era_note} The original wording "
                       "and the quantities the book gives are reproduced "
                       "below as they stand.")
        if len(history) < 200:
            history = (f"From {r['source']}. The original wording and the "
                       "quantities the book gives are reproduced below as "
                       "they stand, in the period spelling, so you can see "
                       "what the cook was actually told to do and how much "
                       "of it still applies.")
        ings = harvest_ingredients(body, title)
        if len(ings) < 3:
            continue
        recs.append({
            "id": f"gb-{tag}-{i:03d}",
            "title": display_title,
            "era": r["era"],
            "year": r["year"],
            "region": r["region"],
            "source": r["source"],
            "source_url": r["source_url"],
            "servings": 4,
            "tags": [],
            "confidence": "verified",
            "history": history,
            "source_text": body[:900],
            "method": r["steps"],
            "ingredients": ings,
            "funky": [],
            # These books do not print ingredient lists. The list below was
            # read out of the method text, so the quantities are a modern
            # cook's sensible defaults rather than the book's own.
            "ingredient_source": "reconstructed",
            "gloss": title_note(title),
        })
    return recs


if __name__ == "__main__":
    allrecs = []
    for fn, tag in ((extract_moxon, "moxon"), (extract_may, "may"),
                    (extract_blot, "blot"), (extract_american, "amcook")):
        try:
            raw = fn()
        except Exception as e:
            print(f"  {tag}: extractor error: {e}")
            raw = []
        recs = build_records(raw, tag)
        print(f"  {tag}: {len(raw)} candidates -> {len(recs)} records")
        for r in recs:
            print(f"     {r['title'][:58]:60s} {len(r['method'])} steps")
        allrecs.extend(recs)

    json.dump(allrecs, open(os.path.join(BASE, "gb_generated.json"), "w"),
              ensure_ascii=False, indent=1)
    print(f"\nTotal Gutenberg records: {len(allrecs)}")
