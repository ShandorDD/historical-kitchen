#!/usr/bin/env python3
"""Mine the novel corpus for food and drink scenes.

The goal is a *literary* corpus: passages where a character eats, drinks,
feasts, or is offered something — with the exact wording, attributed to
the book and chapter.  These are not recipes, and we do not pretend they
are.  They are the "what was on the table" of the gothic novel, which is
a different and more atmospheric kind of evidence.

Two passes:

  1. SCENE PASS  - find paragraphs that name a food or a meal occasion,
     then keep the surrounding prose so the reader sees the scene.
  2. FOOD PASS   - a curated table of period foods (stews, broths, game,
     the Hungarian/Slavic dishes the user asked about) and find every
     mention, so we can build a "what the books ate" index.

Output: novels_food.json
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "data", "sources", "novels")

# ---------------------------------------------------------------- books
# id -> (title, author, year first published)
BOOKS = {
    345:  ("Dracula", "Bram Stoker", 1897),
    10007: ("Carmilla", "J. S. Le Fanu", 1872),
    14833: ("Varney the Vampire", "Thomas Peckett Prest", 1847),
    6087: ("The Vampyre", "John Polidori", 1819),
    696:  ("The Castle of Otranto", "Horace Walpole", 1764),
    84:   ("Frankenstein", "Mary Shelley", 1818),
    42:   ("Dr Jekyll and Mr Hyde", "Robert Louis Stevenson", 1886),
    209:  ("The Turn of the Screw", "Henry James", 1898),
    768:  ("Wuthering Heights", "Emily Brontë", 1847),
    174:  ("The Picture of Dorian Gray", "Oscar Wilde", 1890),
    932:  ("The Fall of the House of Usher", "Edgar Allan Poe", 1839),
    1952: ("The Yellow Wallpaper", "Charlotte Perkins Gilman", 1892),
    46:   ("A Christmas Carol", "Charles Dickens", 1843),
    730:  ("Oliver Twist", "Charles Dickens", 1838),
    580:  ("The Pickwick Papers", "Charles Dickens", 1836),
    1400: ("Great Expectations", "Charles Dickens", 1861),
    766:  ("David Copperfield", "Charles Dickens", 1850),
    550:  ("Silas Marner", "George Eliot", 1861),
    1260: ("Jane Eyre", "Charlotte Brontë", 1847),
    1023: ("Bleak House", "Charles Dickens", 1852),
    145:  ("Middlemarch", "George Eliot", 1871),
    599:  ("Vanity Fair", "W. M. Thackeray", 1848),
    2600: ("War and Peace", "Leo Tolstoy", 1869),
    1399: ("Anna Karenina", "Leo Tolstoy", 1878),
    158:  ("Emma", "Jane Austen", 1815),
    1342: ("Pride and Prejudice", "Jane Austen", 1813),
    4276: ("North and South", "Elizabeth Gaskell", 1855),
    394:  ("Cranford", "Elizabeth Gaskell", 1851),
    155:  ("The Moonstone", "Wilkie Collins", 1868),
    583:  ("The Woman in White", "Wilkie Collins", 1860),
    120:  ("Treasure Island", "Robert Louis Stevenson", 1883),
    521:  ("Robinson Crusoe", "Daniel Defoe", 1719),
    15:   ("Moby-Dick", "Herman Melville", 1851),
    82:   ("Ivanhoe", "Walter Scott", 1820),
    1377: ("The Talisman", "Walter Scott", 1825),
    3339: ("The Wandering Jew", "Eugène Sue", 1844),
    1184: ("The Count of Monte Cristo", "Alexandre Dumas", 1844),
    135:  ("Les Misérables", "Victor Hugo", 1862),
    54116: ("The Mysteries of Paris", "Eugène Sue", 1842),
    1583: ("The Woman in White (dup set)", "", 0),
    2814: ("The Orphan of the Rhine", "Edward Qi", 0),
    2148: ("Wuthering Heights / Gothic set", "", 0),
    3742: ("The Castle of Otranto (dup)", "", 0),
    2403: ("Dr. Nikola", "Guy Boothby", 1896),
    43:   ("The Vampyre (dup set)", "John Polidori", 1819),
    164:  ("Carmilla (dup set)", "J. S. Le Fanu", 1872),
    1727: ("The Three Musketeers", "Alexandre Dumas", 1844),
    1638: ("The Mysteries of Paris (dup)", "", 0),
}

# ------------------------------------------------- food vocabulary
# Deliberately broad: we want to catch the ordinary as well as the
# grand.  A gothic novel is full of "tea", "wine", "supper".
#
# TRAP: the alternation MUST be anchored with word boundaries.  Without
# \b, "ale" matches inside "Royale", "table" inside "suitable", "pie"
# inside "copier", "ice" inside "juice", "tart" inside "start", "inn"
# inside "beginning".  That put 2917 phantom food chips on 1337 cards
# -- "Ale" on a passage that never mentions ale.  It also left a
# trailing "|" in verbose mode, which creates an EMPTY alternative:
# the pattern matched "" at every position, so "" landed in every
# food list.  Both are fixed by anchoring and dropping the stray "|".
FOOD_WORDS = r"""
(?:bread|beer|wine|ale|porter|cider|tea|coffee|chocolate|cocoa|toast|
  butter|cheese|cream|milk|egg|honey|sugar|salt|pepper|spice|
  beef|mutton|lamb|pork|veal|ham|bacon|sausage|meat|steak|chop|roast|
  stew|broth|potage|soup|pottage|porridge|broth|
  soup|pudding|tart|pie|cake|bread|roll|biscuit|bun|loaf|toast|
  fish|trout|salmon|herring|mackerel|carp|pike|sole|cod|halibut|
  venison|hare|rabbit|game|wild|fowl|chicken|turkey|goose|duck|pheasant|
  partridge|roast|boiled|baked|fried|grilled|minced|chopped|
  vegetables|potato|onion|carrot|turnip|cabbage|celery|peas|beans|lentils|
  herbs|parsley|thyme|basil|mint|marjoram|ginger|nutmeg|mace|cinnamon|
  garlic|shallot|lemon|lime|orange|apple|pear|plum|cherry|grape|
  salad|greens|asparagus|beetroot|beet|cucumber|mushroom|truffle|
  jam|jelly|honey|syrup|molasses|treacle|porridge|oatmeal|barley|rice|
  gravy|broth|entree|dish|meal|breakfast|luncheon|dinner|supper|tea-time|
  banquet|feast|revel|table|dining-room|dining.room|kitchen|pantry|
  cellar|vault|butler|cook|housekeeper|waiter|footman|manners|
  goulash|goulach|borscht|borsch|beefsteak|pirog|pirog|blini|vareniki|
  borscht|cabbage|beet|sour[ -]cream|smetana|mustard|horseradish|
  paprika|paprika|cumin|coriander|saffron|bay[ -]leaf|clove|cumin|
  hash|mince|pudding|tarts|cakes|biscuit|custard|omelette|omelet|
  chocolate|coffee|tea|sugar|honey|ice|syrup|lemonade|beer|ale|
  port|claret|sherry|champagne|burgundy|bordeaux|burgundy|
  raki|brandy|rum|cognac|brandy|vinegar|mustard|sauce|ketchup|
  blood|wine|blood-warm|bloodwarm|heart|liver|offal|carcass|
  flesh|hide|skin|bones|bone|offal|entrails|guts|rabbit|rooks|
  rat|mouse|mole|vermin|roast|devour|feast|gorge|glut|banquet|
  haggis|gammon|chops|baron|beef|mutton|pork|veal|lamb|calf|liver|
  kidney|heart|tongue|brawn|palate|head|pig|ox|sheep|goat|bear|boar|
  venison|elk|deer|hare|grouse|ptarmigan|wild[ -]duck|teal|heron|
  carp|salmon|trout|pike|eel|perch|roach|dace|bream|pike|
  cheese|butter|milk|cream|curds|whey|rennet|churn|
  bread|barm|yeast|leaven|hops|malt|ale|brew|tavern|
  kitchen|scullery|larder|store|granary|mill|
  cook|cooking|cooks|cookery|recipe|recipes|dish|dishes|
  supper|dinner|lunch|breakfast|tea|banquet|feast|revel|
  appetite|appetite|hunger|hungry|thirst|thirsty|savour|savor|taste|
  plate|plateful|tray|napkin|tablecloth|fork|knife|spoon|glass|goblet|
  wine-cup|cup|tureen|ladle|dish|bowl|basin|
  smoke|smoking|fumes|reeking|odour|odor|stench|
  fire|fires|hearth|range|oven|boiler|pot|kettle|
  holy|stolen|blessed|christmas|easter|fast|feast-day|
  hungarian|russian|polish|slav|bohemian|magyar|serbian|romanian|
  transylvania|carpathian|steppe|poland|russia|hungary|balkans|
  paprika|red[ -]pepper|black[ -]pepper|paprika|boros|csarnok|goulash|
  borscht|blini|strogonoff|beefstroganoff|kulebyaka|solyanka|shchi|
  kasha|vareniki|potato[ -]dumplings|kolacky|rozgal|
  onion|onions|garlic|horseradish|mustard|vinegar|peasant|
  peasant|serf|husbandman|farmhouse|cottage|hut|
  tavern|inn|public[ -]house|alehouse|hostelry|
  hospitable|hospitality|refreshment|provision|provisions|store|
  larder|pantry|butler|servant|maid|scullion|cook|housekeeper|
  banquet|carve|carving|platter|tray|groove|dish|service|
  sumptuous|exquisite|delicious|palatable|savoury|nutty|sweet|
  rich|poor|plain|simple|humble|coarse|paltry|meagre|meager|
  feast|banquet|revelry|revel|merrymaking|orgy|orgies|carouse|
  carousing|debauch|glutton|gourmand|gourmet|epicure|epicurean|
  appetite|voracity|rapacity|greed|avarice)
"""

# meal-occasion cues: a paragraph that names one of these is very
# likely a food scene even if it never says "dinner".
OCCASION = re.compile(
    r"\b(?:supper|dinner|luncheon|breakfast|breakfast-room|"
    r"breakfast|tea|banquet|feast|revel|revelry|carouse|carousing|"
    r"table|dining|dining-room|board|mess|gorge|feasting|"
    r"grazing|entertain|entertainment|hospitality)\b", re.I)

# A paragraph that reads as a meal.  We want the paragraph to have
# food in it AND some sense of occasion or quantity.
FOOD_RE = re.compile(r"\b" + FOOD_WORDS + r"\b", re.I | re.X)

CHAPTER_RE = re.compile(
    r"^\s*(CHAPTER\s+[IVXLCDM0-9]+|Chapter\s+[ivxlcdm0-9]+|"
    r"[IVXL]+\.|\d+\.)\s*$", re.M)


def strip_gutenberg(text):
    """Remove the PG header/footer and the boilerplate."""
    m = re.search(r"\*\*\*\s*START OF TH[EI][\s\S]*?\*\*\*", text)
    if m:
        text = text[m.end():]
    m = re.search(r"\*\*\*\s*END OF TH[EI][\s\S]*?\*\*\*", text)
    if m:
        text = text[:m.start()]
    return text


def clean_paragraph(p):
    p = re.sub(r"\s+", " ", p).strip()
    p = p.replace("’", "'").replace("‘", "'")
    p = p.replace("“", '"').replace("”", '"')
    p = p.replace("—", "--").replace("–", "-")
    return p


def find_chapters(text):
    """Return list of (index, title) for chapter headings."""
    out = []
    for m in CHAPTER_RE.finditer(text):
        out.append((m.start(), clean_paragraph(m.group(0))))
    return out


def chapter_for(chapters, pos):
    lo, hi = 0, len(chapters) - 1
    res = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        if chapters[mid][0] <= pos:
            res = chapters[mid][1]
            lo = mid + 1
        else:
            hi = mid - 1
    return res


def paragraphs(text):
    """Yield (start_offset, paragraph_text) for prose paragraphs."""
    # split on blank lines; keep offsets
    for m in re.finditer(r"(?:\r?\n[ \t]*){2,}(.+?)(?=(?:\r?\n[ \t]*){2,}|\Z)",
                         text, re.S):
        yield m.start(1), m.group(1)


def is_header_noise(p):
    """Skip chapter titles, illustrations, tables of contents."""
    s = p.strip()
    if len(s) < 120:
        return True
    if re.match(r"^\s*(CHAPTER|Chapter|[IVXL]+\.|\d+\.)\s*$", s):
        return True
    if re.search(r"\[Illustration", s, re.I):
        return True
    if re.match(r"^\s*(P\.|\[|\{)", s):
        return True
    return False


def main():
    records = []
    per_book = {}

    for bid, (title, author, year) in BOOKS.items():
        path = os.path.join(SRC, f"pg{bid}.txt")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            raw = f.read()
        if len(raw) < 5000:
            continue
        # Only books we actually recognise as the right title
        if not title or not author:
            continue
        text = strip_gutenberg(raw)
        chapters = find_chapters(text)

        scenes = []
        for off, para in paragraphs(text):
            if is_header_noise(para):
                continue
            c = clean_paragraph(para)
            if len(c) < 120 or len(c) > 2200:
                continue
            foods = set(m.group(0).lower() for m in FOOD_RE.finditer(c))
            if len(foods) < 2:
                continue
            has_occasion = bool(OCCASION.search(c))
            if not has_occasion:
                continue
            scenes.append({
                "book_id": bid,
                "book": title,
                "author": author,
                "year": year,
                "chapter": chapter_for(chapters, off),
                "text": c,
                "foods": sorted(foods)[:12],
            })

        per_book[title] = len(scenes)
        records.extend(scenes)
        print(f"pg{bid:<6} {title[:40]:40} {len(scenes):>4} scenes", flush=True)

    out = os.path.join(BASE, "novels_food.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
    print(f"\nTotal scenes: {len(records)}")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
