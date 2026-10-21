#!/usr/bin/env python3
"""Build The Historical Kitchen: a self-contained interactive HTML page.

Inputs (all local):
  data/eras.py        era taxonomy
  data/recipes.py     the recipe corpus
  data/pantry.py      pantry dictionary + near-equivalents
  data/substitutes.py period-oddity -> modern stand-in reference

Output:
  index.html          one file, no external requests, works offline

The page has three things:
  1. an era rail (the user asked for era selection) that filters the
     recipe corpus,
  2. a pantry panel where you tick what you actually have, and the
     recommendations re-sort live,
  3. a scale engine: 4 portions is the standard, with 1-12 available,
     quantities recomputed and re-expressed in retail units.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "data"))

from eras import ERAS, ERA_BY_KEY, ERA_ORDER            # noqa: E402
from recipes import RECIPES                              # noqa: E402
from pantry import (PANTRY, DEFAULT_PANTRY, CATEGORIES,  # noqa: E402
                    NEAR_EQUIVALENTS, ALIASES)
from substitutes import SUBSTITUTES                      # noqa: E402
from cuisines import (family_for, FAMILY_ORDER,           # noqa: E402
                      FAMILY_BLURB)

# The Tasting History corpus is extracted mechanically from the source
# pages by extract_th.py + map_pantry.py. It is loaded from JSON so the
# hand-written recipes in recipes.py stay the curated core.
GEN_PATH = os.path.join(BASE, "th_generated.json")
GB_PATH = os.path.join(BASE, "gb_generated.json")
ESCO_PATH = os.path.join(BASE, "escoffier_generated.json")
RAMSAY_PATH = os.path.join(BASE, "ramsay_generated.json")
REGION_PATH = os.path.join(BASE, "region_generated.json")
NOVELS_PATH = os.path.join(BASE, "novels_generated.json")
GENERATED = []
if os.path.exists(GEN_PATH):
    with open(GEN_PATH) as f:
        GENERATED = json.load(f)
if os.path.exists(GB_PATH):
    with open(GB_PATH) as f:
        GENERATED = GENERATED + json.load(f)
if os.path.exists(ESCO_PATH):
    with open(ESCO_PATH) as f:
        GENERATED = GENERATED + json.load(f)
if os.path.exists(RAMSAY_PATH):
    with open(RAMSAY_PATH) as f:
        GENERATED = GENERATED + json.load(f)
if os.path.exists(REGION_PATH):
    with open(REGION_PATH) as f:
        GENERATED = GENERATED + json.load(f)

# The literary corpus is kept separate from the recipes: a passage from
# Dracula is evidence about the table, not a recipe.
FICTION = []
if os.path.exists(NOVELS_PATH):
    with open(NOVELS_PATH) as f:
        FICTION = json.load(f)

OUT = os.path.join(BASE, "index.html")

# The Tasting History corpus contains several recipes that are also in the
# hand-written set (Potage Crecy, Potted Meat, the WWII rations and so on).
# The curated versions carry the period-oddity panels and the verbatim
# quotes, so the extracted duplicates are dropped here.
EXCLUDE_TITLES = {
    "b ration apple cranberry sauce",
    "medieval cherry cheesecake",
    "medieval mustard",
    "potage crécy (creamy carrot and potato soup)",
    "potted meat",
    "roman mustard",
    "william the conqueror’s hen with cameline sauce",
    "wwii british corned beef stew",
    "wwii british military ration scones",
    "wwii italian military carrots",
    "wwii italian military pasta",
    "sumerian date cheesecake",
    "medieval cherry cheesecake",
    "old-fashioned old fashioned",
    "kvass",
    "pina colada",
    "baklava",
    "aztec salsa",
    "gumbo with crab and shrimp",
    "b ration apple cranberry sauce (1946)",
    "payn ragoun (medieval pine nut and grape sauce)",
    "william the conqueror’s hippocras",
    "new and improved kykeon",
    "odysseus’s roast pork",
    "stonehenge pork ribs with honey and mustard seed",
    "stonehenge nettle and hazelnut soup",
    "ancient egyptian zalabiya",
    "kanasu stew",
    "magnonnaise (mayonnaise)",
    "teacaudle",
    "chocolate wine",
    "english toffee",
    "turkish delight",
    "gumbo",
    "welsh rarebit",
    "chelsea buns",
    "kaldolmar",
    "pelmeni",
    "k-1 defense biscuits",
    "world war ii d ration",
    "b ration sausage and beans",
    "b ration pineapple milk",
    "workhouse scouse with suet dumplings",
    "shepherd’s pie",
    "school lunch salisbury steak",
    "tomato soup cake",
    "tesla’s roast duck with celery and cherries",
    "spiced kangaroo",
    "salsa de chile macho",
    "margherita pizza",
    "lobster with beurre blanc",
    "smoked salmon roses with caviar",
    "milk punch",
    "pocket soup",
    "puits d’amour",
    "pocketsoup",
    "alappanu",
    "brawn en peuerade",
    "biscuit hash",
    "anchovies with parmesan",
    "beef bourguignon",
    "williamshippocras",
    "pottedmeat",
    "potagecrecy",
    "romanmustard",
    "medievalmustard",
    "medievalcherrycheesecake",
    "oldfashioned",
    "kvass",
    "baklava",
    "aztecsalsa",
    "gumbo",
    "wwiibritishcornedbeefstew",
    "wwiibritishscones",
    "wwiiitaliancarrots",
    "wwiiitalianpasta",
    "brationapplesauce",
    "sumeriandatecake",
    "wwiimincemeatpie",
    "kration",
    "dration",
    "brationsausageandbeans",
    "brationpineapplemilk",
    "scouseandsuetdumplings",
    "shepherdspie",
    "salisburysteak",
    "tomatosoupcake",
    "teslasduck",
    "spicedkangaroo",
    "salsadechilemacho",
    "margheritapizza",
    "lobsterwithbeurreblanc",
    "smokedsalmonroses",
    "milkpunch",
    "pocketsoup",
    "puitsdamour",
    "alappanu",
    "brawnenpeuerade",
    "biscuithash",
    "anchovieswithparmesan",
    "beefbourguignon",
    "pinacolada",
    "mayonnaise",
    "englishtoffee",
    "turkishdelight",
    "chocolatewine",
    "chelseabuns",
    "kaldolmar",
    "pelmeni",
    "teacaudle",
    "newkykeon",
    "odysseusspork",
    "stonehengeribs",
    "stonehengesoup",
    "zalabiya",
    "kanasustew",
    "paynragoun",
    "williamshippocras",
    "romanporkandpuls",
    "romansweetandsour",
    "kration",
    "dration",
    "conditum paradoxum (roman spiced wine)",
    "cutlets",
}


def _norm_title(t):
    return " ".join(str(t).lower().split())


_excluded = 0
_keep = []
for _r in GENERATED:
    _t = _norm_title(_r.get("title", ""))
    if _t in EXCLUDE_TITLES or _r.get("id", "") in EXCLUDE_TITLES:
        _excluded += 1
        continue
    _keep.append(_r)
GENERATED = _keep
print(f"Excluded {_excluded} duplicate recipes; {len(GENERATED)} generated remain.")

# ------------------------------------------------------------------ payloads
ERAS_JSON = json.dumps(ERAS, ensure_ascii=False)
PANTRY_JSON = json.dumps(
    {k: {"label": v[0], "cat": v[1], "form": v[2], "staple": v[3]}
     for k, v in PANTRY.items()},
    ensure_ascii=False)
CATEGORIES_JSON = json.dumps(
    [{"cat": c, "label": l} for c, l in CATEGORIES], ensure_ascii=False)
DEFAULT_JSON = json.dumps(sorted(set(DEFAULT_PANTRY)))
NEAR_JSON = json.dumps(NEAR_EQUIVALENTS, ensure_ascii=False)
SUBS_JSON = json.dumps(SUBSTITUTES, ensure_ascii=False)

# Recipes: strip the python-only bits, keep what the page needs.
ALL_RECIPES = list(RECIPES) + list(GENERATED)
recs = []
for r in ALL_RECIPES:
    # The region string is free text; the cuisine family is what the
    # filter uses, so every recipe gets one.
    fam = family_for(r.get("region", "")) or "Other"
    recs.append({
        "id": r["id"],
        "title": r["title"],
        "era": r["era"],
        "year": r["year"],
        "region": r["region"],
        "cuisine": fam,
        "source": r["source"],
        "source_url": r.get("source_url", ""),
        "servings": r["servings"],
        "tags": r.get("tags", []),
        "confidence": r.get("confidence", "verified"),
        "history": r["history"],
        "source_text": r.get("source_text", ""),
        "method": r["method"],
        "ingredients": r["ingredients"],
        "funky": r.get("funky", []),
        "ingredient_source": r.get("ingredient_source", "sourced"),
        "gloss": r.get("gloss", ""),
    })
RECIPES_JSON = json.dumps(recs, ensure_ascii=False)

# Cuisine families with their blurbs, for the filter panel.
_cfam = {}
for _r in recs:
    _cfam[_r["cuisine"]] = _cfam.get(_r["cuisine"], 0) + 1
CUISINES_JSON = json.dumps(
    [{"key": k, "label": k, "n": _cfam[k], "blurb": FAMILY_BLURB.get(k, "")}
     for k in FAMILY_ORDER if _cfam.get(k)],
    ensure_ascii=False)

# ---------------------------------------------------------- validation pass
problems = []


def validate():
    seen_ids = set()
    for r in ALL_RECIPES:
        rid = r["id"]
        if rid in seen_ids:
            problems.append(f"duplicate recipe id: {rid}")
        seen_ids.add(rid)
        if r["era"] not in ERA_BY_KEY:
            problems.append(f"{rid}: unknown era '{r['era']}'")
        if r["servings"] < 1:
            problems.append(f"{rid}: bad servings")
        if len(r.get("history", "")) < 200:
            problems.append(f"{rid}: history too short ({len(r.get('history',''))} chars)")
        # A recipe may legitimately be one long instruction. What it must
        # not be is empty.
        if len(r.get("method", [])) < 1:
            problems.append(f"{rid}: no method steps")
        if r.get("method") and len(" ".join(r["method"])) < 60:
            problems.append(f"{rid}: method too short to be usable")
        if not r.get("source"):
            problems.append(f"{rid}: no source citation")
        for ing in r["ingredients"]:
            if ing["pantry"] not in PANTRY and ing["pantry"] not in ALIASES:
                problems.append(
                    f"{rid}: ingredient '{ing['name']}' uses unknown pantry "
                    f"key '{ing['pantry']}'")
            if ing.get("qty") is None:
                problems.append(f"{rid}: ingredient '{ing['name']}' has no qty")
            if not isinstance(ing.get("qty"), (int, float)) or ing["qty"] <= 0:
                problems.append(
                    f"{rid}: ingredient '{ing['name']}' has bad qty {ing.get('qty')!r}")
        # every funky ingredient should map to a documented substitute and
        # point at a real ingredient in the recipe
        for f in r.get("funky", []):
            if f["key"] not in SUBSTITUTES and not f.get("sub"):
                problems.append(
                    f"{rid}: funky ingredient '{f['ingredient']}' "
                    f"(key {f['key']}) has no substitute reference")
            if not any(i["name"] == f.get("ing_ref") for i in r["ingredients"]):
                problems.append(
                    f"{rid}: funky '{f['ingredient']}' ing_ref "
                    f"'{f.get('ing_ref')}' matches no ingredient in the recipe")
    # era coverage
    for e in ERA_ORDER:
        n = sum(1 for r in ALL_RECIPES if r["era"] == e)
        if n == 0:
            problems.append(f"era '{e}' has no recipes")
        elif n < 2:
            problems.append(f"era '{e}' has only {n} recipe")
    # every substitute reference should be reachable: either it names a
    # pantry key, or it is a concept-level entry (an oddity that has no
    # single modern pantry item, e.g. "grape must").
    CONCEPT_ONLY = {
        "grapes_must", "powdour_douce", "powdour_fort", "powder_fort",
        "cameline", "sea_hare", "bully_beef", "brain", "thrush",
        "sow_belly", "caul", "gourds", "herbs", "indian_meal",
        "west_india_molasses", "bred_cheese", "hard_biscuit",
        "dehydrated_apple", "catsup_walnut", "mushroom_powder",
        "long_pepper", "grains_paradise", "powdered_malt", "caraway",
        "rose_petals", "sea_hare", "sugar_in_veg",
    }
    for key in SUBSTITUTES:
        if key in CONCEPT_ONLY:
            continue
        if key not in PANTRY and key not in ALIASES:
            problems.append(f"substitute '{key}' has no pantry key")


validate()
if problems:
    print("VALIDATION PROBLEMS:")
    for p in problems:
        print("  -", p)
    sys.exit(1)

print(f"Validation passed: {len(ALL_RECIPES)} recipes across {len(ERA_ORDER)} eras "
      f"({len(RECIPES)} curated + {len(GENERATED)} extracted).")

# ------------------------------------------------------------------ the page
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Historical Kitchen</title>
<meta name="description" content="Cook 2,000 years of history from what you already have in the kitchen. Filter by era, tick your pantry, scale any recipe from 1 to 12 portions.">
<style>
:root{
  --bg:#0b0b0f; --bg2:#121219; --bg3:#181820; --line:#26262f;
  --fg:#e8e6e1; --dim:#9b98a3; --dim2:#6e6b78;
  --amber:#e0a34e; --amber-dim:#8a6430;
  --green:#6fbf73; --red:#e0685f; --blue:#6aa9e0;
  --serif:Georgia,'Iowan Old Style','Times New Roman',serif;
  --sans:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --mono:ui-monospace,'SF Mono',Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:var(--bg); color:var(--fg); font-family:var(--sans);
  font-size:15px; line-height:1.55; -webkit-font-smoothing:antialiased;
  padding:0 0 80px;
}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}

/* ---------- header ---------- */
header{
  border-bottom:1px solid var(--line); padding:34px 0 26px; margin-bottom:22px;
  background:linear-gradient(180deg,#101018 0%,var(--bg) 100%);
}
h1{
  font-family:var(--serif); font-weight:600; font-size:clamp(26px,5.2vw,40px);
  margin:0 0 8px; letter-spacing:-.01em;
}
.sub{color:var(--dim);font-size:15px;max-width:62ch;margin:0 0 20px}
.byline{color:var(--dim2);font-size:12.5px;font-family:var(--mono)}

/* ---------- tabs ---------- */
.tabs{
  display:flex; gap:6px; margin-bottom:16px; border-bottom:1px solid var(--line);
  padding-bottom:0;
}
.tab{
  background:none;border:none;border-bottom:2px solid transparent;
  color:var(--dim);font-family:var(--serif);font-size:16px;font-weight:600;
  padding:9px 14px 10px;cursor:pointer;transition:.13s;
}
.tab:hover{color:var(--fg)}
.tab.on{color:var(--amber);border-bottom-color:var(--amber)}

/* ---------- fiction & fear ---------- */
.food-strip{
  display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px;
}
.food-chip{
  background:var(--bg2);border:1px solid var(--line);border-radius:20px;
  padding:4px 11px;font-size:12.5px;cursor:pointer;color:var(--dim);
  transition:.12s;user-select:none;
}
.food-chip:hover{border-color:#3a3a46;color:var(--fg)}
.food-chip.on{border-color:var(--red);background:#201113;color:#e8b4b0}
.lit{
  background:var(--bg2);border:1px solid var(--line);border-radius:12px;
  margin-bottom:12px;overflow:hidden;transition:border-color .14s;
}
.lit:hover{border-color:#31313c}
.lit-head{padding:15px 17px;cursor:pointer}
.lit-title{
  font-family:var(--serif);font-size:18px;font-weight:600;margin:0 0 5px;
  line-height:1.25;
}
.lit-meta{
  color:var(--dim);font-size:12.5px;font-family:var(--mono);
  display:flex;flex-wrap:wrap;gap:5px 12px;
}
.lit-meta b{color:#c3bfb6;font-weight:600}
.lit-kind{
  display:inline-block;font-size:10.5px;text-transform:uppercase;
  letter-spacing:.09em;padding:2px 7px;border-radius:4px;margin-left:8px;
  vertical-align:2px;font-family:var(--mono);
}
.lit-kind.gothic{background:#2a1013;color:#e09a92;border:1px solid #4a1c20}
.lit-kind.victorian{background:#131f2a;color:#8fc0e0;border:1px solid #1e3346}
.lit-kind.russian{background:#1a1410;color:#d8a878;border:1px solid #33261a}
.lit-kind.romance{background:#1a1420;color:#b49ae0;border:1px solid #2e2340}
.lit-kind.regency{background:#141a14;color:#9fd0a0;border:1px solid #22331f}
.lit-kind.industrial{background:#201a10;color:#d8c088;border:1px solid #362c1a}
.lit-kind.sensation{background:#101a1a;color:#8fd0c8;border:1px solid #1a2e2c}
.lit-kind.sea{background:#0f1620;color:#85a8cc;border:1px solid #182838}
.lit-kind.adventure{background:#1c1a10;color:#c8bc88;border:1px solid #2e2a18}
.lit-foods{
  display:flex;flex-wrap:wrap;gap:5px;margin-top:9px;
}
.lit-food{
  font-size:11.5px;background:#141418;border:1px solid var(--line);
  border-radius:5px;padding:2px 8px;color:var(--dim);font-family:var(--mono);
}
.lit-body{
  display:none;padding:0 17px 18px;border-top:1px solid var(--line);
}
.lit.open .lit-body{display:block}
.lit.open .lit-title{color:var(--amber)}
.lit-passage{
  font-family:var(--serif);font-size:15px;line-height:1.72;color:#c9c5bc;
  margin:16px 0 0;max-width:66ch;
}
.lit-passage::before{content:'"';color:var(--amber-dim);font-size:28px;line-height:0;vertical-align:-6px;margin-right:2px}
.lit-passage::after{content:'"';color:var(--amber-dim);font-size:28px;line-height:0;vertical-align:-8px;margin-left:2px}
.lit-cite{
  display:block;margin-top:12px;font-family:var(--mono);font-size:11.5px;
  color:var(--dim2);
}
.lit-why{
  margin-top:14px;font-size:13.5px;color:var(--dim);border-left:2px solid
  var(--line);padding-left:12px;max-width:66ch;
}

/* ---------- era rail ---------- */
.era-rail-wrap{position:relative}
.era-rail{
  display:flex; gap:8px; overflow-x:auto; padding:2px 0 14px;
  scrollbar-width:thin; -webkit-overflow-scrolling:touch;
  scroll-snap-type:x proximity;
}
.era-rail::-webkit-scrollbar{height:5px}
.era-rail::-webkit-scrollbar-thumb{background:var(--line);border-radius:3px}
.era-rail::after{
  content:'';position:sticky;right:0;top:0;flex:0 0 40px;align-self:stretch;
  background:linear-gradient(90deg,rgba(11,11,15,0),var(--bg) 70%);
  pointer-events:none;margin-left:-40px;
}
.era{
  flex:0 0 auto; background:var(--bg2); border:1px solid var(--line);
  border-radius:9px; padding:9px 14px; cursor:pointer; min-width:118px;
  transition:border-color .13s, background .13s; user-select:none;
  scroll-snap-align:start;
}
.era:hover{border-color:#3a3a46}
.era.on{border-color:var(--amber); background:#1d1811}
.era .el{display:block;font-weight:600;font-size:14px;color:var(--fg)}
.era.on .el{color:var(--amber)}
.era .es{display:block;font-size:11px;color:var(--dim2);font-family:var(--mono);margin-top:2px}
.era .ec{display:block;font-size:11px;color:var(--dim2);margin-top:3px}

/* ---------- toolbar ---------- */
.toolbar{
  display:flex; flex-wrap:wrap; gap:12px; align-items:center;
  background:var(--bg2); border:1px solid var(--line); border-radius:11px;
  padding:13px 15px; margin-bottom:18px; position:sticky; top:0; z-index:40;
  backdrop-filter:blur(8px);
}
.tb-group{display:flex;align-items:center;gap:8px}
.tb-label{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--dim2);font-family:var(--mono)}
.seg{display:flex;background:var(--bg3);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.seg button{
  background:none;border:none;color:var(--dim);font-family:var(--mono);font-size:12.5px;
  padding:6px 10px;cursor:pointer;border-right:1px solid var(--line);
  white-space:nowrap;
}
.seg button:last-child{border-right:none}
.seg button:hover{color:var(--fg);background:#1e1e27}
.seg button.on{background:var(--amber);color:#17120a;font-weight:700}
.ghost{
  background:var(--bg3);border:1px solid var(--line);color:var(--dim);
  border-radius:8px;padding:7px 13px;cursor:pointer;font-size:13px;font-family:var(--sans);
}
.ghost:hover{color:var(--fg);border-color:#3a3a46}
.ghost.on{border-color:var(--amber);color:var(--amber)}

/* ---------- pantry drawer ---------- */
.pantry-panel{
  background:var(--bg2); border:1px solid var(--line); border-radius:11px;
  padding:16px; margin-bottom:18px; display:none;
}
.pantry-panel.open{display:block}
.pp-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.pp-head h3{font-family:var(--serif);font-size:18px;margin:0;font-weight:600}
.pp-head p{margin:0;color:var(--dim);font-size:13px}
.cat{margin-bottom:14px}
.cat h4{
  font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--dim2);
  margin:0 0 7px;font-family:var(--mono);font-weight:600;
}
.cat-grid{display:flex;flex-wrap:wrap;gap:6px}
.chip{
  display:inline-flex;align-items:center;gap:6px;background:var(--bg3);
  border:1px solid var(--line);border-radius:20px;padding:5px 11px;
  font-size:12.5px;cursor:pointer;user-select:none;transition:.12s;
}
.chip:hover{border-color:#3a3a46}
.chip.on{border-color:var(--green);background:#12200f;color:#cfe6c4}
.chip .dot{width:7px;height:7px;border-radius:50%;background:#3a3a46;flex:0 0 auto}
.chip.on .dot{background:var(--green)}

/* ---------- recipe cards ---------- */
.era-blurb{
  background:linear-gradient(135deg,#15130f,#12121a);border:1px solid var(--amber-dim);
  border-radius:11px;padding:15px 17px;margin-bottom:20px;
}
.era-blurb h2{font-family:var(--serif);font-size:20px;margin:0 0 3px;color:var(--amber);font-weight:600}
.era-blurb .span{font-family:var(--mono);font-size:11.5px;color:var(--dim2);margin-bottom:8px}
.era-blurb p{margin:0;color:#cbc7be;font-size:14px;max-width:70ch}

.count{color:var(--dim2);font-size:13px;font-family:var(--mono);margin:0 0 14px}

.card{
  background:var(--bg2); border:1px solid var(--line); border-radius:12px;
  margin-bottom:14px; overflow:hidden; transition:border-color .14s;
}
.card:hover{border-color:#31313c}
.card.hit{border-color:var(--green)}
.card-head{padding:15px 17px;cursor:pointer;display:flex;gap:14px;align-items:flex-start}
.ch-head{flex:1 1 auto;min-width:0}
.ch-title{font-family:var(--serif);font-size:19px;font-weight:600;margin:0 0 5px;line-height:1.25}
.ch-meta{color:var(--dim);font-size:12.5px;font-family:var(--mono);display:flex;flex-wrap:wrap;gap:5px 12px}
.ch-meta b{color:#c3bfb6;font-weight:600}
.score{
  flex:0 0 auto;text-align:right;font-family:var(--mono);font-size:11.5px;
  color:var(--dim2);padding-top:2px;min-width:92px;
}
.score .pct{display:block;font-size:19px;font-weight:700;color:var(--green);line-height:1.1}
.score .pct.mid{color:var(--amber)}
.score .pct.low{color:var(--red)}
.score .miss{display:block;font-size:11px;margin-top:3px;color:var(--dim)}
.miss-list{color:var(--red)}
.card-body{display:none;padding:0 17px 18px;border-top:1px solid var(--line)}
.card.open .card-body{display:block}
.card.open .ch-title{color:var(--amber)}

.sec{margin-top:18px}
.sec h4{
  font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:var(--dim2);
  margin:0 0 8px;font-family:var(--mono);font-weight:600;
  padding-bottom:5px;border-bottom:1px solid var(--line);
}
.hist{font-size:14.5px;color:#d5d2cb;max-width:70ch}
.hist em{color:var(--amber);font-style:normal;font-weight:600}
.quote{
  font-family:var(--serif);font-size:14px;color:#bdb9b0;background:#0e0e13;
  border-left:2px solid var(--amber-dim);padding:11px 15px;margin:0;
  white-space:pre-line; line-height:1.6;
}
.quote .cite{display:block;margin-top:9px;font-family:var(--mono);font-size:11.5px;color:var(--dim2);font-style:normal}

/* substitutes */
.subs{display:flex;flex-direction:column;gap:9px}
.sub{
  background:#12120f;border:1px solid #2a2620;border-radius:9px;padding:11px 13px;
}
.sub .sw{font-weight:600;font-size:14px;color:var(--amber);margin-bottom:4px}
.sub .sn{font-size:13.5px;color:#c6c2ba;margin-bottom:6px}
.sub .sd{font-size:13px;color:var(--dim);margin-bottom:5px}
.sub .src{font-size:11px;color:var(--dim2);font-family:var(--mono)}

/* ingredients */
.ing-list{display:flex;flex-direction:column;gap:0}
.ing{
  display:flex;gap:11px;align-items:baseline;padding:8px 0;
  border-bottom:1px solid #1c1c24; font-size:14px;
}
.ing:last-child{border-bottom:none}
.ing .have{
  flex:0 0 17px;height:17px;border-radius:4px;border:1px solid var(--line);
  background:var(--bg3);position:relative;align-self:center;
}
.ing.have .have{border-color:var(--green);background:#12200f}
.ing.have .have::after{
  content:'';position:absolute;left:5px;top:2px;width:5px;height:9px;
  border:solid var(--green);border-width:0 2px 2px 0;transform:rotate(42deg);
}
.ing .qty{
  flex:0 0 96px;font-family:var(--mono);font-size:13px;color:var(--amber);
  font-weight:600;
}
.ing .nm{flex:1 1 auto;min-width:0}
.ing .nm .n{color:var(--fg)}
.ing .nm .note{display:block;font-size:12px;color:var(--dim2);margin-top:2px}
.ing.missing .n{color:var(--dim)}
.ing .miss-note{color:var(--red);font-size:12.5px;display:block;margin-top:3px}
.ing .sub-line{color:var(--green);font-size:12.5px;display:block;margin-top:3px}
.ing.optional .n{color:var(--dim)}
.tag-opt{font-size:10.5px;color:var(--dim2);font-family:var(--mono);border:1px solid var(--line);border-radius:4px;padding:1px 5px;margin-left:6px}

/* scale */
.scale-bar{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  background:var(--bg3);border:1px solid var(--line);border-radius:9px;
  padding:10px 13px;margin-top:15px;
}
.scale-bar .lbl{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--dim2);font-family:var(--mono)}
.stepper{display:flex;align-items:center;gap:0;background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.stepper button{
  background:none;border:none;color:var(--dim);font-size:17px;width:32px;height:31px;cursor:pointer;
}
.stepper button:hover{background:#22222c;color:var(--fg)}
.stepper .val{
  min-width:52px;text-align:center;font-family:var(--mono);font-size:14px;font-weight:700;color:var(--amber);
  border-left:1px solid var(--line);border-right:1px solid var(--line);padding:6px 0;
}
.presets{display:flex;gap:5px;flex-wrap:wrap}
.presets button{
  background:var(--bg);border:1px solid var(--line);color:var(--dim);border-radius:7px;
  padding:5px 10px;font-family:var(--mono);font-size:12px;cursor:pointer;
}
.presets button:hover{color:var(--fg);border-color:#3a3a46}
.presets button.on{background:var(--amber);color:#17120a;border-color:var(--amber);font-weight:700}

/* method */
ol.method{margin:0;padding-left:20px}
ol.method li{margin-bottom:8px;font-size:14px;color:#cfccc5;max-width:72ch}
ol.method li::marker{color:var(--amber);font-family:var(--mono);font-size:12px}

/* footer */
footer{border-top:1px solid var(--line);margin-top:34px;padding-top:20px;color:var(--dim2);font-size:12.5px}
footer a{color:var(--amber);text-decoration:none}
footer a:hover{text-decoration:underline}
.srch{
  width:100%;max-width:300px;background:var(--bg3);border:1px solid var(--line);
  border-radius:8px;padding:7px 11px;color:var(--fg);font-family:var(--sans);font-size:13.5px;
}
.srch:focus{outline:none;border-color:var(--amber)}
.srch::placeholder{color:var(--dim2)}
.empty{padding:34px 16px;text-align:center;color:var(--dim2);font-size:14px}
.hidden{display:none !important}

/* ---------- mobile ---------- */
@media(max-width:640px){
  body{font-size:14.5px}
  .wrap{padding:0 12px}
  header{padding:24px 0 20px}
  .toolbar{padding:11px 12px;gap:9px}
  /* the era chip row is wider than a phone: let it scroll sideways
     instead of pushing the page wide */
  .tb-group{max-width:100%;min-width:0;flex:1 1 auto}
  .tb-group .seg{overflow-x:auto;max-width:100%;-webkit-overflow-scrolling:touch}
  .tb-group .seg::-webkit-scrollbar{height:0}
  .toolbar{flex-wrap:wrap;min-width:0}
  .toolbar > .tb-group:last-child{margin-left:auto !important;flex:0 0 auto}
  .card-head{padding:13px 14px;gap:10px}
  .ch-title{font-size:17px}
  .score{min-width:74px}
  .score .pct{font-size:17px}
  .card-body{padding:0 14px 16px}
  .ing .qty{flex:0 0 82px;font-size:12.5px}
  .ing{font-size:13.5px;gap:9px}
  .era{min-width:104px;padding:8px 11px}
  .era .el{font-size:13px}
  .scale-bar{gap:8px;padding:9px 11px}
  .presets button{padding:5px 8px;font-size:11.5px}
  .pp-head{flex-direction:column;align-items:flex-start;gap:6px}
  .byline{font-size:11.5px}
  /* the fiction tab has its own two chip rows plus a food strip */
  .tab{font-size:14.5px;padding:8px 10px 9px}
  .food-strip{gap:5px;max-height:none}
  .food-chip{padding:4px 9px;font-size:12px}
  .lit-head{padding:13px 14px}
  .lit-title{font-size:16.5px}
  .lit-body{padding:0 14px 16px}
  .lit-passage{font-size:14.5px;line-height:1.68}
  .lit-kind{margin-left:0;display:inline-block;margin-top:4px}
}
@media(max-width:380px){
  .score{min-width:64px;font-size:11px}
  .score .miss{display:none}
}
</style>
</head>
<body>

<header>
  <div class="wrap">
    <h1>The Historical Kitchen</h1>
    <p class="sub">Two thousand years of real recipes, filtered by era, matched to
      what is already in your kitchen — and scaled to the table you are actually
      cooking for.</p>
    <p class="byline"><span id="recipeCount">__COUNT__</span> &middot; Ancient to post-war
      &middot; every recipe traced to a primary source</p>
  </div>
</header>

<div class="wrap">

  <!-- ============================ TABS ============================ -->
  <div class="tabs" id="tabs">
    <button class="tab on" data-tab="recipes">Recipes</button>
    <button class="tab" data-tab="fiction">Fiction &amp; Fear</button>
  </div>

  <!-- ============================ ERA RAIL ============================ -->
  <div class="era-rail-wrap" id="recipesTab">
    <div class="era-rail" id="eraRail"></div>
  </div>

  <div class="era-blurb" id="eraBlurb"></div>

  <!-- ============================ TOOLBAR ============================ -->
  <div class="toolbar">
    <div class="tb-group">
      <span class="tb-label">Era</span>
      <div class="seg" id="eraSeg"></div>
    </div>
    <div class="tb-group" id="cuisineGroup">
      <span class="tb-label">Cuisine</span>
      <div class="seg" id="cuisineSeg"></div>
    </div>
    <div class="tb-group" style="margin-left:auto">
      <button class="ghost" id="pantryToggle">My pantry</button>
      <button class="ghost" id="resetBtn">Reset</button>
    </div>
  </div>

  <!-- ============================ PANTRY ============================ -->
  <div class="pantry-panel" id="pantryPanel">
    <div class="pp-head">
      <div>
        <h3>What's in your kitchen?</h3>
        <p>Tick what you have. Recipes re-sort by how well you can make them right now.</p>
      </div>
      <div class="tb-group">
        <button class="ghost" id="pantryAll">Select all staples</button>
        <button class="ghost" id="pantryNone">Clear</button>
      </div>
    </div>
    <div id="pantryCats"></div>
  </div>

  <div class="count" id="count"></div>
  <div id="results"></div>

  <!-- ============================ FICTION & FEAR ============================ -->
  <div id="fictionTab" style="display:none">
    <div class="era-blurb" id="fictionBlurb"></div>
    <div class="toolbar">
      <div class="tb-group">
        <span class="tb-label">Genre</span>
        <div class="seg" id="kindSeg"></div>
      </div>
      <div class="tb-group">
        <span class="tb-label">Book</span>
        <div class="seg" id="bookSeg"></div>
      </div>
      <div class="tb-group" style="margin-left:auto">
        <button class="ghost" id="foodBtn">All foods</button>
      </div>
    </div>
    <div class="food-strip" id="foodStrip"></div>
    <div class="count" id="fictionCount"></div>
    <div id="fictionResults"></div>
  </div>

</div>

<footer class="wrap">
  <p><strong>Sources.</strong> Recipes are transcribed from primary texts read in
  full: <em>Apicius, De Re Coquinaria</em> (c. 400 CE); <em>The Forme of Cury</em>
  (c. 1390, ed. Pegge 1780); <em>The Virginia House-Wife</em> (Randolph, 1824);
  <em>Modern Cookery</em> (Acton, 1845); <em>Book of Household Management</em>
  (Beeton, 1861); <em>The American Frugal Housewife</em> (Child, 1832); and
  Max Miller's Tasting History, which supplied the Sackler, Roman, Medieval and
  wartime material.</p>
  <p>Original spellings are kept where the source's wording is quoted. Quantities
  are modernised for a home kitchen; the source wording is shown alongside so you
  can see what changed. Where a period ingredient is genuinely unobtainable, the
  modern stand-in is named with a citation — silphium is the famous one, and it
  is, for once, genuinely extinct.</p>
  <p style="color:var(--dim2)">Built by aiFrado. Single file, no tracking, works offline.</p>
</footer>

<script>
const ERAS = __ERAS__;
const RECIPES = __RECIPES__;
const PANTRY = __PANTRY__;
const CATEGORIES = __CATEGORIES__;
const DEFAULT_PANTRY = __DEFAULT__;
const NEAR = __NEAR__;
const SUBS = __SUBS__;
const ALIASES = __ALIASES__;
const ERA_ORDER = ERAS.map(e => e.key);
const ERA_BY_KEY = Object.fromEntries(ERAS.map(e => [e.key, e]));

/* ---------------- state ---------------- */
const STORE_KEY = 'historical-kitchen-pantry-v1';
let state = {
  era: 'all',
  cuisine: 'all',
  portions: 4,
  sort: 'match',
  onlyHave: false,
  pantry: new Set(),
  open: new Set(),
  tab: 'recipes',
  kind: 'all',
  book: 'all',
  food: '',
};
let pantryLoaded = false;

function loadPantry(){
  try{
    const raw = localStorage.getItem(STORE_KEY);
    if(raw){
      const arr = JSON.parse(raw);
      if(Array.isArray(arr)){ state.pantry = new Set(arr); pantryLoaded = true; return; }
    }
  }catch(e){ /* storage may be unavailable; fall through to defaults */ }
  state.pantry = new Set(DEFAULT_PANTRY);
  pantryLoaded = true;
}
function savePantry(){
  try{ localStorage.setItem(STORE_KEY, JSON.stringify([...state.pantry])); }catch(e){}
}

/* ---------------- units ---------------- */
const ML_PER = {
  ml:1, l:1000, tbsp:15, tsp:5, cup:240, quart:946, pint:473,
  gallon:3785, gill:118, sextarius:550
};
const PLURAL = {
  g:'g', kg:'kg', ml:'ml', l:'L', ea:'', tbsp:'tbsp', tsp:'tsp',
  cup:'cups', quart:'qt', pint:'pt', gallon:'gal', gill:'gill',
  sextarius:'sextarii', handful:'handfuls', pinch:'pinches', dozen:'dozen',
  lb:'lb', oz:'oz'
};

/* Format a scaled quantity nicely, switching to the retail unit when the
   scaled number gets silly (e.g. 900 g of butter -> 225 g x 4). */
function fmtQty(qty, unit, factor){
  const v = qty * factor;
  const u = PLURAL[unit] !== undefined ? PLURAL[unit] : unit;
  if(unit === 'ea'){
    const n = Math.abs(v - Math.round(v)) < 0.02 ? Math.round(v) : Math.round(v*10)/10;
    return n + '';
  }
  if(unit === 'kg') return (Math.round(v*1000)/1000) + ' kg';
  if(unit === 'l')  return (Math.round(v*100)/100) + ' L';
  if(unit === 'lb') return (Math.round(v*100)/100) + ' lb';
  if(unit === 'oz') return (Math.round(v*10)/10) + ' oz';
  if(unit === 'g'){
    if(v >= 1000) return (Math.round(v/10)/100) + ' kg';
    return (Math.round(v*10)/10) + ' g';
  }
  if(unit === 'ml'){
    if(v >= 1000) return (Math.round(v/10)/100) + ' L';
    return (Math.round(v*10)/10) + ' ml';
  }
  // spoons, cups, etc: use fractions
  const fr = frac(v);
  return fr.n + ' ' + u;
}
function frac(v){
  const whole = Math.floor(v);
  const rem = v - whole;
  const table = [[0.125,'1/8'],[0.25,'1/4'],[0.333,'1/3'],[0.5,'1/2'],[0.667,'2/3'],[0.75,'3/4']];
  let bf = 0, bl = '';
  for(const [r,l] of table){
    if(Math.abs(rem - r) < 0.03){ bf = r; bl = l; break; }
  }
  if(!bl) return {n: Math.round(v*100)/100, d:''};
  if(whole === 0) return {n: bl, d:''};
  return {n: whole + ' ' + bl, d:''};
}

/* Retail re-expression: for a scaled amount, also give the number of
   retail units (tins, sticks, jars) where that is the natural buy. */
function retailHint(qty, unit, factor){
  const v = qty * factor;
  if(unit === 'g'){
    if(v >= 400 && v <= 700) return Math.round(v/225) + ' stick(s) of butter';
    if(v >= 450 && v <= 500) return 'one 450 g pack';
    if(v >= 900 && v <= 1000) return 'one 1 kg bag';
  }
  if(unit === 'ml'){
    if(v >= 900 && v <= 1000) return 'one 1 litre carton/bottle';
    if(v >= 230 && v <= 260) return 'one 240 ml cup';
  }
  return '';
}

/* ---------------- matching ---------------- */
function has(key){
  if(state.pantry.has(key)) return true;
  // an alias counts as the same thing (e.g. 'heavy_cream' -> 'cream')
  const al = ALIASES;
  for(const alias in al){ if(al[alias] === key && state.pantry.has(alias)) return true; }
  return false;
}
function nearEquivalents(key){
  return NEAR[key] || [];
}
function subFor(ing){
  if(ing.sub) return {sub: ing.sub, note: ing.note || ''};
  if(ing.historic && SUBS[ing.pantry]) return {sub: SUBS[ing.pantry].sub, note: ing.note || ''};
  return null;
}
function scoreRecipe(r){
  let have = 0, total = 0, missing = [], missingHard = 0;
  for(const ing of r.ingredients){
    if(ing.optional) continue;
    total++;
    if(has(ing.pantry)) have++;
    else {
      missing.push(ing);
      // a near-equivalent on the shelf softens the penalty
      const eq = nearEquivalents(ing.pantry).find(e => has(e[0]));
      if(eq) have += 0.75;
      else missingHard++;
    }
  }
  const pct = total ? Math.round((have/total)*100) : 100;
  return {pct, missing, missingHard, have, total};
}
function sortRecipes(list){
  const scored = list.map(r => ({r, s: scoreRecipe(r)}));
  if(state.sort === 'match'){
    scored.sort((a,b) => b.s.pct - a.s.pct || a.r.year.localeCompare(b.r.year));
  } else if(state.sort === 'era'){
    scored.sort((a,b) => {
      const ea = ERA_ORDER.indexOf(a.r.era), eb = ERA_ORDER.indexOf(b.r.era);
      return ea - eb || a.r.year.localeCompare(b.r.year);
    });
  } else {
    scored.sort((a,b) => a.r.title.localeCompare(b.r.title));
  }
  return scored;
}

/* ---------------- rendering ---------------- */
function el(tag, cls, html){
  const e = document.createElement(tag);
  if(cls) e.className = cls;
  if(html !== undefined) e.innerHTML = html;
  return e;
}
function esc(s){
  return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}

function renderEraRail(){
  const rail = document.getElementById('eraRail');
  rail.innerHTML = '';
  const all = el('div','era' + (state.era==='all'?' on':''));
  all.innerHTML = '<span class="el">All eras</span><span class="es">2000 BCE - 1946</span>' +
    '<span class="ec">' + RECIPES.length + ' recipes</span>';
  all.onclick = () => { state.era = 'all'; renderAll(); };
  rail.appendChild(all);
  for(const e of ERAS){
    const n = RECIPES.filter(r => r.era === e.key).length;
    const d = el('div','era' + (state.era===e.key?' on':''));
    d.innerHTML = '<span class="el">' + esc(e.label) + '</span><span class="es">' + esc(e.span) + '</span>' +
      '<span class="ec">' + n + ' recipe' + (n===1?'':'s') + '</span>';
    d.onclick = () => { state.era = e.key; renderAll(); };
    rail.appendChild(d);
  }
  // keep the selected era visible when it is chosen from the chip row
  if(state.era !== 'all' && rail.scrollWidth > rail.clientWidth){
    const sel = rail.querySelector('.era.on');
    if(sel) sel.scrollIntoView({inline:'center', block:'nearest', behavior:'smooth'});
  }
}

function renderEraSeg(){
  const seg = document.getElementById('eraSeg');
  seg.innerHTML = '';
  const mk = (label, val) => {
    const b = el('button', state.era===val?'on':'');
    b.textContent = label;
    b.onclick = () => { state.era = val; renderAll(); };
    seg.appendChild(b);
  };
  mk('All','all');
  for(const e of ERAS) mk(e.label, e.key);
}

/* ---------------- cuisine axis ----------------
   A second way in: not "when" but "where".  Each recipe carries a
   cuisine family, derived from its region string at build time. */
const CUISINE_LIST = __CUISINES__;

function renderCuisineSeg(){
  const seg = document.getElementById('cuisineSeg');
  if(!seg) return;
  seg.innerHTML = '';
  const mk = (label, val, n) => {
    const b = el('button', state.cuisine===val?'on':'');
    b.textContent = n ? label + ' (' + n + ')' : label;
    b.onclick = () => { state.cuisine = val; renderAll(); };
    seg.appendChild(b);
  };
  mk('Any','all');
  for(const c of CUISINE_LIST) mk(c.label, c.key, c.n);
}

function renderEraBlurb(){
  const box = document.getElementById('eraBlurb');
  box.innerHTML = '';
  if(state.cuisine !== 'all'){
    const c = CUISINE_LIST.find(x => x.key === state.cuisine);
    box.innerHTML = '<h2>' + esc(state.cuisine) + '</h2>' +
      '<div class="span">' + (c ? c.n : 0) + ' recipes</div>' +
      '<p>' + esc(c ? c.blurb : '') + ' Where the era tells you when a ' +
      'dish was cooked, the cuisine tells you what it was cooking &mdash; ' +
      'and for a hundred years of European food writing those were ' +
      'different questions with different answers.</p>';
    return;
  }
  if(state.era === 'all'){
    box.innerHTML = '<h2>All eras</h2><div class="span">c. 2000 BCE - 1946</div>' +
      '<p>Every recipe in the collection. Pick an era above to narrow it down — ' +
      'the eras are the spine of the book, and each one has its own pantry, ' +
      'its own set of missing ingredients, and its own idea of what dinner was for.</p>';
  } else {
    const e = ERA_BY_KEY[state.era];
    box.innerHTML = '<h2>' + esc(e.label) + '</h2><div class="span">' + esc(e.span) + '</div>' +
      '<p>' + esc(e.blurb) + '</p>';
  }
}

function renderPantry(){
  const host = document.getElementById('pantryCats');
  host.innerHTML = '';
  const cats = {};
  for(const k in PANTRY){
    const c = PANTRY[k].cat;
    (cats[c] = cats[c] || []).push(k);
  }
  for(const c of CATEGORIES){
    const cat = c.cat, label = c.label;
    if(!cats[cat]) continue;
    const div = el('div','cat');
    div.appendChild(el('h4', null, label));
    const grid = el('div','cat-grid');
    for(const k of cats[cat]){
      const chip = el('div','chip' + (state.pantry.has(k)?' on':''));
      chip.innerHTML = '<span class="dot"></span>' + esc(PANTRY[k].label);
      chip.onclick = () => {
        if(state.pantry.has(k)) state.pantry.delete(k); else state.pantry.add(k);
        savePantry();
        renderPantry();
        renderResults();
      };
      grid.appendChild(chip);
    }
    div.appendChild(grid);
    host.appendChild(div);
  }
}

function renderResults(){
  const host = document.getElementById('results');
  host.innerHTML = '';
  const countEl = document.getElementById('count');

  let list = RECIPES.filter(r => state.era === 'all' || r.era === state.era);
  if(state.cuisine !== 'all'){
    list = list.filter(r => r.cuisine === state.cuisine);
  }
  const scored = sortRecipes(list);
  const filtered = state.onlyHave ? scored.filter(x => x.s.missingHard === 0) : scored;

  countEl.innerHTML = filtered.length + ' recipe' + (filtered.length===1?'':'s') +
    ' shown' + (state.onlyHave ? ' &middot; only what you can make now' : '');

  // sort control
  const sortBar = el('div','toolbar');
  sortBar.style.marginBottom = '12px';
  const sg = el('div','tb-group');
  sg.appendChild(el('span','tb-label','Sort'));
  const seg = el('div','seg');
  for(const [lab,val] of [['Best match','match'],['By era','era'],['A-Z','title']]){
    const b = el('button', state.sort===val?'on':'');
    b.textContent = lab;
    b.onclick = () => { state.sort = val; renderResults(); };
    seg.appendChild(b);
  }
  sg.appendChild(seg);
  sortBar.appendChild(sg);

  const og = el('div','tb-group');
  og.style.marginLeft = 'auto';
  const ob = el('button','ghost' + (state.onlyHave?' on':''));
  ob.textContent = 'Only show what I can make';
  ob.onclick = () => { state.onlyHave = !state.onlyHave; renderResults(); };
  og.appendChild(ob);
  sortBar.appendChild(og);
  host.appendChild(sortBar);

  if(!filtered.length){
    host.appendChild(el('div','empty',
      'No recipes match that filter. Try switching eras, or tick a few more pantry items.'));
    return;
  }

  // With over a thousand recipes, rendering every card at once is slow
  // on a phone. Render the first batch, then the rest in chunks as the
  // user reaches the bottom.
  const BATCH = 60;
  let shown = 0;
  const more = el('div','empty');
  more.style.cssText = 'padding:18px;cursor:pointer';

  function drawBatch(){
    const slice = filtered.slice(shown, shown + BATCH);
    if(!slice.length) return;
    const frag = document.createDocumentFragment();
    for(const {r, s} of slice){
      frag.appendChild(renderCard(r, s));
    }
    host.appendChild(frag);
    shown += slice.length;
    if(shown < filtered.length){
      more.textContent = 'Showing ' + shown + ' of ' + filtered.length +
        ' — tap to load more';
      if(!more.parentNode) host.appendChild(more);
    } else {
      more.remove();
    }
  }
  more.onclick = drawBatch;
  drawBatch();
}

function renderCard(r, s){
  const card = el('div','card' + (s.missingHard===0 ? ' hit':''));
  if(state.open.has(r.id)) card.classList.add('open');

  const head = el('div','card-head');
  const ch = el('div','ch-head');
  ch.appendChild(el('h3','ch-title', esc(r.title)));

  const meta = el('div','ch-meta');
  meta.innerHTML =
    '<span>' + esc(ERA_BY_KEY[r.era].label) + '</span>' +
    '<span><b>' + esc(r.year) + '</b></span>' +
    '<span>' + esc(r.cuisine || r.region) + '</span>' +
    '<span>' + esc(r.source.split(',')[0]) + '</span>';
  ch.appendChild(meta);
  head.appendChild(ch);

  const sc = el('div','score');
  const cls = s.pct >= 85 ? '' : (s.pct >= 60 ? 'mid' : 'low');
  sc.innerHTML = '<span class="pct ' + cls + '">' + s.pct + '%</span>' +
    '<span class="miss">' + (s.missingHard ? s.missingHard + ' to buy' : 'you have it') + '</span>';
  head.appendChild(sc);

  head.onclick = () => {
    if(state.open.has(r.id)) state.open.delete(r.id); else state.open.add(r.id);
    card.classList.toggle('open');
  };
  card.appendChild(head);

  const body = el('div','card-body');
  buildBody(body, r, s);
  card.appendChild(body);
  return card;
}

function buildBody(body, r, s){
  const factor = state.portions / r.servings;

  // ---- history
  const hs = el('div','sec');
  hs.appendChild(el('h4', null, 'The story'));
  hs.appendChild(el('p','hist', esc(r.history)));
  body.appendChild(hs);

  // ---- source quote
  if(r.source_text){
    const qs = el('div','sec');
    qs.appendChild(el('h4', null, 'From the source'));
    const q = el('blockquote','quote', esc(r.source_text) +
      '<span class="cite">' + esc(r.source) + '</span>');
    qs.appendChild(q);
    body.appendChild(qs);
  }

  // ---- funky ingredients / modern substitutes
  if(r.funky.length){
    const fs = el('div','sec');
    fs.appendChild(el('h4', null, 'Period oddities &amp; what to use today'));
    const wrap = el('div','subs');
    for(const f of r.funky){
      const ref = SUBS[f.key];
      const box = el('div','sub');
      let html = '<div class="sw">' + esc(f.ingredient) + '</div>';
      html += '<div class="sn">' + esc(f.why) + '</div>';
      if(ref){
        html += '<div class="sd"><strong style="color:var(--green)">Use instead:</strong> ' + esc(ref.sub) + '</div>';
        html += '<div class="sd">' + esc(ref.note) + '</div>';
        if(ref.source) html += '<div class="src">' + esc(ref.source) + '</div>';
      } else {
        // fall back to the ingredient's own sub field
        const ing = r.ingredients.find(i => i.pantry === f.key && i.sub);
        if(ing){
          html += '<div class="sd"><strong style="color:var(--green)">Use instead:</strong> ' + esc(ing.sub) + '</div>';
        }
      }
      box.innerHTML = html;
      wrap.appendChild(box);
    }
    fs.appendChild(wrap);
    body.appendChild(fs);
  }

  // ---- ingredients
  const is = el('div','sec');
  const ingHead = 'Ingredients &mdash; ' + state.portions + ' portion' + (state.portions===1?'':'s');
  is.appendChild(el('h4', null, ingHead));
  if(r.ingredient_source === 'reconstructed'){
    const warn = el('p');
    warn.style.cssText = 'font-size:12.5px;color:var(--dim2);margin:-4px 0 10px';
    warn.innerHTML = 'This book does not print an ingredient list. The list below was ' +
      'read out of the method text, and the quantities are a modern cook\\u2019s ' +
      'sensible defaults rather than the book\\u2019s own.';
    is.appendChild(warn);
  }
  if(r.gloss){
    const gl = el('p');
    gl.style.cssText = 'font-size:13px;color:var(--amber);margin:-4px 0 10px';
    gl.innerHTML = '<em>' + esc(r.gloss) + '</em>';
    is.appendChild(gl);
  }
  const list = el('div','ing-list');
  for(const ing of r.ingredients){
    const have = has(ing.pantry);
    const eq = have ? null : nearEquivalents(ing.pantry).find(e => has(e[0]));
    const row = el('div','ing' + (have?' have':'') + (!have && !eq ? ' missing':'') + (ing.optional?' optional':''));
    let html = '<span class="have"></span>';
    html += '<span class="qty">' + esc(fmtQty(ing.qty, ing.unit, factor)) + '</span>';
    html += '<span class="nm"><span class="n">' + esc(ing.name);
    if(ing.optional) html += '<span class="tag-opt">optional</span>';
    html += '</span>';
    if(ing.note) html += '<span class="note">' + esc(ing.note) + '</span>';
    if(!have && eq){
      html += '<span class="sub-line">Have ' + esc(eq[1]) + ' instead</span>';
    } else if(!have){
      const sub = subFor(ing);
      if(sub && sub.sub) html += '<span class="sub-line">No ' + esc(ing.name.toLowerCase()) +
        '? Use ' + esc(sub.sub) + '</span>';
      else html += '<span class="miss-note">Not in your pantry</span>';
    }
    const rh = retailHint(ing.qty, ing.unit, factor);
    if(rh) html += '<span class="note">' + esc(rh) + '</span>';
    row.innerHTML = html;
    list.appendChild(row);
  }
  is.appendChild(list);
  body.appendChild(is);

  // ---- scale control
  const sb = el('div','scale-bar');
  sb.appendChild(el('span','lbl','Portions'));
  const st = el('div','stepper');
  const minus = el('button', null, '&minus;');
  minus.onclick = () => { state.portions = Math.max(1, state.portions-1); renderResults(); };
  const val = el('div','val', String(state.portions));
  const plus = el('button', null, '+');
  plus.onclick = () => { state.portions = Math.min(12, state.portions+1); renderResults(); };
  st.appendChild(minus); st.appendChild(val); st.appendChild(plus);
  sb.appendChild(st);

  const pr = el('div','presets');
  for(const p of [2,4,6,8,12]){
    const b = el('button', state.portions===p?'on':'');
    b.textContent = p;
    b.onclick = () => { state.portions = p; renderResults(); };
    pr.appendChild(b);
  }
  sb.appendChild(pr);
  const note = el('span');
  note.style.cssText = 'font-size:12px;color:var(--dim2);font-family:var(--mono)';
  note.textContent = 'base recipe: ' + r.servings;
  sb.appendChild(note);
  body.appendChild(sb);

  // ---- method
  const ms = el('div','sec');
  ms.appendChild(el('h4', null, 'Method'));
  const ol = el('ol','method');
  for(const step of r.method){
    const li = el('li', null, esc(step));
    ol.appendChild(li);
  }
  ms.appendChild(ol);
  body.appendChild(ms);

  // ---- provenance
  const ps = el('div','sec');
  ps.appendChild(el('h4', null, 'Provenance'));
  let ph = '<p class="hist" style="font-size:13.5px">' + esc(r.source);
  if(r.source_url) ph += ' &middot; <a href="' + esc(r.source_url) +
    '" target="_blank" rel="noopener" style="color:var(--amber)">source</a>';
  ph += '<br>Confidence: <b style="color:var(--dim)">' + esc(r.confidence) + '</b>';
  if(r.tags && r.tags.length) ph += ' &middot; ' + esc(r.tags.join(', '));
  ph += '</p>';
  ps.innerHTML = ph;
  body.appendChild(ps);
}

/* ---------------- fiction & fear ----------------
   The novels are not a cookbook.  They are the other kind of evidence:
   what was served, in what room, to what mood.  We keep them separate
   and honest about what they are. */
const FICTION = __FICTION__;

const KIND_LABEL = {
  gothic: 'Gothic', victorian: 'Victorian', russian: 'Russian',
  romance: 'Romance', regency: 'Regency', industrial: 'Industrial',
  sensation: 'Sensation', sea: 'Sea', adventure: 'Adventure',
};

function fictionBooks(){
  const b = {};
  for(const s of FICTION) b[s.book] = (b[s.book]||0) + 1;
  return Object.keys(b).sort((a,c) => b[c]-b[a] || a.localeCompare(b));
}

function renderKindSeg(){
  const seg = document.getElementById('kindSeg');
  seg.innerHTML = '';
  const kinds = {};
  for(const s of FICTION) kinds[s.kind] = (kinds[s.kind]||0) + 1;
  const mk = (label, val) => {
    const b = el('button', state.kind===val?'on':'');
    b.textContent = label;
    b.onclick = () => { state.kind = val; state.book='all'; renderFiction(); };
    seg.appendChild(b);
  };
  mk('All','all');
  const order = ['gothic','victorian','russian','romance','regency',
                 'industrial','sensation','sea','adventure'];
  for(const k of order){
    if(!kinds[k]) continue;
    mk(KIND_LABEL[k]||k, k);
  }
}

function renderBookSeg(){
  const seg = document.getElementById('bookSeg');
  seg.innerHTML = '';
  const mk = (label, val) => {
    const b = el('button', state.book===val?'on':'');
    b.textContent = label;
    b.onclick = () => { state.book = val; renderFiction(); };
    seg.appendChild(b);
  };
  mk('All books','all');
  const books = fictionBooks();
  for(const bk of books){
    if(state.kind !== 'all'){
      const inKind = FICTION.some(s => s.book===bk && s.kind===state.kind);
      if(!inKind) continue;
    }
    mk(bk, bk);
  }
}

function renderFoodStrip(){
  const host = document.getElementById('foodStrip');
  host.innerHTML = '';
  const foods = {};
  let pool = FICTION;
  if(state.kind !== 'all') pool = pool.filter(s => s.kind===state.kind);
  if(state.book !== 'all') pool = pool.filter(s => s.book===state.book);
  for(const s of pool) for(const f of s.foods) foods[f] = (foods[f]||0) + 1;
  const top = Object.keys(foods).sort((a,b) => foods[b]-foods[a]).slice(0, 44);
  for(const f of top){
    const chip = el('div','food-chip' + (state.food===f?' on':''));
    chip.textContent = f + ' · ' + foods[f];
    chip.onclick = () => { state.food = state.food===f ? '' : f; renderFiction(); };
    host.appendChild(chip);
  }
}

function renderFictionBlurb(){
  const box = document.getElementById('fictionBlurb');
  if(state.book !== 'all'){
    const s = FICTION.find(x => x.book===state.book);
    const au = s ? s.author : '', yr = s ? s.year : '';
    box.innerHTML = '<h2>' + esc(state.book) + '</h2>' +
      '<div class="span">' + esc(au) + ' &middot; ' + esc(String(yr)) + '</div>' +
      '<p>Every food scene found in the text. The book is the source, and ' +
      'the passages are quoted exactly as they stand.</p>';
    return;
  }
  if(state.kind !== 'all'){
    const n = FICTION.filter(s => s.kind===state.kind).length;
    const blurb = {
      gothic: 'Gothic fiction ate well and drank better. The vampire ' +
              'novel is full of the table: the last supper before the ' +
              'seduction, the tea that precedes the murder, the feast ' +
              'that is really a farewell.',
      victorian: 'The great age of the English novel, and with it the ' +
                 'great age of the English dinner. Pudding, port, and ' +
                 'the industrial kitchens that made both possible.',
      russian: 'Tolstoy and the Russian table: the borscht, the samovar, ' +
               'the long meal that is really a way of talking about the ' +
               'soul.',
      romance: 'France and the feuilleton: the suppers, the duels over ' +
               'the last slice, and the mysterious wine that turns out ' +
               'to have been poisoned.',
      regency: 'Austen and the table as a test of character. It is all ' +
               'in the servants, the tea, and who gets invited to dinner.',
      industrial: 'Gaskell and the northern industrial towns: ' +
                  'manufactured food, poverty, and the dinner that says ' +
                  'everything about who has money.',
      sensation: 'The detective novel, and the food that frames the ' +
                 'body. A poisoned dinner, a missing dish, a household ' +
                 'that eats together because it has to.',
      sea: 'Moby-Dick and the sea: salt beef, hardtack, and the ' +
           'sufficiency of ship stores.',
      adventure: 'Defoe and Stevenson: the provisions of a shipwreck, ' +
                 'the picnic on a beach, and food as the whole of ' +
                 'survival.',
    }[state.kind] || '';
    box.innerHTML = '<h2>' + esc(KIND_LABEL[state.kind]||state.kind) + '</h2>' +
      '<div class="span">' + n + ' food scenes</div><p>' + esc(blurb) + '</p>';
    return;
  }
  box.innerHTML = '<h2>Fiction &amp; Fear</h2>' +
    '<div class="span">' + FICTION.length + ' food scenes from ' +
    fictionBooks().length + ' books</div>' +
    '<p>What the great novels of the period put on the table. These are ' +
    'not recipes &mdash; they are the evidence around them: the supper ' +
    'before the vampire arrives, the borscht in the Russian novels, the ' +
    'pudding that hides a clue. Read the passages, pick out the dishes, ' +
    'then go and cook them from the recipe tab.</p>';
}

function renderFiction(){
  renderFictionBlurb();
  renderKindSeg();
  renderBookSeg();
  renderFoodStrip();
  const host = document.getElementById('fictionResults');
  host.innerHTML = '';
  const countEl = document.getElementById('fictionCount');

  let list = FICTION;
  if(state.kind !== 'all') list = list.filter(s => s.kind===state.kind);
  if(state.book !== 'all') list = list.filter(s => s.book===state.book);
  if(state.food) list = list.filter(s => s.foods.includes(state.food));

  countEl.innerHTML = list.length + ' passage' + (list.length===1?'':'s') +
    (state.food ? ' mentioning ' + esc(state.food) : '');

  if(!list.length){
    host.appendChild(el('div','empty','No passages match that filter.'));
    return;
  }

  // Over a thousand passages at once is slow on a phone. Render the
  // first batch and let the reader pull the rest in.
  const BATCH = 50;
  let shown = 0;
  const more = el('div','empty');
  more.style.cssText = 'padding:16px;cursor:pointer';
  more.textContent = 'Tap for more passages';

  const paint = () => {
    const slice = list.slice(shown, shown + BATCH);
    for(const s of slice){
      const card = el('div','lit');
      const head = el('div','lit-head');
      const t = el('h3','lit-title');
      t.innerHTML = esc(s.book) + '<span class="lit-kind ' + s.kind + '">' +
        esc(KIND_LABEL[s.kind]||s.kind) + '</span>';
      head.appendChild(t);
      const meta = el('div','lit-meta');
      meta.innerHTML = '<span>' + esc(s.author) + '</span>' +
        '<span><b>' + esc(String(s.year)) + '</b></span>' +
        (s.chapter ? '<span>' + esc(s.chapter) + '</span>' : '') +
        '<span>' + s.foods.length + ' foods</span>';
      head.appendChild(meta);
      const chips = el('div','lit-foods');
      for(const f of s.foods.slice(0,7)){
        chips.appendChild(el('span','lit-food', esc(f)));
      }
      head.appendChild(chips);
      head.onclick = () => card.classList.toggle('open');
      card.appendChild(head);

      const body = el('div','lit-body');
      body.appendChild(el('blockquote','lit-passage', esc(s.text)));
      const cite = el('span','lit-cite');
      cite.textContent = s.book + ' — ' + s.author + ', ' + s.year +
        (s.chapter ? ', ' + s.chapter : '');
      body.appendChild(cite);
      card.appendChild(body);
      host.appendChild(card);
    }
    shown += slice.length;
    if(shown < list.length){
      more.textContent = 'Tap for more passages (' + shown + ' of ' +
        list.length + ')';
      more.style.display = '';
    } else {
      more.style.display = 'none';
    }
  };
  more.onclick = paint;
  paint();
  host.appendChild(more);
}

function renderAll(){
  renderEraRail();
  renderEraSeg();
  renderCuisineSeg();
  renderEraBlurb();
  renderPantry();
  renderResults();
}

/* ---------------- init ---------------- */
function init(){
  loadPantry();
  // tabs
  const tabs = document.getElementById('tabs');
  tabs.querySelectorAll('.tab').forEach(t => {
    t.onclick = () => {
      state.tab = t.dataset.tab;
      tabs.querySelectorAll('.tab').forEach(x =>
        x.classList.toggle('on', x === t));
      const isRec = state.tab === 'recipes';
      document.getElementById('recipesTab').style.display =
        isRec ? '' : 'none';
      // the era blurb and toolbar live in the recipes column
      document.getElementById('eraBlurb').style.display =
        isRec ? '' : 'none';
      document.querySelectorAll('.toolbar')[0].style.display =
        isRec ? '' : 'none';
      document.getElementById('count').style.display =
        isRec ? '' : 'none';
      document.getElementById('results').style.display =
        isRec ? '' : 'none';
      document.getElementById('fictionTab').style.display =
        isRec ? 'none' : '';
      if(!isRec) renderFiction();
      window.scrollTo({top:0, behavior:'smooth'});
    };
  });
  document.getElementById('pantryToggle').onclick = () => {
    const p = document.getElementById('pantryPanel');
    p.classList.toggle('open');
    document.getElementById('pantryToggle').classList.toggle('on');
    if(p.classList.contains('open')) p.scrollIntoView({behavior:'smooth', block:'start'});
  };
  document.getElementById('resetBtn').onclick = () => {
    state.pantry = new Set(DEFAULT_PANTRY);
    state.era = 'all'; state.cuisine = 'all';
    state.onlyHave = false; state.sort = 'match';
    savePantry(); renderAll();
  };
  document.getElementById('pantryAll').onclick = () => {
    for(const k in PANTRY) if(PANTRY[k].staple) state.pantry.add(k);
    savePantry(); renderPantry(); renderResults();
  };
  document.getElementById('pantryNone').onclick = () => {
    state.pantry = new Set(); savePantry(); renderPantry(); renderResults();
  };
  renderAll();
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>
"""

page = (HTML
        .replace("__ERAS__", ERAS_JSON)
        .replace("__RECIPES__", RECIPES_JSON)
        .replace("__PANTRY__", PANTRY_JSON)
        .replace("__CATEGORIES__", CATEGORIES_JSON)
        .replace("__COUNT__", str(len(ALL_RECIPES)))
        .replace("__DEFAULT__", DEFAULT_JSON)
        .replace("__NEAR__", NEAR_JSON)
        .replace("__SUBS__", SUBS_JSON)
        .replace("__ALIASES__", json.dumps(ALIASES, ensure_ascii=False))
        .replace("__CUISINES__", CUISINES_JSON)
        .replace("__FICTION__", json.dumps(FICTION, ensure_ascii=False)))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)

# --------------------------------------------------------- smoke test
# Catch the class of bug where a JS constant is referenced but never
# injected: every __PLACEHOLDER__ must be gone, and every identifier the
# page uses must be defined in the emitted script.
smoke_fail = []
for token in ("__ERAS__", "__RECIPES__", "__PANTRY__", "__CATEGORIES__",
              "__DEFAULT__", "__NEAR__", "__SUBS__", "__ALIASES__",
              "__COUNT__", "__FICTION__", "__CUISINES__"):
    if token in page:
        smoke_fail.append(f"unreplaced placeholder {token}")

required_ids = ["ERAS", "RECIPES", "PANTRY", "CATEGORIES", "DEFAULT_PANTRY",
                "NEAR", "SUBS", "ALIASES", "FICTION", "CUISINE_LIST"]
js = page.split("<script>")[1].split("</script>")[0]
for ident in required_ids:
    if f"const {ident} = " not in js:
        smoke_fail.append(f"JS constant {ident} not defined in output")

# every function the page calls must be defined
for fn in ["renderAll", "renderPantry", "renderResults", "renderEraRail",
           "renderCard", "buildBody", "scoreRecipe", "fmtQty", "has",
           "savePantry", "loadPantry", "nearEquivalents", "subFor",
           "renderEraBlurb", "renderEraSeg", "renderCuisineSeg",
           "renderFiction", "renderKindSeg", "renderBookSeg",
           "renderFoodStrip", "renderFictionBlurb", "fictionBooks"]:
    if f"function {fn}(" not in js:
        smoke_fail.append(f"function {fn}() missing")

# the recipe count in the header must match the corpus
if f'<span id="recipeCount">{len(ALL_RECIPES)}</span>' not in page:
    smoke_fail.append("header recipe count does not match corpus size")

# no external RESOURCE requests: scripts, stylesheets, images and fonts
# must all be inline, so the page works offline from a file:// or a
# static host. Outbound citation <a href> links are fine.
ext_resources = re.findall(
    r'<(?:script|img|iframe|video|audio|source)\b[^>]*\ssrc\s*=\s*["\']([^"\']+)',
    page, re.I)
ext_resources += re.findall(
    r'<link\b[^>]*\shref\s*=\s*["\']([^"\']+)', page, re.I)
ext_resources += re.findall(
    r'@import\s+(?:url\()?["\']?([^"\')\s]+)', page, re.I)
ext_resources = [u for u in ext_resources
                  if u.startswith("http") or u.startswith("//")]
if ext_resources:
    smoke_fail.append("page loads external resources: " +
                      ", ".join(sorted(set(ext_resources))))

if smoke_fail:
    print("SMOKE TEST FAILED:")
    for p_ in smoke_fail:
        print("  -", p_)
    sys.exit(1)
print("Smoke test passed: no unreplaced placeholders, all JS wired.")

print(f"Wrote {OUT}  ({len(page):,} bytes)")
print(f"  recipes : {len(ALL_RECIPES)} ({len(RECIPES)} curated + {len(GENERATED)} extracted)")
print(f"  eras    : {len(ERAS)}")
print(f"  pantry  : {len(PANTRY)} items in {len(CATEGORIES)} categories")
