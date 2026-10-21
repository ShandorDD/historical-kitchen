"""The Historical Kitchen — recipe corpus.

Every recipe here is transcribed from a primary source that was read
directly (Project Gutenberg full texts, or tastinghistory.com). The
`source_text` field holds the original wording where available; `method`
is a condensed modern-cook version of the same source.

Ingredient schema
-----------------
  name      display name
  qty       base quantity at `servings` portions
  unit      g | kg | ml | l | ea | tbsp | tsp | cup | quart | pint | gallon
            | gill | handful | pinch | dozen
  note      short note, max ~14 words
  pantry    key used for pantry matching (see PANTRY_KEYS)
  optional  true = omit-able without tanking the match score
  historic  true = the period oddity (drives the modern-substitute panel)
  sub       modern stand-in for that oddity
  sub_note  how the substitute behaves, and what changes

`funky` is the list of historic ingredients for the recipe, each with a
longer substitution explanation. `substitutes` is the shared reference
table of period-oddity -> modern stand-in, with sources.
"""

# ------------------------------------------------------------------ units
# Historical volume units converted to millilitres. One sextarius (Roman)
# = 0.55 L per LacusCurtius; one US gill = 118 ml.
UNIT_ML = {
    "g": None, "kg": None, "ea": None,
    "ml": 1.0, "l": 1000.0,
    "tbsp": 15.0, "tsp": 5.0, "cup": 240.0,
    "quart": 946.0, "pint": 473.0, "gallon": 3785.0, "gill": 118.0,
    "sextarius": 550.0,
    "handful": None, "pinch": None, "dozen": None,
}

# ------------------------------------------------------------------ eras
from eras import ERAS  # noqa: E402  (kept adjacent to the corpus)

# --------------------------------------------------------- substitute ref
# Each entry: period ingredient -> modern stand-in, with a source or a
# plain-language reason.
SUBSTITUTES = {
    "silphium": {
        "name": "Silphium / laser",
        "sub": "Asafoetida (hing) — a pinch, or garlic",
        "note": "The Roman herb of Cyrene, over-harvested to extinction by "
                "the 1st century CE. Its " + "sulphurous" + " resin note is "
                "reproduced by asafoetida; use a pinch, it is powerful. "
                "Garlic is a blunter stand-in.",
        "source": "Pliny, NH XI; BBC Future, 'The mystery of the lost Roman herb' (2017)",
    },
    "powder_douce": {
        "name": "Powdour douce (sweet aromatic powder)",
        "sub": "Galangal + cinnamon + ginger + cloves, ground together",
        "note": "Pegge's preface identifies it as powdered galangal, or a "
                "household compound of ground aromatic spices. A modern "
                "spice bag of galangal, cinnamon, ginger, cloves and nutmeg "
                "reproduces it closely.",
        "source": "Samuel Pegge, preface to The Forme of Cury (ed. 1780)",
    },
    "powdour_fort": {
        "name": "Powdour fort (strong powder)",
        "sub": "Black pepper, ginger and cinnamon",
        "note": "Pegge reads it as a mixture of the warmer spices — pepper, "
                "ginger, cinnamon — pulverised. The heat of the medieval "
                "sauce came from this, not from chiles.",
        "source": "Samuel Pegge, preface to The Forme of Cury (ed. 1780)",
    },
    "grapes_must": {
        "name": "Grape must (unfermented wine)",
        "sub": "Dry white wine or cider vinegar, plus a little sugar",
        "note": "Mustum ardens, 'burning must', was the medieval base of "
                "mustard. Ordinary white wine vinegar is the modern "
                "equivalent; it is more aggressively sour than must.",
        "source": "Tasting History, 'Medieval Mustard' (Mustum ardens)",
    },
    "grains_paradise": {
        "name": "Grains of paradise",
        "sub": "White pepper, or a pinch of allspice",
        "note": "Aframomum melegueta — peppery, gingery, faintly citrus. "
                "White pepper is the closest stand-in; allspice is warmer "
                "and sweeter. It was itself the standard substitute for "
                "black pepper in medieval Europe.",
        "source": "Spiceography, 'Long Pepper Substitute'; University of "
                  "Reading, Tropical Biodiversity (2014)",
    },
    "long_pepper": {
        "name": "Long pepper",
        "sub": "Black pepper, or white pepper for a cleaner heat",
        "note": "Piper longum, the rounder, fruitier relative of black "
                "pepper. Black pepper is the standard substitute; a "
                "teaspoon of black pepper stands in for a pinch of long "
                "pepper without fuss.",
        "source": "Spiceography, 'Long Pepper Substitute'",
    },
    "calf_head": {
        "name": "Calf's head (with skin, tongue, brains)",
        "sub": "Veal knuckle, or 500 g of beef shin + 1 tbsp gelatine",
        "note": "Mock turtle was invented because green turtle soup was "
                "prohibitively expensive — not to mock anything. The head "
                "supplied skin, tongue, brains and, above all, gelatin. "
                "Veal knuckle gives the same unctuous body; powdered "
                "gelatine recreates the set if the meat is lean.",
        "source": "Acton, Modern Cookery (1845); Atlas Obscura, 'How America "
                  "Fell Into — and Out of — Love With Mock Turtle Soup'",
    },
    "catsup_mushroom": {
        "name": "Mushroom catsup",
        "sub": "Soy sauce + a pinch of mushroom powder, or Worcestershire",
        "note": "18th-century American ketchups were fermented, spiced and "
                "often mushroom-based, and were kept for a year. Soy and a "
                "little mushroom powder stand in; Worcestershire is the "
                "descendant and works well.",
        "source": "Mary Randolph, The Virginia House-Wife (1824)",
    },
    "catsup_walnut": {
        "name": "Walnut catsup",
        "sub": "Balsamic vinegar + a teaspoon of walnut extract",
        "note": "Another long-keeping American ketchup. The balsamic "
                "supplies the dark fruit vinegar note.",
        "source": "Mary Randolph, The Virginia House-Wife (1824)",
    },
    "gravy_meat_drip": {
        "name": "Meat drippings / gravy",
        "sub": "The same quantity of unsalted stock",
        "note": "Randolph's dishes lean on home-made gravy, which in a "
                "modern kitchen means reducing the roasting juices or "
                "adding a good stock.",
        "source": "Mary Randolph, The Virginia House-Wife (1824)",
    },
    "powdered_malt": {
        "name": "Powdered malt",
        "sub": "Instant malted milk powder, or extra flour plus milk",
        "note": "Victorian bakers used malt to give bread body and a "
                "slightly sweet edge. Modern malted milk powder is the "
                "closest single-jar answer.",
        "source": "Mrs Beeton, Book of Household Management (1861)",
    },
    "caraway": {
        "name": "Caraway seed",
        "sub": "None needed — still sold in bulk and in the spice aisle",
        "note": "Caraway survives intact in every modern supermarket. It "
                "sits in the same family as cumin, and the two are "
                "interchangeable in a pinch.",
        "source": "Tasting History, 'Medieval Mustard'",
    },
    "rose_petals": {
        "name": "Edible rose petals",
        "sub": "1 teaspoon rose water, or a pinch of rose extract",
        "note": "Damask rose petals were used to scent both the filling and "
                "the sugar-dusted top. Rose water is the standard modern "
                "route; buy it in the baking aisle.",
        "source": "Tasting History, 'Medieval Cherry Cheesecake'",
    },
    "dehydrated_apple": {
        "name": "Dehydrated apple nuggets",
        "sub": "Any dried apple, or 2 fresh apples, finely diced",
        "note": "The US Army's 1946 B-ration field used dehydrated fruit "
                "because it weighed nothing and kept for years. Ordinary "
                "dried apple rehydrates the same way; fresh apple needs "
                "longer simmering.",
        "source": "Tasting History, 'B Ration Apple Cranberry Sauce'",
    },
    "hard_biscuit": {
        "name": "Hard military biscuits (hardtack)",
        "sub": "Any unsalted digestive biscuit, or stale bread",
        "note": "The army biscuit was a hard, low-fat, long-keeping "
                "baked good made to survive marching. Digestives or "
                "stale sourdough work; sweet biscuits will make the scone "
                "sweet.",
        "source": "Tasting History, 'WWII British Military Ration Scones'",
    },
    "evaporated_milk": {
        "name": "Evaporated milk",
        "sub": "Whole milk with a spoon of milk powder, or condensed milk",
        "note": "Already a modern pantry standard — it simply had a shelf "
                "life that fresh milk did not. Half-and-half is the "
                "closest in richness.",
        "source": "Tasting History, 'WWII British Military Ration Scones'",
    },
    "sea_hare": {
        "name": "Sea hare",
        "sub": "Any firm white fish — conger, cod, or sea bass",
        "note": "Apicius lists the sea hare among the seafood used for "
                "minced dishes. Firm white fish stands in; the point of "
                "the recipe is the texture of the forcemeat.",
        "source": "Apicius, De Re Coquinaria (c. 400 CE)",
    },
    "caul": {
        "name": "Caul (pig's caul membrane)",
        "sub": "A sheet of parchment paper, or a well-buttered baking dish",
        "note": "Roman pastry cases were lined with caul membrane to keep "
                "the base crisp. Parchment does the same job; oiling the "
                "dish works too.",
        "source": "Apicius, 'Pisa Farsilis' (c. 400 CE)",
    },
    "sow_belly": {
        "name": "Sow's belly",
        "sub": "Pork belly or bacon",
        "note": "Still completely available, and still the right fatty "
                "base for a braise. Lean pork shoulder is the modern "
                "lighter option.",
        "source": "Apicius, 'De PisIs' and 'Pisa Farsilis'",
    },
    "thrush": {
        "name": "Thrushes / small songbirds",
        "sub": "Quail, or chicken thighs",
        "note": "Small game birds were the norm in Roman cooking. Quail "
                "is the closest in size; chicken thigh stands in for "
                "bulk, and shredded chicken makes a good forcemeat.",
        "source": "Apicius, 'Pisa Farsilis'",
    },
    "brain": {
        "name": "Calf's brains",
        "sub": "Skip it, or use 100 g of pork liver for the depth",
        "note": "Brains were the connoisseur's prize — Randolph calls the "
                "eyes 'a great delicacy' and Acton fries the brain into "
                "cakes. Liver gives a comparable savoury depth; many "
                "modern cooks simply leave it out.",
        "source": "Randolph (1824); Acton, Modern Cookery (1845)",
    },
    "vinegar_white": {
        "name": "White wine vinegar",
        "sub": "Rice vinegar, or cider vinegar",
        "note": "Available everywhere; the sharpness is what matters.",
        "source": "Tasting History",
    },
    "beaten_egg_yolk": {
        "name": "Beaten egg yolk",
        "sub": "Whole egg, or a yolk with a little water",
        "note": "The yelk is Middle English for yolk. Where a historical "
                "recipe calls for yolks alone, a whole egg plus a "
                "tablespoon of water is a close stand-in.",
        "source": "The Forme of Cury (c. 1390), editorial gloss",
    },
    "indian_meal": {
        "name": "Indian meal (corn meal)",
        "sub": "Stone-ground cornmeal, or polenta flour",
        "note": "'Indian meal' meant corn meal — the name came from the "
                "term for Native American growing regions, not from a "
                "spice. The 1832 warning about lumps is why you stir it "
                "into cold milk first.",
        "source": "Child, The American Frugal Housewife (1832)",
    },
    "west_india_molasses": {
        "name": "West India molasses",
        "sub": "Dark brown sugar, or treacle",
        "note": "The rum-trade byproduct of Barbados. Dark brown sugar "
                "with a spoonful of water is the modern equivalent, and "
                "treacle is closer still.",
        "source": "Child, The American Frugal Housewife (1832)",
    },
    "sour_rye": {
        "name": "Dark rye bread (kvass)",
        "sub": "Any dark rye or sourdough, toasted",
        "note": "Kvass was the everyday drink of Muscovite Russia — a "
                "fermented bread beverage, dark and faintly sour. Dark "
                "rye is still the right bread; pumpernickel works too.",
        "source": "Tasting History, 'Kvass'",
    },
    "ghee": {
        "name": "Ghee (clarified butter)",
        "sub": "Butter, or a 50/50 butter and neutral oil blend",
        "note": "Ghee is clarified butter and is now a supermarket "
                "standard. It matters in baklava and in scones because "
                "it has no water to fight the flour, and it smokes less.",
        "source": "Tasting History, 'Baklava'",
    },
    "phyllo": {
        "name": "Phyllo / yufka sheets",
        "sub": "Spring-roll wrappers, or bought phyllo",
        "note": "Still sold frozen in every supermarket. Spring-roll "
                "wrappers are the closest emergency stand-in, though they "
                "want more ghee to stay crisp.",
        "source": "Tasting History, 'Baklava'",
    },
    "bred_cheese": {
        "name": "Aged cheese (parmesan-style)",
        "sub": "Parmigiano-Reggiano, or Grana Padano",
        "note": "The 15th-century Italian cheese that stood in for "
                "parmesan is simply a hard aged cow's-milk cheese. Any "
                "good hard cheese grated fine will do.",
        "source": "Tasting History, 'Medieval Cherry Cheesecake'",
    },
    "mushroom_powder": {
        "name": "Mushroom powder",
        "sub": "Dried porcini, rehydrated and blitzed",
        "note": "The concentrated savoury note of a century of "
                "mushroom catsup. A teaspoon of porcini powder does the "
                "same work.",
        "source": "Mary Randolph, The Virginia House-Wife (1824)",
    },
    "cameline": {
        "name": "Cameline sauce",
        "sub": "Any wine-and-breadcrumb sauce with ginger, cinnamon, cloves",
        "note": "A medieval bread-and-wine sauce, thickened and spiced. It "
                "is a device for putting the expensive spices into a "
                "sauce that clings to meat.",
        "source": "Tasting History, 'William the Conqueror's Hen'",
    },
    "brewers_yeast": {
        "name": "Brewer's yeast",
        "sub": "Active dry yeast, or a spoonful of fizzy ginger beer",
        "note": "The old-fashioned way to start a ferment without a "
                "laboratory. Active dry yeast works identically; a "
                "teaspoon of ginger-beer culture also works.",
        "source": "Tasting History, 'Kvass'; Beeton (1861)",
    },
    "cream_tartar": {
        "name": "Cream of tartar",
        "sub": "Lemon juice, in a pinch",
        "note": "The acid that stops the sugar from crystallising and "
                "gives the ginger beer its bite. Lemon juice does the "
                "same job in a much smaller quantity.",
        "source": "Mrs Beeton, Book of Household Management (1861)",
    },
    "lovage": {
        "name": "Lovage",
        "sub": "Celery leaves, or parsley",
        "note": "A tall member of the celery family with a deep, "
                "savoury celery flavour. It was a standard Roman and "
                "medieval green. Celery leaves give the closest match; "
                "parsley is blunter but always available.",
        "source": "Apicius, De Re Coquinaria; Tasting History",
    },
    "powder_fort": {
        "name": "Powdour fort (strong powder)",
        "sub": "Black pepper, ginger and cinnamon",
        "note": "Pegge reads it as a mixture of the warmer spices — pepper, "
                "ginger, cinnamon — pulverised. The heat of the medieval "
                "sauce came from this, not from chiles.",
        "source": "Samuel Pegge, preface to The Forme of Cury (ed. 1780)",
    },
    "powdour_fort": {
        "name": "Powdour fort (strong powder)",
        "sub": "Black pepper, ginger and cinnamon",
        "note": "Pegge reads it as a mixture of the warmer spices — pepper, "
                "ginger, cinnamon — pulverised. The heat of the medieval "
                "sauce came from this, not from chiles.",
        "source": "Samuel Pegge, preface to The Forme of Cury (ed. 1780)",
    },
    "cameline": {
        "name": "Cameline sauce",
        "sub": "Any wine-and-breadcrumb sauce with ginger, cinnamon, cloves",
        "note": "A medieval bread-and-wine sauce, thickened and spiced. It "
                "is a device for putting the expensive spices into a "
                "sauce that clings to meat.",
        "source": "Tasting History, 'William the Conqueror's Hen'",
    },
    "powdour_douce": {
        "name": "Powdour douce (sweet aromatic powder)",
        "sub": "Galangal + cinnamon + ginger + cloves, ground together",
        "note": "Pegge's preface identifies it as powdered galangal, or a "
                "household compound of ground aromatic spices. A modern "
                "spice bag of galangal, cinnamon, ginger, cloves and nutmeg "
                "reproduces it closely.",
        "source": "Samuel Pegge, preface to The Forme of Cury (ed. 1780)",
    },
    "dehydrated_apple": {
        "name": "Dehydrated apple nuggets",
        "sub": "Any dried apple, or 2 fresh apples, finely diced",
        "note": "The US Army's 1946 B-ration field used dehydrated fruit "
                "because it weighed nothing and kept for years. Ordinary "
                "dried apple rehydrates the same way; fresh apple needs "
                "longer simmering.",
        "source": "Tasting History, 'B Ration Apple Cranberry Sauce'",
    },
    "grapes_must": {
        "name": "Grape must (unfermented wine)",
        "sub": "Dry white wine or cider vinegar, plus a little sugar",
        "note": "Mustum ardens, 'burning must', was the medieval base of "
                "mustard. Ordinary white wine vinegar is the modern "
                "equivalent; it is more aggressively sour than must.",
        "source": "Tasting History, 'Medieval Mustard' (Mustum ardens)",
    },
    "gourds": {
        "name": "Bottle gourds",
        "sub": "Courgette, or butternut squash",
        "note": "Gourds grew in every medieval English garden and have "
                "largely vanished from Western shops. Courgette is the "
                "closest in texture; butternut squash works if you want "
                "the sweetness of the original.",
        "source": "The Forme of Cury (c. 1390), ed. Pegge",
    },
    "hard_biscuit": {
        "name": "Hard military biscuits (hardtack)",
        "sub": "Any unsalted digestive biscuit, or stale bread",
        "note": "The army biscuit was a hard, low-fat, long-keeping "
                "baked good made to survive marching. Digestives or "
                "stale sourdough work; sweet biscuits will make the scone "
                "sweet.",
        "source": "Tasting History, 'WWII British Military Ration Scones'",
    },
    "bully_beef": {
        "name": "Bully beef (canned corned beef)",
        "sub": "Canned corned beef, or corned beef hash",
        "note": "Corned beef in a tin was the standard field ration across "
                "the British Empire, eaten cold from the tin. It is still "
                "sold under the 'bully beef' name in some carousels.",
        "source": "Tasting History, 'WWII British Corned Beef Stew'",
    },
    "sea_hare": {
        "name": "Sea hare",
        "sub": "Any firm white fish — conger, cod, or sea bass",
        "note": "Apicius lists the sea hare among the seafood used for "
                "minced dishes. Firm white fish stands in; the point of "
                "the recipe is the texture of the forcemeat.",
        "source": "Apicius, De Re Coquinaria (c. 400 CE)",
    },
    "herbs": {
        "name": "Winter savoury and lemon thyme",
        "sub": "Extra thyme, or thyme plus a little rosemary",
        "note": "A 19th-century herb bench of pot herbs. Winter savoury is "
                "a step back from thyme, and lemon thyme is thyme crossed "
                "with lemon. If you cannot find them, more plain thyme is "
                "entirely fine.",
        "source": "Acton, Modern Cookery for Private Families (1845)",
    },
    "shallots": {
        "name": "Shallots",
        "sub": "One mild onion",
        "note": "Acton says it herself: 'or if these should not be at hand, "
                "one mild onion in lieu of them.'",
        "source": "Acton, Modern Cookery for Private Families (1845)",
    },
    "lard": {
        "name": "Dripping / lard",
        "sub": "Butter, margarine, or rendered fat from a roast",
        "note": "Rendered fat was the cooking fat of the British army and "
                "the British home kitchen. It is more neutral than butter "
                "and it is what the original dish was fried in.",
        "source": "Tasting History, 'WWII British Corned Beef Stew'",
    },
    "mushroom_powder": {
        "name": "Mushroom powder",
        "sub": "Dried porcini, rehydrated and blitzed",
        "note": "The concentrated savoury note of a century of "
                "mushroom catsup. A teaspoon of porcini powder does the "
                "same work.",
        "source": "Mary Randolph, The Virginia House-Wife (1824)",
    },
    "catsup_walnut": {
        "name": "Walnut catsup",
        "sub": "Balsamic vinegar + a teaspoon of walnut extract",
        "note": "Another long-keeping American ketchup. The balsamic "
                "supplies the dark fruit vinegar note.",
        "source": "Mary Randolph, The Virginia House-Wife (1824)",
    },
    "grains_paradise": {
        "name": "Grains of paradise",
        "sub": "White pepper, or a pinch of allspice",
        "note": "Aframomum melegueta — peppery, gingery, faintly citrus. "
                "White pepper is the closest stand-in; allspice is warmer "
                "and sweeter. It was itself the standard substitute for "
                "black pepper in medieval Europe.",
        "source": "Spiceography, 'Long Pepper Substitute'; University of "
                  "Reading, Tropical Biodiversity (2014)",
    },
    "mastic": {
        "name": "Mastic gum",
        "sub": "A pinch of grated nutmeg, or simply leave it out",
        "note": "A resin that wept from a Mediterranean tree, chewed as a "
                "perfume and used in wine throughout the ancient world. It "
                "came from Chios and was expensive. Nutmeg gives a "
                "different but complementary warmth; the drink is fine "
                "without it.",
        "source": "Apicius, De Re Coquinaria; Pliny, NH XII",
    },
    "charcoal": {
        "name": "Charcoal as a filter",
        "sub": "A coffee filter, or strain it twice through muslin",
        "note": "Apicius clarifies his wine with burnt charcoal, twice if "
                "necessary, drawing the residue together as it strains. The "
                "editor notes that charcoal is still a favourite filterer "
                "for liquors.",
        "source": "Apicius, 'Conditum Paradoxum', ed. Vehling note (3)",
    },
    "sugar_in_veg": {
        "name": "Sugar in a savoury dish",
        "sub": "Use a small pinch — it is doing real work, not adding sweetness",
        "note": "Not a mistake and not a modern affectation. Sugar in peas, "
                "and in most green vegetables, is old advice: it pulls out "
                "the sweetness that boiling blunts. Both Beeton and Acton "
                "tell you to sugar your peas to taste.",
        "source": "Acton, Modern Cookery (1845); Beeton (1861)",
    },
    "date_stones": {
        "name": "Roasted date stones",
        "sub": "The stones from a box of Medjool dates, roasted and soaked in wine",
        "note": "Apicius uses the stones, not the flesh — roasted, crushed, "
                "and soaked in wine to soften them before they go into the "
                "spiced wine. A modern cook would just leave them out; the "
                "drink does not miss them.",
        "source": "Apicius, 'Conditum Paradoxum'",
    },
    "nard": {
        "name": "Nard (spikenard) leaves",
        "sub": "Rosemary, or a little extra saffron",
        "note": "A Himalayan root, the most expensive spice in the Roman "
                "world, and named in Apicius's first recipe. A drachm of "
                "nard and a drachm of saffron together. Rosemary is the "
                "modern echo; the saffron is already in the drink.",
        "source": "Apicius, 'Conditum Paradoxum'; Pliny, NH XII",
    },
}
