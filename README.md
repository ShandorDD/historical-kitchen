# The Historical Kitchen

Cook 2,000 years of history from what you already have in the kitchen.

A single self-contained HTML page. No build step needed to view it, no external
requests, works offline. Open `index.html` in a browser, or visit the deployed
copy.

## What's in it

**29 recipes**, c. 2000 BCE to 1946, every one transcribed from a primary source
that was read in full:

- *Apicius, De Re Coquinaria* (c. 400 CE)
- *The Forme of Cury* (c. 1390, ed. Samuel Pegge 1780)
- *The Virginia House-Wife* (Mary Randolph, 1824)
- *Modern Cookery for Private Families* (Eliza Acton, 1845)
- *The Book of Household Management* (Mrs Beeton, 1861)
- *The American Frugal Housewife* (Lydia Maria Child, 1832)
- Max Miller's Tasting History

18 recipes carry a verbatim source quote, in the original Middle English or
19th-century English.

## The three features

**Era filter** — nine eras, from Ancient (3000–1000 BCE) through Roman,
Medieval, Renaissance & Colonial, Georgian, Victorian, Edwardian and Wartime
to Post-War. Each era has a context panel explaining what its kitchens were
actually like.

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

## Rebuilding

```bash
python3 build.py
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
data/eras.py          era taxonomy
data/recipes.py       the recipe corpus
data/pantry.py        pantry dictionary + near-equivalents
data/substitutes.py   period-oddity -> modern stand-in reference
build.py              validator + generator
deploy.sh             push + enable Pages
```

Built by aiFrado.
