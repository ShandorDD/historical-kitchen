# The Historical Kitchen

Cook 2,000 years of history from what you already have in the kitchen.

A single self-contained HTML page. No build step needed to view it, no external
requests, works offline. Open `index.html` in a browser, or visit the deployed
copy.

**Live:** https://shandordd.github.io/historical-kitchen/

## What's in it

**1,392 recipes**, c. 1740 BCE to 2025, every one traced to a source that was
downloaded and read:

| Source | Recipes | Notes |
|---|---:|---|
| Tasting History (Max Miller) | 339 | The full corpus — 380 pages, scraped from the sitemap |
| Escoffier, *A guide to modern cookery* (1903) | 789 | Le Guide Culinaire, English translation |
| Gordon Ramsay, gordonramsay.com | 170 | His own recipe collection |
| Gutenberg primary cookbooks | 22 | May (1660), Moxon (1720), *American Cookery* (1796) |
| Hand-curated (Apicius, Forme of Cury, Randolph, Acton, Beeton, Child) | 29 | Verbatim quotes, period-oddity panels |

### The ten eras

Ancient · Roman · Medieval · Renaissance & Stuart · Georgian · Victorian ·
Edwardian · **Escoffier's Foundations** · Wartime · Post-War

Each era has a context panel explaining what its kitchens were actually like.
"Escoffier's Foundations" is split out from Edwardian because the foundations —
stocks, sauces, forcemeats, court-bouillons — are the grammar of the book.
You learn them once; they turn up in everything else.

## The three features

**Era filter** — a scrolling rail of era cards plus a compact chip row.
Selecting one filters the corpus and swaps the context panel.

**Pantry matching** — tick what you have. Recipes re-sort by how well you can
make them right now, with a match percentage and a "you have it / N to buy"
readout. Near-equivalents are suggested ("have milk + a knob of butter
instead"). The pantry is remembered in your browser.

**Scaling** — 4 portions is the standard; 1–12 available. Quantities
recompute live and switch units sensibly (1.9 L, 2.25 kg, 1 1/2 tbsp).

**Period oddities** — where a period ingredient is genuinely unobtainable, the
modern stand-in is named and cited. Silphium (extinct) becomes asafoetida.
Calf's head becomes veal knuckle plus gelatine. Mustum ardens becomes white
wine vinegar. *Powdour douce* becomes galangal, cinnamon, ginger and cloves.

**Honesty markers** — recipes whose ingredient list was reconstructed from
prose rather than printed by the source say so, right above the list.

## Rebuilding

```bash
# one-shot: re-scrape the sources and rebuild
python3 extract_th.py          # Tasting History  -> th_generated.json
python3 map_pantry.py          # map ingredients   -> pantry keys
python3 extract_gutenberg.py   # 1660-1874 cookbooks
python3 extract_escoffier.py   # Escoffier 1903
python3 extract_ramsay.py      # Gordon Ramsay
python3 build.py               # validate + emit index.html
```

Requires Python 3 and nothing else. The build validates the corpus (every
pantry key resolves, every quantity is numeric, every substitute has a source),
runs a smoke test (no unreplaced placeholders, all JS wired, no external
resource requests), and writes `index.html`.

## Deploying

```bash
./deploy.sh
```

Pushes to `github.com/ShandorDD/historical-kitchen` and enables GitHub Pages
from the `main` branch root.

## Layout

```
data/eras.py                era taxonomy
data/recipes.py             the hand-curated recipe corpus
data/pantry.py              pantry dictionary + near-equivalents
data/substitutes.py         period-oddity -> modern stand-in reference
extract_th.py               scrape + parse Tasting History
map_pantry.py               ingredient name -> pantry key mapping
extract_gutenberg.py        May, Moxon, American Cookery
extract_escoffier.py        Escoffier 1903
extract_ramsay.py           Gordon Ramsay
build.py                    validator + generator
deploy.sh                   push + enable Pages
```

Built by aiFrado.
