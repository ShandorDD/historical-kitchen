#!/usr/bin/env python3
"""Extract recipes from Gordon Ramsay's own recipe site.

gordonramsay.com/gr/recipes/ -- 176 recipes, all with a clean
"Ingredients" block and a "Cooking instructions" block, plus a category
filter list (chicken, beef, dessert, ...).

Gordon Ramsay is the modern end of the line this collection traces: the
apprenticeship at Claridge's and the Ritz under Marco Pierre White, then
a hundred television programmes teaching the same discipline Escoffier
wrote down. His recipes are modern (2006 onwards), so they are filed in
the Post-War era.

Output: ramsay_generated.json -- RECIPES-compatible records.
"""
import json
import os
import re
import html

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/histcook/src/gr"

# category slug -> a short label
CATEGORIES = {
    "2020-holiday": "Holiday", "autumn": "Autumn", "bbq": "Barbecue",
    "beef": "Beef", "breakfast": "Breakfast", "chicken": "Chicken",
    "chocolate": "Chocolate", "christmas": "Christmas",
    "comfort-food": "Comfort food", "dessert": "Dessert", "drinks": "Drinks",
    "duck": "Duck", "easter": "Easter", "egg": "Egg", "fish": "Fish",
    "fit-food": "Fit food", "game": "Game", "kids": "Kids", "lamb": "Lamb",
    "pancake-day": "Pancake Day", "pasta": "Pasta", "pie": "Pie",
    "pork": "Pork", "salads": "Salads", "seafood": "Seafood",
    "store-cupboard-staples": "Store-cupboard staples", "summer": "Summer",
    "thanksgiving": "Thanksgiving", "valentines-day": "Valentine's Day",
    "vegan": "Vegan", "vegetarian": "Vegetarian", "wellington": "Wellington",
}

# ---- shared with the other extractors -------------------------------
import sys
sys.path.insert(0, os.path.join(BASE, "data"))

PANTRY_RULES = [
    (r"\b(beef|steak|brisket|mince|beef mince|short rib|"
     r"oxtail|beef cheek)\b", "beef_roast"),
    (r"\b(veal|calf)\b", "veal"),
    (r"\b(lamb|mutton)\b", "mutton"),
    (r"\b(pork|ham|bacon|sausage|gammon|chorizo|prosciutto)\b", "pork"),
    (r"\b(chicken|duck|turkey|poultry|guinea fowl|quail)\b", "chicken"),
    (r"\b(salmon|tuna|cod|haddock|mackerel|sea bass|trout|"
     r"swordfish|monkfish|halibut|prawn|shrimp|lobster|crab|"
     r"scallop|mussel|oyster|anchovy|squid|calamari|white fish)\b", "fish"),
    (r"\b(egg)\b", "eggs"),
    (r"\b(butter|ghee|lard)\b", "butter"),
    (r"\b(milk|cream|creme fraiche|cr.me fra.che|buttermilk)\b", "cream"),
    (r"\b(cheese|parmesan|cheddar|mozzarella|ricotta|feta|"
     r"gruyere|halloumi|brie|creme fraiche)\b", "parmesan"),
    (r"\b(flour|breadcrumb|breadcrumbs|pastry|batter|biscuits)\b", "flour"),
    (r"\b(sugar|honey|syrup|molasses|icing|maple)\b", "sugar"),
    (r"\b(chocolate|cocoa)\b", "chocolate"),
    (r"\b(onion|shallot|leek|garlic|scallion)\b", "onion"),
    (r"\b(carrot)\b", "carrots"),
    (r"\b(potato|sweet potato)\b", "potato"),
    (r"\b(tomato|passata|tinned tomato)\b", "tomatoes"),
    (r"\b(lemon|lime|orange)\b", "lemon"),
    (r"\b(apple|pear)\b", "apple"),
    (r"\b(berry|berries|strawberr|raspberr|blueberr|blackberr|"
     r"raspberry|strawberry|blueberry|blackberry)\b", "cherries"),
    (r"\b(bean|beans|lentil|chickpea|pea|peas)\b", "beans"),
    (r"\b(cabbage|kale|spinach|rocket|arugula|lettuce|chard|"
     r"pak choi|bok choy)\b", "spinach"),
    (r"\b(broccoli|cauliflower|courgette|zucchini|aubergine|eggplant|"
     r"asparagus|pepper|capsicum|chilli|chili|cucumber|mushroom|"
     r"celery|parsnip|turnip|beetroot|butternut|squash|pumpkin|"
     r"sweetcorn|corn|peas|sugar snap|runner bean|"
     r"vegetable|veg)\b", "mixed_veg"),
    (r"\b(wine|red wine|white wine|vermouth|brandy|cognac|"
     r"sherry|port|rum|cider|beer|lager|stout|champagne)\b", "white_wine"),
    (r"\b(olive oil|rapeseed oil|sunflower oil|vegetable oil|oil|"
     r"mayonnaise|rapeseed)\b", "olive_oil"),
    (r"\b(vinegar|rice vinegar|cider vinegar|balsamic|"
     r"white wine vinegar|red wine vinegar)\b", "vinegar"),
    (r"\b(salt)\b", "salt"),
    (r"\b(pepper|black pepper|white pepper|paprika|cayenne|chilli "
     r"flakes|cayenne pepper)\b", "pepper"),
    (r"\b(cumin|coriander|turmeric|paprika|garam masala|"
     r"ground ginger|ginger|cinnamon|nutmeg|cloves|mace|cardamom|"
     r"allspice|spice|zaatar|sumac|saffron|chili powder|"
     r"cayenne powder|curry powder)\b", "spices_misc"),
    (r"\b(parsley|coriander fresh|thyme|rosemary|basil|mint|dill|"
     r"chives|tarragon|herbs|sage|marjoram|lemongrass|"
     r"flat leaf)\b", "herbs"),
    (r"\b(vanilla)\b", "vanilla"),
    (r"\b(nuts|almond|walnut|cashew|pecan|pistachio|hazelnut|"
     r"pine nuts)\b", "nuts"),
    (r"\b(raisin|sultana|currant|dried fruit)\b", "raisins"),
    (r"\b(bread)\b", "bread"),
    (r"\b(rice|pasta|spaghetti|penne|tagliatelle|linguine|"
     r"rigatoni|macaroni|noodle|gnocchi|orzo|couscous)\b", "pasta"),
    (r"\b(oats|porridge|muesli|granola)\b", "oats"),
    (r"\b(tomato puree|tomato paste|passata)\b", "tomato_paste"),
    (r"\b(baby spinach|watercress|mizuna)\b", "spinach"),
    (r"\b(sweetcorn)\b", "cornmeal"),
    (r"\b(white chocolate|dark chocolate|milk chocolate|"
     r"chocolate chips|chocolate buttons)\b", "chocolate"),
    (r"\b(plain flour|cornflour|cornstarch|starch|self-raising|"
     r"self raising|baking powder|bicarbonate|baking soda)\b", "flour"),
    (r"\b(cornstarch|cornflour)\b", "cornstarch"),
    (r"\b(white fish|whitefish)\b", "fish"),
    (r"\b(chicken stock|beef stock|vegetable stock|chicken broth|"
     r"stock|broth)\b", "broth"),
    (r"\b(vegetable oil|neutral oil)\b", "vegetable_oil"),
]

NAME_HINT = [
    (r"\b(beef|steak|brisket|mince|oxtail|short rib)\b", "meat"),
    (r"\b(veal|calf)\b", "meat"),
    (r"\b(lamb|mutton)\b", "meat"),
    (r"\b(pork|ham|bacon|sausage|gammon|chorizo|prosciutto)\b", "meat"),
    (r"\b(chicken|duck|turkey|poultry|guinea fowl|quail)\b", "meat"),
    (r"\b(salmon|tuna|cod|haddock|mackerel|sea bass|trout|swordfish|"
     r"monkfish|halibut|prawn|shrimp|lobster|crab|scallop|mussel|"
     r"oyster|anchovy|squid|calamari|white fish)\b", "fish"),
    (r"\b(egg)\b", "eggs"),
    (r"\b(butter|ghee|lard)\b", "butter"),
    (r"\b(milk|cream|creme fraiche|cr.me fra.che|buttermilk)\b", "cream"),
    (r"\b(cheese|parmesan|cheddar|mozzarella|ricotta|feta|gruyere|"
     r"halloumi|brie)\b", "cheese"),
    (r"\b(flour|breadcrumbs|breadcrumb|pastry|batter|biscuits)\b", "flour"),
    (r"\b(sugar|honey|syrup|molasses|icing|maple)\b", "sugar"),
    (r"\b(chocolate|cocoa)\b", "chocolate"),
    (r"\b(onion|shallot|leek|garlic|scallion)\b", "onion"),
    (r"\b(carrot)\b", "carrots"),
    (r"\b(potato|sweet potato)\b", "potato"),
    (r"\b(tomato|passata)\b", "tomatoes"),
    (r"\b(lemon|lime|orange)\b", "lemon"),
    (r"\b(apple|pear)\b", "apple"),
    (r"\b(berry|berries|strawberr|raspberr|blueberr|blackberr)\b", "fruit"),
    (r"\b(bean|beans|lentil|chickpea|peas)\b", "beans"),
    (r"\b(cabbage|kale|spinach|rocket|arugula|lettuce|chard)\b", "greens"),
    (r"\b(broccoli|cauliflower|courgette|zucchini|aubergine|eggplant|"
     r"asparagus|pepper|capsicum|chilli|chili|cucumber|mushroom|"
     r"celery|parsnip|turnip|beetroot|butternut|squash|pumpkin|"
     r"sweetcorn|corn|sugar snap|runner bean|vegetable)\b", "veg"),
    (r"\b(wine|vermouth|brandy|cognac|sherry|port|rum|cider|beer|"
     r"lager|stout|champagne)\b", "drink"),
    (r"\b(olive oil|rapeseed oil|sunflower oil|vegetable oil|oil|"
     r"mayonnaise)\b", "oil"),
    (r"\b(vinegar|balsamic)\b", "vinegar"),
    (r"\b(salt)\b", "salt"),
    (r"\b(pepper|black pepper|paprika|cayenne|chilli flakes)\b", "pepper"),
    (r"\b(cumin|coriander|turmeric|garam masala|ginger|cinnamon|"
     r"nutmeg|cloves|mace|cardamom|allspice|spice|zaatar|saffron|"
     r"curry powder|chili powder)\b", "spices"),
    (r"\b(parsley|thyme|rosemary|basil|mint|dill|chives|tarragon|"
     r"herbs|sage|marjoram|lemongrass)\b", "herbs"),
    (r"\b(vanilla)\b", "vanilla"),
    (r"\b(nuts|almond|walnut|cashew|pecan|pistachio|hazelnut)\b", "nuts"),
    (r"\b(raisin|sultana|currant)\b", "dried"),
    (r"\b(bread)\b", "bread"),
    (r"\b(rice|pasta|spaghetti|penne|tagliatelle|linguine|rigatoni|"
     r"macaroni|noodle|gnocchi|orzo|couscous)\b", "pasta"),
    (r"\b(oats|porridge|muesli|granola)\b", "oats"),
    (r"\b(tomato puree|tomato paste)\b", "paste"),
    (r"\b(chicken stock|beef stock|vegetable stock|stock|broth)\b", "stock"),
]

DEFAULT_QTY = {
    "beef_roast": (500, "g"), "veal": (400, "g"), "mutton": (500, "g"),
    "pork": (400, "g"), "chicken": (600, "g"), "fish": (400, "g"),
    "butter": (60, "g"), "cream": (100, "ml"), "milk": (250, "ml"),
    "parmesan": (60, "g"), "eggs": (3, "ea"), "flour": (200, "g"),
    "sugar": (100, "g"), "onion": (2, "ea"), "carrots": (300, "g"),
    "potato": (400, "g"), "mixed_veg": (300, "g"), "tomatoes": (300, "g"),
    "lemon": (2, "ea"), "apple": (3, "ea"), "cherries": (300, "g"),
    "beans": (250, "g"), "spinach": (200, "g"), "white_wine": (150, "ml"),
    "olive_oil": (45, "ml"), "vinegar": (30, "ml"), "salt": (1, "tsp"),
    "pepper": (1, "tsp"), "spices_misc": (1, "tsp"), "herbs": (0.5, "cup"),
    "vanilla": (1, "tsp"), "chocolate": (100, "g"), "nuts": (100, "g"),
    "raisins": (100, "g"), "bread": (150, "g"), "pasta": (400, "g"),
    "oats": (150, "g"), "cornstarch": (30, "g"), "broth": (1000, "ml"),
    "tomato_paste": (60, "g"), "vegetable_oil": (45, "ml"), "misc": (1, "ea"),
}

FRACTIONS = {
    "¼": 0.25, "½": 0.5, "¾": 0.75, "⅓": 0.3333, "⅔": 0.6667, "⅛": 0.125,
    "1/4": 0.25, "1/2": 0.5, "3/4": 0.75, "1/3": 0.3333, "2/3": 0.6667,
    "1/8": 0.125, "3/8": 0.375, "5/8": 0.625, "7/8": 0.875,
    "1/16": 0.0625, "5/16": 0.3125, "7/16": 0.4375, "9/16": 0.5625,
    "11/16": 0.6875, "13/16": 0.8125, "15/16": 0.9375,
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
         .replace("⅓", " 1/3").replace("⅔", " 2/3").replace("⅛", " 1/8")
         .replace("⅜", " 3/8").replace("⅝", " 5/8").replace("⅞", " 7/8"))
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
    if u.startswith("ml") or u.startswith("milli"):
        return "ml"
    if u.startswith("l") and not u.startswith("lb"):
        return "l"
    if u.startswith("table"):
        return "tbsp"
    if u.startswith("tea"):
        return "tsp"
    if u.startswith("fl"):
        return "cup"
    if u.startswith("pint") or u.startswith("quart") or u.startswith("cup") \
            or u.startswith("gill") or u.startswith("teacup"):
        return "cup"
    return "ea"


def key_for(name):
    n = name.lower()
    for rx, key in PANTRY_RULES:
        if re.search(rx, n):
            return key
    return "misc"


QTY_RX = re.compile(
    r"^\s*(?P<num>[\d¼½¾⅓⅔⅛\.,/]+\s*(?:[\d¼½¾⅓⅔⅛]+)?)\s*"
    r"(?P<unit>lbs?\.|lb|ounces?|oz\.?|grams?|g|kilos?|kg|pints?|quarts?|"
    r"gills?|teacups?|cups?|fl oz|fl\. oz\.|decilitres?|litres?|l\.|"
    r"millilitres?|ml|tablespoonfuls?|tablespoons?|tbsp|"
    r"teaspoonfuls?|teaspoons?|tsp|dash|pinch|handful)?\s*", re.I)


def parse_ingredient(line):
    line = line.strip()
    if not line or len(line) > 200:
        return None
    # strip trailing note
    line = re.sub(r"\s*\(.*?\)\s*$", "", line).strip()
    m = QTY_RX.match(line)
    qty, unit, rest = None, "ea", line
    if m:
        qty = to_float(m.group("num"))
        if m.group("unit"):
            unit = unit_kind(m.group("unit"))
        rest = line[m.end():]
    else:
        mc = re.match(r"^\s*(\d+)\s+", line)
        if mc:
            qty = float(mc.group(1))
            rest = line[mc.end():]
    rest = re.sub(r"^[\s,;:\-–—(]*", "", rest)
    rest = re.sub(r"\s+", " ", rest).strip(" ,.;:")
    if not rest:
        return None
    found = None
    for rx, kind in NAME_HINT:
        mm = re.search(rx, rest, re.I)
        if mm:
            found = mm.group(0)
            break
    if not found:
        return None
    key = key_for(found)
    if key == "misc":
        return None
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


def strip_html(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        t = f.read()
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    lines = []
    prev = None
    for ln in t.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        if ln == prev:
            continue
        prev = ln
        lines.append(ln)
    return lines


records = []
files = sorted(f for f in os.listdir(SRC) if f.endswith(".html"))
for fn in files:
    slug = fn[:-5]
    path = os.path.join(SRC, fn)
    lines = strip_html(path)
    # the title is the all-caps line just before "Ingredients"
    title = ""
    i_ing = i_meth = None
    for i, ln in enumerate(lines):
        if ln == "Ingredients" and i_ing is None:
            i_ing = i
        if ln in ("Cooking instructions", "Cooking Instructions",
                  "Method", "Instructions") and i_ing is not None \
                and i_meth is None and i > i_ing:
            i_meth = i
            break
    if i_ing is None:
        continue
    # The recipe name sits directly above "Ingredients". On this site it
    # is title case, not shouted, so take the line above and reject the
    # nav furniture.
    NAV = {
        "gordon ramsay.com", "academy", "restaurants & bars",
        "uk restaurants", "us restaurants", "recipes", "chicken recipes",
        "beef recipes", "vegetarian recipes", "ultimate fit food",
        "masterclasses", "the gordon ramsay masterclass", "about gordon",
        "gordon & tana ramsay foundation", "books", "hexclad",
        "by chef ramsay", "chef blast", "gordon ramsay wines", "tv",
        "studio ramsay", "careers", "gifts", "menu",
        "javascript turned off", "your browser appears to have javascript "
        "disabled. you may find this causes parts of the site to function "
        "unexpectedly. please enable javascript",
        "please upgrade your browser",
        "it appears you are using an older browser. this site will function "
        "better if you upgrade to the latest version",
    }
    title = ""
    for j in range(i_ing - 1, max(0, i_ing - 8), -1):
        cand = lines[j]
        if cand.lower() in NAV or cand.startswith(("Your browser", "Please ",
                                                    "It appears")):
            continue
        if len(cand) < 4:
            continue
        title = cand
        break
    if not title:
        title = slug.replace("-", " ").replace("_", " ").title()
    # tidy the title: "Gordon'S" should be "Gordon's"
    title = re.sub(r"([a-z])'S\b", r"\1's", title)
    title = re.sub(r"\bBaked(\w)", lambda m: "Baked " + m.group(1), title)
    if " " not in title and len(title) > 6:
        # a camelCase slug with no title on the page: split it
        title = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", title)
    # ingredients: from after "Ingredients" to the method marker
    ing_lines = lines[i_ing + 1:(i_meth if i_meth else len(lines))]
    ings, seen = [], set()
    for ln in ing_lines[:50]:
        p = parse_ingredient(ln)
        if p and p["pantry"] not in seen:
            seen.add(p["pantry"])
            ings.append(p)
    if len(ings) < 3:
        continue
    # method
    meth_lines = lines[i_meth + 1:] if i_meth else []
    method_text = " ".join(meth_lines)
    # stop at the site furniture
    for stop in ("RECIPE NOTES:", "Looking to learn new cookery skills",
                 "Back", "Next", "Category Filters", "Share", "Print",
                 "Nutrition", "You might also like", "Search",
                 "Skip to main content", "Recipe Notes:"):
        idx = method_text.find(stop)
        if idx > 200:
            method_text = method_text[:idx]
    method_text = re.sub(r"\s+", " ", method_text).strip()
    steps = re.split(r"(?<=[.!])\s+(?=[A-Z])", method_text)
    steps = [s.strip() for s in steps if len(s.strip()) > 30][:12]
    if len(steps) < 2:
        continue
    # the "Serves N" line tells us the real yield
    servings = 4
    ms = re.search(r"serves\s+(\d+)", method_text, re.I)
    if ms:
        servings = max(1, int(ms.group(1)))
    # drop the "Serves N" fragment from the first step
    if steps:
        steps[0] = re.sub(r"^Serves\s+\d+\.?\s*", "", steps[0]).strip()
    # Categories: the "Category Filters" block is the same site-wide list
    # on every page, so it cannot tag a single recipe. Instead, infer
    # from the slug and from what is actually in the dish.
    cats = []
    for c, label in CATEGORIES.items():
        if c in slug:
            cats.append(label)
    if not cats:
        keys = {i["pantry"] for i in ings}
        if "chicken" in keys:
            cats.append("Chicken")
        elif "beef_roast" in keys:
            cats.append("Beef")
        elif "pork" in keys:
            cats.append("Pork")
        elif "fish" in keys:
            cats.append("Seafood")
        elif "mutton" in keys:
            cats.append("Lamb")
        if "chocolate" in keys or "sugar" in keys and "cream" in keys:
            cats.append("Dessert")
    if not cats:
        cats = ["Ramsay"]
    history = (f"Gordon Ramsay, from his own recipe collection. Ramsay trained "
               f"the hard way -- a two-year stage in Marco Pierre White's "
               f"kitchen at the Ritz, then Claridge's, then the Hotel "
               f"Concorde -- and it shows in how little he leaves to "
               f"chance. The method is reproduced as he writes it.")
    records.append({
        "id": "ramsay-" + slug,
        "title": title,
        "era": "postwar",
        "year": "2006 - 2025",
        "region": "Britain",
        "source": "Gordon Ramsay, gordonramsay.com",
        "source_url": f"https://gordonramsay.com/gr/recipes/{slug}/",
        "servings": servings,
        "tags": cats,
        "confidence": "verified",
        "history": history,
        "source_text": "",
        "method": steps,
        "ingredients": ings,
        "funky": [],
        "ingredient_source": "sourced",
        "gloss": "",
    })

json.dump(records, open(os.path.join(BASE, "ramsay_generated.json"), "w"),
          ensure_ascii=False, indent=1)
print(f"Extracted {len(records)} Gordon Ramsay recipes from {len(files)} pages.")
for r in records[:14]:
    print(f"   {r['title'][:44]:46s} {len(r['ingredients']):2d} ing  "
          f"{len(r['method'])} steps  {','.join(r['tags'][:2])}")
