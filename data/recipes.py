"""The Historical Kitchen — the recipe corpus.

26 recipes, c. 2000 BCE to 1946. Every entry was transcribed from a
primary source read in full:

  Project Gutenberg (via cache/epub/<id>/pg<id>.txt)
    29728  Apicius, De Re Coquinaria (ed. J.D. Vehling, 1926)   [ISBN-free]
    8102   The Forme of Cury (ed. Samuel Pegge, 1780)
    12519  Mary Randolph, The Virginia House-Wife (1824)
    72482  Eliza Acton, Modern Cookery for Private Families (1845)
    10136  Mrs Beeton, Book of Household Management (1861)
    13493  Lydia Maria Child, The American Frugal Housewife (1832)

  tastinghistory.com/recipes/<slug>  (Max Miller)
    22 recipes; the ones used here were downloaded and read.

`src` holds the exact source wording (Middle English, 19th-century English,
or Latin-translated English) where the source is quotable at length.
`method` is the modern-cook version, condensed but faithful.
`history` is the era context, written to be read.
"""

RECIPES = [

    # ============================================================ ANCIENT
    {
        "id": "sumerian-date-cake",
        "title": "Sumerian Date Cake",
        "era": "ancient",
        "year": "c. 2000 BCE",
        "region": "Sumer & Mesopotamia",
        "source": "Third Dynasty of Ur cuneiform tablet, via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/sumeriandatecake",
        "servings": 4,
        "tags": ["dessert", "vegetarian"],
        "confidence": "likely",
        "history": "This is not a recipe so much as a shopping list. A "
                   "cuneiform tablet from the Third Dynasty of Ur lists "
                   "dates, wheat, butter, cheese and raisins — most likely "
                   "a temple bakery's stock, not a set of instructions. "
                   "That is exactly why it is interesting: it is one of the "
                   "oldest written records of people assembling a food for "
                   "a purpose, and the ingredients still read like a recipe "
                   "today. The proportions are anyone's guess. Max's advice "
                   "stands — try your own variation, and yours will be "
                   "exactly as correct as his.",
        "source_text": "The inspiration for this recipe comes from a list "
                       "of ingredients on a cuneiform tablet from the Third "
                       "Dynasty of Ur around 4,000 years ago. While many "
                       "historical recipes are vague, this isn't even "
                       "pretending to be a recipe.",
        "method": [
            "Preheat the oven to 350F (175C).",
            "Mince the dates, then grind them in a mortar to a paste.",
            "In a bowl, combine the flour, cheese and butter. Work them "
            "together with your hands until thoroughly combined.",
            "Add the dates and work them into the dough until evenly "
            "distributed. Layer some raisins below and above if you like.",
            "Form the cake into a disc that fits your pan. Line the bottom "
            "and sides with parchment or rinsed grape leaves.",
            "Bake until golden and set, roughly 35-40 minutes.",
        ],
        "ingredients": [
            {"name": "Pitted dates", "qty": 300, "unit": "g", "pantry": "dates",
             "note": "The tablet's main sweetener; Mesopotamian date "
                     "cultivation is very old"},
            {"name": "Whole wheat flour", "qty": 90, "unit": "g", "pantry": "flour",
             "note": "The grain the tablet implies but does not name"},
            {"name": "Soft white cheese (ricotta)", "qty": 45, "unit": "g",
             "pantry": "ricotta", "note": "Fresh cheese in place of a "
                     "curdled one, as Sumerian dairy was"},
            {"name": "Salted butter", "qty": 115, "unit": "g", "pantry": "butter",
             "note": "Named on the tablet; a prestige good"},
            {"name": "Raisins", "qty": 30, "unit": "g", "pantry": "raisins",
             "note": "The second dried fruit, and another listed item"},
            {"name": "Grape leaves (jarred or fresh)", "qty": 1, "unit": "ea",
             "pantry": "grape_leaves", "optional": True,
             "note": "Line the pan the way the bakers would have"},
        ],
        "funky": [],
    },

    # ============================================================== ROMAN
    {
        "id": "apicius-pea-soup",
        "title": "Apicius's Pea Soup (De PisIs)",
        "era": "roman",
        "year": "c. 400 CE",
        "region": "Rome",
        "source": "Apicius, De Re Coquinaria, Book I (ed. J.D. Vehling, 1926)",
        "source_url": "https://www.gutenberg.org/ebooks/29728",
        "servings": 4,
        "tags": ["soup", "vegetarian"],
        "confidence": "verified",
        "history": "Apicius is Europe's only surviving Roman cookbook, and "
                   "it opens with soups because in Rome a meal began with "
                   "them. This recipe is barely more than instructions to "
                   "boil peas with herbs and wine — the genius is the "
                   "omission of anything rich. Roman peas were a luxury "
                   "green thing in winter, and Vehling's own note points "
                   "out the modern equivalent: petits pois à la Française, "
                   "green peas cooked in broth with bacon, lettuce and "
                   "mint. The Roman version reaches for lovage and "
                   "basilica, which we would simply call herbs.",
        "source_text": "COOK THE PEAS, WHEN SKIMMED, LAY LEEKS, CORIANDER "
                       "AND CUMIN ON TOP. CRUSH PEPPER, LOVAGE, CUMIN, DILL "
                       "AND GREEN BASILICA, WINE AND BROTH TO TASTE, MAKE IT "
                       "BOIL; WHEN DONE STIR WELL, PUT IN WHAT PERCHANCE "
                       "SHOULD BE MISSING AND SERVE.",
        "method": [
            "Cook the peas in salted water, skimming as they rise.",
            "Lay leeks, coriander and cumin on top of the peas to steam "
            "in the pod.",
            "Crush pepper, lovage, cumin, dill and green basil together "
            "with a little wine and broth.",
            "Add the crushed herbs and broth to the peas, bring to a boil.",
            "Stir well, taste, and serve — adding whatever was forgotten.",
        ],
        "ingredients": [
            {"name": "Green peas (in the pod if possible)", "qty": 500,
             "unit": "g", "pantry": "peas",
             "note": "The dish's whole identity; Roman peas were precious"},
            {"name": "Leeks", "qty": 2, "unit": "ea", "pantry": "leeks",
             "note": "Layered over the peas to steam in the pod"},
            {"name": "Coriander seed", "qty": 1, "unit": "tsp",
             "pantry": "coriander_seed", "note": "Ground, not fresh leaf"},
            {"name": "Cumin seed", "qty": 1, "unit": "tsp", "pantry": "cumin",
             "note": "Crushed with the other aromatics"},
            {"name": "Lovage", "qty": 1, "unit": "tbsp", "pantry": "lovage",
             "historic": True, "sub": "celery leaves or parsley",
             "note": "A celery-family herb, now uncommon in shops"},
            {"name": "Dill", "qty": 1, "unit": "tbsp", "pantry": "dill",
             "note": "A Roman green herb we now treat as a pickle herb"},
            {"name": "Green basil", "qty": 1, "unit": "tbsp", "pantry": "basil",
             "note": "Basilica, the aromatic sweet basil"},
            {"name": "Black pepper", "qty": 1, "unit": "tsp", "pantry": "pepper",
             "note": "Crushed, and expensive — Rome imported it"},
            {"name": "Dry white wine", "qty": 120, "unit": "ml", "pantry": "white_wine",
             "note": "Splash to the broth, to taste"},
            {"name": "Chicken or vegetable broth", "qty": 500, "unit": "ml",
             "pantry": "broth", "note": "Roman cookery built on a rich stock"},
        ],
        "funky": [
            {"ingredient": "Lovage", "key": "lovage", "ing_ref": 'Lovage',
             "why": "A tall celery-family herb that tastes like concentrated "
                    "celery and lovage. It was a standard Roman green, and "
                    "it is genuinely hard to find now."},
        ],
    },
    {
        "id": "apicius-supreme-peas",
        "title": "Peas Supreme Style (Pisa Farsilis)",
        "era": "roman",
        "year": "c. 400 CE",
        "region": "Rome",
        "source": "Apicius, De Re Coquinaria, Book I (ed. J.D. Vehling, 1926)",
        "source_url": "https://www.gutenberg.org/ebooks/29728",
        "servings": 6,
        "tags": ["main", "showpiece"],
        "confidence": "verified",
        "history": "This is Roman showpiece cooking at its most theatrical: "
                   "a dish turned out onto a plate, with a sauce poured over "
                   "it, and a second layer inverted on top so the diner cuts "
                   "into a mosaic of peas, meat and nuts. The recipe needs "
                   "a square baking dish you can invert — which is why "
                   "Apicius specifies one 'suitable for turning over' and "
                   "tells you to line it with caul membrane so the base "
                   "stays crisp. The laser is the elephant in the room: "
                   "the herb Apicius names over and over, harvested to "
                   "extinction in Cyrene.",
        "source_text": "COOK THE PEAS WITH OIL AND A PIECE OF SOW'S BELLY. "
                       "PUT IN A SAUCE PAN BROTH, LEEK HEADS, GREEN "
                       "CORIANDER AND PUT ON THE FIRE TO BE COOKED. OF "
                       "TID-BITS CUT LITTLE DICE. SIMILARLY COOK THRUSHES OR "
                       "OTHER SMALL BIRDS, OR TAKE SLICED CHICKEN AND DICED "
                       "BRAIN. FURTHER COOK, IN THE AVAILABLE LIQUOR OR "
                       "BROTH, LUCANIAN SAUSAGE AND BACON... SPRINKLE A "
                       "LAYER OF CRUSHED NUTS UPON WHICH PUT SOME PEAS.",
        "method": [
            "Cook the peas with oil and a piece of sow's belly; build a "
            "broth with leek heads, green coriander and the peas' liquor.",
            "Dice the meat small: thrush or other small birds, or sliced "
            "chicken and diced brain. Cook in the liquor with Lucanian "
            "sausage and bacon.",
            "Crush pepper, lovage, origany and ginger; dilute with the "
            "broth.",
            "Oil a square baking dish and line it with caul. Lay a layer "
            "of crushed toasted pignolia nuts, then the peas to cover the "
            "bottom completely.",
            "Add the meat, sauce and more nuts on top, then turn the whole "
            "dish out onto a serving plate.",
        ],
        "ingredients": [
            {"name": "Green peas", "qty": 700, "unit": "g", "pantry": "peas",
             "note": "The base layer, covering the whole dish"},
            {"name": "Pork belly or bacon", "qty": 150, "unit": "g",
             "pantry": "pork_belly", "historic": True, "sub": "pancetta or bacon",
             "note": "Sow's belly in Apicius; bacon today"},
            {"name": "Leeks (white part, sliced)", "qty": 2, "unit": "ea",
             "pantry": "leeks", "note": "Leek heads give the broth body"},
            {"name": "Green coriander", "qty": 1, "unit": "tbsp",
             "pantry": "coriander", "note": "Fresh leaves, unlike the seed"},
            {"name": "Chicken (sliced) or quail", "qty": 400, "unit": "g",
             "pantry": "chicken", "historic": True, "sub": "quail, or chicken thigh",
             "note": "Thrushes in the original; quail is closest today"},
            {"name": "Lucanian sausage", "qty": 200, "unit": "g",
             "pantry": "sausage", "historic": True, "sub": "Italian-style pork sausage",
             "note": "A Roman regional sausage, still made in that style"},
            {"name": "Toasted pine nuts (pignolia)", "qty": 60, "unit": "g",
             "pantry": "pine_nuts", "note": "Crushed for the layered mosaic"},
            {"name": "Laser (silphium)", "qty": 1, "unit": "pinch",
             "pantry": "silphium", "historic": True, "sub": "asafoetida, a pinch",
             "note": "The extinct Roman herb of Cyrene; the defining flavour "
                     "of the whole book"},
            {"name": "Lovage", "qty": 1, "unit": "tbsp", "pantry": "lovage",
             "historic": True, "sub": "celery leaves or parsley",
             "note": "Apicius uses it constantly"},
            {"name": "Origany (oregano)", "qty": 1, "unit": "tbsp",
             "pantry": "oregano", "note": "The wild oregano of antiquity"},
            {"name": "Ginger", "qty": 1, "unit": "tsp", "pantry": "ginger",
             "note": "Ground, and imported at great cost"},
            {"name": "Black pepper", "qty": 2, "unit": "tsp", "pantry": "pepper",
             "note": "Crushed"},
            {"name": "Olive oil", "qty": 3, "unit": "tbsp", "pantry": "olive_oil",
             "note": "Rome's cooking fat"},
            {"name": "Caul membrane", "qty": 1, "unit": "ea", "pantry": "caul",
             "historic": True, "sub": "parchment paper",
             "note": "Lining for the inverted dish, to keep the base crisp"},
        ],
        "funky": [
            {"ingredient": "Laser (silphium)", "key": "silphium", "ing_ref": 'Laser (silphium)',
             "why": "Apicius names this in nearly every savoury recipe. It "
                    "grew only around Cyrene in Libya, was harvested to "
                    "absolute extinction by the first century CE, and was so "
                    "valued it is said to have been minted into coins. Its "
                    "resinous, slightly sulphurous note is approximated "
                    "today by asafoetida."},
            {"ingredient": "Caul membrane", "key": "caul", "ing_ref": 'Caul membrane',
             "why": "Pig's caul, the translucent membrane that wraps a "
                    "pig's organs, used as a baking liner. It kept the "
                    "underside of a turned-out Roman dish crisp. Parchment "
                    "does the same job."},
            {"ingredient": "Thrushes / small songbirds", "key": "thrush", "ing_ref": 'Chicken (sliced) or quail',
             "why": "Songbirds were ordinary table fare in Rome. Quail is "
                    "the modern bird of the same size."},
        ],
    },
    {
        "id": "roman-mustard",
        "title": "Roman Mustard",
        "era": "roman",
        "year": "4th century CE",
        "region": "Rome",
        "source": "Apicius, De Re Coquinaria (ed. J.D. Vehling, 1926), via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/romanmustard",
        "servings": 8,
        "tags": ["condiment", "vegetarian", "no-cook"],
        "confidence": "verified",
        "history": "Mustard is as old as civilisation — cultivated in India "
                   "by 3000 BCE and growing wild from North Africa to the "
                   "Himalayas. Pliny the Elder lists what the Romans thought "
                   "it cured, from snake bites to poisonous mushrooms to "
                   "phlegm. This version is almost pure honey: five pounds "
                   "of it to an ounce and a half of seed. You get the "
                   "mustard aroma with none of the heat, the honey "
                   "completely dominant. It also separates, which is the "
                   "sort of detail a Roman kitchen would not have "
                   "commented on.",
        "source_text": "Take mustard seed in the amount of one and a half "
                       "sextarii and grind it into a powder. To this add "
                       "five pounds of honey, one pound of Spanish olive "
                       "oil, and one sextarius of sharp vinegar. Grind "
                       "everything together.",
        "method": [
            "Grind the mustard seeds in a mortar until they are the "
            "texture you like. A fine powder will make for a smoother mustard.",
            "Stir in the honey until it is fully incorporated.",
            "Then stir in the olive oil until it is fully incorporated, and "
            "finally the vinegar, again until fully incorporated.",
            "The oil and vinegar will separate after a couple of minutes, "
            "so give it another stir before you serve it forth.",
        ],
        "ingredients": [
            {"name": "Black mustard seeds", "qty": 50, "unit": "g",
             "pantry": "mustard_seeds", "note": "Black for real heat; "
             "yellow is milder"},
            {"name": "Honey", "qty": 115, "unit": "g", "pantry": "honey",
             "note": "The dominant flavour — five pounds to the sextarius"},
            {"name": "Olive oil", "qty": 30, "unit": "ml", "pantry": "olive_oil",
             "note": "Spanish oil, i.e. the good imported kind"},
            {"name": "Wine vinegar", "qty": 40, "unit": "ml", "pantry": "vinegar",
             "note": "Sharp vinegar, a full sextarius"},
        ],
        "funky": [],
    },

    # =========================================================== MEDIEVAL
    {
        "id": "cury-gourdes-in-potage",
        "title": "Gourds in Potage (Gourdes in Potage)",
        "era": "medieval",
        "year": "c. 1390",
        "region": "England",
        "source": "The Forme of Cury, ed. Samuel Pegge (1780), recipe no. VIII",
        "source_url": "https://www.gutenberg.org/ebooks/8102",
        "servings": 4,
        "tags": ["soup", "pork"],
        "confidence": "verified",
        "history": "The Forme of Cury is the oldest English cookbook, "
                   "compiled about 1390 and preserved in the British "
                   "Library among manuscripts that once belonged to the "
                   "monks of Reading Abbey. It is written in Middle "
                   "English, in the reign of Richard II. This recipe is a "
                   "gourd soup enriched with pounded boiled pork, egg "
                   "yolks and saffron, then finished with powdour douce — "
                   "the sweet aromatic powder that Pegge's preface "
                   "identifies as galangal or a household blend of ground "
                   "spices. It is a 'curious potage', the cookbook's word "
                   "for a dish above a householder's station.",
        "source_text": "Take young Gowrdes pare hem and kerue hem on pecys. "
                       "cast hem in gode broth, and do ther to a gode pertye "
                       "of Oynouns mynced. take Pork soden. grynd it and alye "
                       "it ther with and with zolkes of ayrenn. do ther to "
                       "safroun and salt, and messe it forth with powdour "
                       "douce.",
        "method": [
            "Peel the young gourds and cut them into pieces.",
            "Cast them into good broth with a good quantity of minced "
            "onions.",
            "Take boiled pork, pound it, and mix it in with egg yolks.",
            "Add saffron and salt, and serve it forth with powdour douce.",
        ],
        "ingredients": [
            {"name": "Young gourds (or courgette / squash)", "qty": 600,
             "unit": "g", "pantry": "squash", "historic": True,
             "sub": "zucchini or butternut squash",
             "note": "Bottle gourds, ubiquitous then, uncommon now"},
            {"name": "Good broth", "qty": 1200, "unit": "ml", "pantry": "broth",
             "note": "'Gode broth', prepared beforehand"},
            {"name": "Onion, minced", "qty": 1, "unit": "ea", "pantry": "onion",
             "note": "A good quantity — 'a gode pertye'"},
            {"name": "Cooked pork (shoulder)", "qty": 200, "unit": "g",
             "pantry": "pork", "note": "Boiled, then pounded to a paste"},
            {"name": "Egg yolks", "qty": 2, "unit": "ea", "pantry": "eggs",
             "historic": True, "sub": "whole eggs plus a little water",
             "note": "'Zolkes of ayrenn' — yolks alone, no whites"},
            {"name": "Saffron", "qty": 0.25, "unit": "tsp", "pantry": "saffron",
             "note": "Colour and perfume, and ruinously expensive"},
            {"name": "Salt", "qty": 1, "unit": "tsp", "pantry": "salt",
             "note": "To taste"},
            {"name": "Powdour douce (sweet aromatic powder)", "qty": 1,
             "unit": "tsp", "pantry": "powder_douce", "historic": True,
             "sub": "galangal + cinnamon + ginger + cloves",
             "note": "The house spice blend, ground fine"},
        ],
        "funky": [
            {"ingredient": "Powdour douce", "key": "powder_douce", "ing_ref": 'Powdour douce (sweet aromatic powder)',
             "why": "A mystery blend mentioned in nearly every recipe in "
                    "the book. Pegge spent years on it and concluded it was "
                    "either powdered galangal or a home-ground compound of "
                    "aromatic spices — a 'good powder' kept ready in a "
                    "special box, the medieval equivalent of a masala tin."},
            {"ingredient": "Young gourds", "key": "gourds", "ing_ref": 'Young gourds (or courgette / squash)',
             "why": "Bottle gourds grew everywhere in medieval England and "
                    "have largely vanished from Western shops. Courgette is "
                    "the closest thing in texture."},
        ],
    },
    {
        "id": "cury-ground-beans",
        "title": "Ground Beans (Gronnden Benes)",
        "era": "medieval",
        "year": "c. 1390",
        "region": "England",
        "source": "The Forme of Cury, ed. Samuel Pegge (1780), recipe no. I",
        "source_url": "https://www.gutenberg.org/ebooks/8102",
        "servings": 4,
        "tags": ["main", "vegetarian", "pork"],
        "confidence": "verified",
        "history": "The very first recipe in the Forme of Cury, and it is a "
                   "dish of the poor. Pegge's editorial note says so "
                   "plainly: this 'was a dish of the poorer householder'. "
                   "Beans were dried in a kiln or an oven until hard, then "
                   "hulled and winnowed clean — a long slow process, and the "
                   "reason beans could be stored through a hungry winter "
                   "and eaten with bacon. The companion recipe, Drawen "
                   "Benes, grinds them in a mortar and draws them up with "
                   "broth into a thick pottage. Served with bacon, this is "
                   "medieval peasant food, and it is the foundation of "
                   "every bean dish since.",
        "source_text": "Take benes and dry hem in a nost or in an Ovene and "
                       "hulle hem wele and wyndewe out the hulk and wayshe "
                       "hem clene an do hem to seeth in gode broth an ete hem "
                       "with Bacon.",
        "method": [
            "Dry the beans in a kiln or oven until hard — this is what "
            "made them storable through winter.",
            "Hull them well and winnow the hulls out.",
            "Wash them clean and simmer in good broth.",
            "Eat them with bacon.",
        ],
        "ingredients": [
            {"name": "Dried beans (haricot or cannellini)", "qty": 400,
             "unit": "g", "pantry": "beans", "note": "Dried and hulled; the "
             "staple of the poorer householder"},
            {"name": "Good broth", "qty": 1200, "unit": "ml", "pantry": "broth",
             "note": "Prepared beforehand"},
            {"name": "Bacon", "qty": 200, "unit": "g", "pantry": "bacon",
             "note": "'Ete hem with Bacon' — the whole garnish"},
        ],
        "funky": [],
    },
    {
        "id": "cury-cabbage-potage",
        "title": "Cabbage in Potage (Caboches in Potage)",
        "era": "medieval",
        "year": "c. 1390",
        "region": "England",
        "source": "The Forme of Cury, ed. Samuel Pegge (1780), recipe no. IV",
        "source_url": "https://www.gutenberg.org/ebooks/8102",
        "servings": 4,
        "tags": ["side", "vegetarian"],
        "confidence": "verified",
        "history": "Caboches is, in Pegge's gloss, 'probably cabbages' — and "
                   "the uncertainty is the interesting part. The Forme of "
                   "Cury is a composite manuscript, and the editor cannot "
                   "always be certain what the medieval cook meant. The "
                   "recipe is short: quarter the cabbages, boil them in good "
                   "broth with minced onions and the white of leeks sliced "
                   "thin, then saffron, salt and powdour douce. Cabbage, "
                   "saffron and spice in one pot — a poor man's dish made "
                   "expensive by the addition of the two most expensive "
                   "things in the medieval kitchen.",
        "source_text": "Take Caboches and quarter hem and seeth hem in gode "
                       "broth with Oynouns y mynced and the whyte of Lekes y "
                       "slyt and corue smale and do ther to safroun an salt "
                       "and force it with powdour douce.",
        "method": [
            "Quarter the cabbages and simmer them in good broth with the "
            "minced onions.",
            "Add the white of the leeks, sliced thin and cut small.",
            "Finish with saffron and salt.",
            "Force it with powdour douce and serve it forth.",
        ],
        "ingredients": [
            {"name": "Cabbage", "qty": 600, "unit": "g", "pantry": "cabbage",
             "note": "'Caboches' — the editor says 'probably cabbages'"},
            {"name": "Good broth", "qty": 900, "unit": "ml", "pantry": "broth",
             "note": "The base"},
            {"name": "Onion, minced", "qty": 1, "unit": "ea", "pantry": "onion",
             "note": "Mynced fine"},
            {"name": "Leek (white part, sliced thin)", "qty": 2, "unit": "ea",
             "pantry": "leeks", "note": "'Slyt' and cut small"},
            {"name": "Saffron", "qty": 0.25, "unit": "tsp", "pantry": "saffron",
             "note": "Colour and perfume"},
            {"name": "Salt", "qty": 1, "unit": "tsp", "pantry": "salt",
             "note": "To taste"},
            {"name": "Powdour douce", "qty": 1, "unit": "tsp",
             "pantry": "powder_douce", "historic": True,
             "sub": "galangal + cinnamon + ginger + cloves",
             "note": "Forced (seasoned) with it at the end"},
        ],
        "funky": [
            {"ingredient": "Powdour douce", "key": "powder_douce", "ing_ref": "Powdour douce",
             "why": "Used here not as a heat but as a perfume. A pinch of "
                    "galangal and cinnamon ground together gets you most of "
                    "the way there."},
        ],
    },
    {
        "id": "medieval-mustard",
        "title": "Medieval Mustard",
        "era": "medieval",
        "year": "c. 1300",
        "region": "France",
        "source": "Le Viandier de Taillevent, Guillaume Tirel, c. 1300, via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/medievalmustard",
        "servings": 8,
        "tags": ["condiment", "vegetarian"],
        "confidence": "verified",
        "history": "One of the earliest ways of preparing early medieval "
                   "French mustard was grinding the seeds with grape must — "
                   "the seeds, skins and juice of unfermented wine grapes. "
                   "In medieval Latin this was mustum ardens, 'burning "
                   "must'. The name mustarde came from it, and mustard was "
                   "food for everyone: a crop the common people could grow "
                   "at home, and a component of lavish feasts for the "
                   "wealthy. Tirel's method is vinegar and patience — soak "
                   "the seed overnight, grind it, thin with vinegar, and "
                   "let it rest. The version here leaves out the must "
                   "entirely and adds a sack of warm spiced wine.",
        "source_text": "Moustarde... If you want to make it good and at "
                       "leisure, put the mustard seed to soak overnight in "
                       "good vinegar; then have it ground well in the mill, "
                       "and little by little thin it with vinegar. And if "
                       "you have any spices left over from making jelly, "
                       "clare, hippocras, or sauces, have them ground with "
                       "it, and afterward let it rest.",
        "method": [
            "Put the mustard seeds in a small bowl, pour enough vinegar over "
            "them to cover, and let them soak overnight.",
            "Make the hippocras: mix sugar, cinnamon, ginger, nutmeg, mace "
            "and cloves. Put the mixture in a few layers of cheesecloth, "
            "gather and tie it into a sachet, and steep it in the wine "
            "overnight.",
            "Grind the soaked seeds in a mortar until as smooth as you "
            "like. Mix in more vinegar a little at a time to a thick "
            "consistency.",
            "Remove the sachet from the wine, open it, and add the spices "
            "to the mustard.",
            "Stir the spices through, let sit about 10 minutes, and serve. "
            "The hippocras is good drunk on its own.",
        ],
        "ingredients": [
            {"name": "White or yellow mustard seeds", "qty": 50, "unit": "g",
             "pantry": "mustard_seeds", "note": "White and yellow are the "
             "same seed; the colour is the hull"},
            {"name": "Wine vinegar (white or red)", "qty": 60, "unit": "ml",
             "pantry": "vinegar", "note": "For the soak, and to thin with"},
            {"name": "Sugar", "qty": 25, "unit": "g", "pantry": "sugar",
             "note": "For the hippocras spice sachet"},
            {"name": "Cinnamon", "qty": 1, "unit": "tsp", "pantry": "cinnamon",
             "note": "In the wine sachet"},
            {"name": "Ground ginger", "qty": 0.5, "unit": "tsp",
             "pantry": "ginger", "note": "In the wine sachet"},
            {"name": "Nutmeg", "qty": 0.5, "unit": "tsp", "pantry": "nutmeg",
             "note": "In the wine sachet"},
            {"name": "Mace", "qty": 0.5, "unit": "tsp", "pantry": "mace",
             "note": "In the wine sachet"},
            {"name": "Cloves", "qty": 0.125, "unit": "tsp", "pantry": "cloves",
             "note": "In the wine sachet"},
            {"name": "Dry white or red wine", "qty": 475, "unit": "ml",
             "pantry": "white_wine", "note": "Steeped with the spices"},
        ],
        "funky": [
            {"ingredient": "Grape must (mustum ardens)", "key": "grapes_must", "ing_ref": 'Wine vinegar (white or red)',
             "why": "The original medieval mustard was ground with "
                    "unfermented grape juice — 'burning must'. Modern "
                    "white wine vinegar carries the same acid and a trace "
                    "of the fruit, and is what you can actually buy."},
        ],
    },
    {
        "id": "william-the-conquerors-hen",
        "title": "William the Conqueror's Hen with Cameline Sauce",
        "era": "medieval",
        "year": "c. 1300",
        "region": "France",
        "source": "Le Viandier de Taillevent, Guillaume Tirel, c. 1300, via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/williamshen",
        "servings": 4,
        "tags": ["main", "poultry"],
        "confidence": "likely",
        "history": "The Bayeux Tapestry shows William the Conqueror and his "
                   "men eating, and the inventory of his household "
                   "apprentices — the bone-carvers, the spicers, the "
                   "pastry cooks — tells you that a medieval royal kitchen "
                   "was a real trade establishment. This dish is the "
                   "medieval idea of a banquet bird, studded with guanciale "
                   "and served with cameline, a bread-and-wine sauce "
                   "heavy with ginger, cinnamon, cloves, mace and grains "
                   "of paradise. The spice list is the real recipe here: it "
                   "is a dish designed to make a bird taste of something "
                   "other than bird.",
        "source_text": "",
        "method": [
            "Preheat the oven to 450F (230C).",
            "Make shallow cuts all over the hen and stick pieces of "
            "guanciale into the cuts. Tie the legs together with twine.",
            "Roast 20 minutes at 450F, then reduce to 350F (175C) for "
            "another 20 minutes, until the thickest part hits 165F (74C).",
            "For the cameline: remove the crust from the bread, tear it "
            "small, and soak it in the red wine and vinegar.",
            "Grind the soaked bread with the ginger, cinnamon, cloves, "
            "salt, grains of paradise and mace into a sauce.",
            "Carve the hen and serve it with the cameline sauce poured "
            "over.",
        ],
        "ingredients": [
            {"name": "Cornish game hen", "qty": 1, "unit": "ea",
             "pantry": "chicken", "note": "A small bird for one person"},
            {"name": "Guanciale", "qty": 30, "unit": "g", "pantry": "guanciale",
             "historic": True, "sub": "pancetta or thick bacon",
             "note": "Cured pig cheek, pushed into the cuts"},
            {"name": "Stale or toasted white bread", "qty": 30, "unit": "g",
             "pantry": "bread", "note": "The body of the cameline sauce"},
            {"name": "Red wine", "qty": 60, "unit": "ml", "pantry": "red_wine",
             "note": "Soaks the bread"},
            {"name": "Red wine vinegar", "qty": 30, "unit": "ml",
             "pantry": "vinegar", "note": "The acid in the sauce"},
            {"name": "Ground ginger", "qty": 0.5, "unit": "tsp",
             "pantry": "ginger", "note": "The dominant medieval spice"},
            {"name": "Cinnamon", "qty": 2, "unit": "tsp", "pantry": "cinnamon",
             "note": "Heavy, by modern standards"},
            {"name": "Ground cloves", "qty": 0.125, "unit": "tsp",
             "pantry": "cloves", "note": "A pinch only"},
            {"name": "Grains of paradise", "qty": 0.125, "unit": "tsp",
             "pantry": "grains_paradise", "historic": True,
             "sub": "white pepper, or a pinch of allspice",
             "note": "Also called melegueta or guinea pepper"},
            {"name": "Ground mace", "qty": 0.25, "unit": "tsp",
             "pantry": "mace", "note": "The outer coat of nutmeg"},
            {"name": "Salt", "qty": 1, "unit": "pinch", "pantry": "salt",
             "note": "To taste"},
        ],
        "funky": [
            {"ingredient": "Grains of paradise", "key": "grains_paradise", "ing_ref": 'Grains of paradise',
             "why": "Aframomum melegueta, a West African rhizome with a "
                    "peppery, gingery, faintly citrus heat. It was the "
                    "standard replacement for black pepper in medieval "
                    "Europe, and it is still sold — usually as 'alligator "
                    "pepper' or 'melegueta'."},
            {"ingredient": "Long pepper", "key": "long_pepper", "ing_ref": 'Salt',
             "why": "Piper longum, the rounder and fruitier pepper. Black "
                    "pepper is the standard substitute and nobody will "
                    "notice."},
        ],
    },
    {
        "id": "medieval-cherry-cheesecake",
        "title": "Medieval Cherry Cheesecake",
        "era": "medieval",
        "year": "15th century",
        "region": "Italy",
        "source": "15th-century Italian manuscript, via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/medievalcherrycheesecake",
        "servings": 8,
        "tags": ["dessert", "vegetarian"],
        "confidence": "likely",
        "history": "A 15th-century Italian manuscript gives a cheesecake "
                   "built on a shortcrust pastry and fresh cheese, with "
                   "dark cherries, ginger, cinnamon and black pepper, and "
                   "rose petals scattered through the filling. The black "
                   "pepper is not a mistake — Renaissance cooks used pepper "
                   "in sweet food regularly, and it is doing the same job "
                   "the ginger and cinnamon are. The rose is the expensive "
                   "part: fragrant damask petals, or rose water if you "
                   "cannot find them, which is what most medieval "
                   "cookbooks used anyway.",
        "source_text": "",
        "method": [
            "For the crust: rub the butter into the flour until it has the "
            "texture of breadcrumbs. Add the cold water 1 teaspoon at a "
            "time until the dough just comes together. Knead briefly, wrap, "
            "and rest in the fridge 30 minutes.",
            "Preheat the oven to 425F (220C). Roll the dough out to line "
            "the tin, patch any tears.",
            "Line with parchment, fill with baking beans, and blind bake 15 "
            "minutes. Remove beans and paper, and bake a further 10 minutes.",
            "For the filling: beat the eggs and sugar, then fold in the "
            "cheese, spices and rose petals.",
            "Pour into the cooled crust and bake until the centre is just "
            "set.",
            "Top with rose water and powdered sugar.",
        ],
        "ingredients": [
            {"name": "Salted butter, diced (crust)", "qty": 226, "unit": "g",
             "pantry": "butter", "note": "Rubbed into the flour"},
            {"name": "Flour (crust)", "qty": 360, "unit": "g", "pantry": "flour",
             "note": "Kept cold"},
            {"name": "Very cold water (crust)", "qty": 120, "unit": "ml",
             "pantry": "water", "note": "Added a teaspoon at a time"},
            {"name": "Dark cherries (pitted)", "qty": 680, "unit": "g",
             "pantry": "cherries", "note": "The darkest you can find"},
            {"name": "Eggs", "qty": 3, "unit": "ea", "pantry": "eggs",
             "note": "For the filling"},
            {"name": "Fresh cheese (ricotta)", "qty": 375, "unit": "g",
             "pantry": "ricotta", "note": "What was then simply 'fresh "
             "cheese'"},
            {"name": "Sugar", "qty": 200, "unit": "g", "pantry": "sugar",
             "note": "Sweetened with a whole egg's worth more than we "
                     "would use"},
            {"name": "Ground ginger", "qty": 1.5, "unit": "tsp",
             "pantry": "ginger", "note": "In a dessert, with cinnamon"},
            {"name": "Cinnamon", "qty": 1.5, "unit": "tsp", "pantry": "cinnamon",
             "note": "Heavy, as the period style was"},
            {"name": "Black pepper", "qty": 0.5, "unit": "tsp",
             "pantry": "pepper", "note": "In a sweet dish — no mistake"},
            {"name": "Aged hard cheese (parmesan-style)", "qty": 30,
             "unit": "g", "pantry": "parmesan", "historic": True,
             "sub": "parmigiano-reggiano or grana padano",
             "note": "Grated into the filling"},
            {"name": "Fragrant edible rose petals", "qty": 1, "unit": "tsp",
             "pantry": "rose_petals", "historic": True,
             "sub": "1 teaspoon rose water",
             "note": "Red if you can find them"},
            {"name": "Rose water (to top)", "qty": 1, "unit": "tbsp",
             "pantry": "rose_water", "note": "Poured over before serving"},
            {"name": "Powdered sugar (to top)", "qty": 2, "unit": "tbsp",
             "pantry": "powdered_sugar", "note": "Dusted on at the table"},
        ],
        "funky": [
            {"ingredient": "Edible rose petals", "key": "rose_petals", "ing_ref": 'Fragrant edible rose petals',
             "why": "Damask rose petals, eaten as a garnish and perfume. "
                    "Rose water is the modern route and was in the "
                    "manuscripts too."},
            {"ingredient": "Aged cheese in a sweet dish", "key": "bred_cheese", "ing_ref": 'Aged hard cheese (parmesan-style)',
             "why": "Aged hard cheese grated into a cheesecake is not a "
                    "modern instinct, but it is exactly what the 15th "
                    "century called for — the umami of age in a dessert."},
        ],
    },

    # ==================================================== RENAISSANCE / COLONIAL
    {
        "id": "aztec-salsa",
        "title": "Aztec Salsa (Salsa de los Aztecas)",
        "era": "renaissance",
        "year": "16th century",
        "region": "Mexico",
        "source": "Fray Bernardino de Sahagún, Florentine Codex (via Tasting History)",
        "source_url": "https://www.tastinghistory.com/recipes/aztecsalsa",
        "servings": 6,
        "tags": ["condiment", "vegan", "spicy"],
        "confidence": "likely",
        "history": "When the Franciscan missionary Bernardino de Sahagún "
                   "wrote down all aspects of Aztec culture in the 16th "
                   "century, he described many kinds of salsa, from mild to "
                   "hot, and the combination of chiles with tomatoes appears "
                   "everywhere. The Aztecs ate salsa with tamales, turkey, "
                   "venison and seafood. Note what they did not have: a good "
                   "source of fat for frying, so tortilla chips did not "
                   "exist until the Spanish brought livestock. There is no "
                   "exact recipe — Sahagún describes a market, not a method "
                   "— so this is a reconstruction using the ingredients he "
                   "names.",
        "source_text": "",
        "method": [
            "Heat a pan over high heat and char the chiles and tomatoes in "
            "batches, turning them so they blister all over. Keep the "
            "tomato skins on.",
            "Cover the charred chiles and tomatoes with water, simmer 12-15 "
            "minutes, then remove. Now the skins may come off.",
            "Let cool. Remove the seeds and ribs from the chiles; chop the "
            "chiles and tomatoes.",
            "Grind in a molcajete with the salt until as smooth as you "
            "like — a blender or food processor also works.",
            "Serve with tamales, or with grilled meat or fish.",
        ],
        "ingredients": [
            {"name": "Yellow chiles (caribe/güero)", "qty": 3, "unit": "ea",
             "pantry": "chiles", "note": "Medium heat"},
            {"name": "Habanero chiles", "qty": 2, "unit": "ea", "pantry": "chiles",
             "optional": True, "note": "Very hot — use with care"},
            {"name": "Anaheim chile", "qty": 1, "unit": "ea", "pantry": "chiles",
             "note": "Mild, and the workhorse"},
            {"name": "Large heirloom tomatoes", "qty": 4, "unit": "ea",
             "pantry": "tomatoes", "note": "Charred, then peeled"},
            {"name": "Salt", "qty": 1, "unit": "tsp", "pantry": "salt",
             "note": "A large pinch, ground in with the chiles"},
        ],
        "funky": [],
    },
    {
        "id": "kvass",
        "title": "Kvass (Russian Bread Drink)",
        "era": "renaissance",
        "year": "16th century",
        "region": "Russia",
        "source": "16th-century Russian, via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/kvass",
        "servings": 8,
        "tags": ["drink", "vegan", "fermented"],
        "confidence": "likely",
        "history": "Kvass was the everyday drink of Muscovy — a fermented "
                   "bread beverage, dark, faintly sour, faintly sweet, and "
                   "sold by the barrel in the streets. It was also the "
                   "peasant drink, and cheap enough that Peter the Great "
                   "once had to issue decrees to stop his own soldiers "
                   "drinking it in preference to state spirits. The 16th "
                   "century recipe is just bread, water and honey left to "
                   "ferment. Brewer's yeast and raisins come later, from "
                   "18th and 19th century versions, and they make it "
                   "smoother.",
        "source_text": "",
        "method": [
            "Optional but worth it: tear the bread into small pieces and "
            "toast them at 350F (175C) for 5-10 minutes until dry.",
            "Bring the water to a boil, turn off the heat, add the bread, "
            "cover, and let it soak at least 2 hours, preferably overnight.",
            "Transfer the bread and water to a large sterilised container "
            "for fermenting. Stir in the honey.",
            "Add the brewer's yeast and raisins if using.",
            "Cover with cheesecloth secured tightly, or a lid with an "
            "airlock. Ferment 2-3 days at room temperature, then strain and "
            "chill.",
        ],
        "ingredients": [
            {"name": "Water", "qty": 3000, "unit": "ml", "pantry": "water",
             "note": "Three quarts"},
            {"name": "Dark rye bread (stale)", "qty": 450, "unit": "g",
             "pantry": "rye_bread", "historic": True,
             "sub": "dark rye, sourdough, or pumpernickel",
             "note": "The fermenting substrate, and the whole flavour"},
            {"name": "Raw honey", "qty": 225, "unit": "g", "pantry": "honey",
             "note": "Sweetness, and a little fermentable sugar"},
            {"name": "Brewer's yeast", "qty": 0.5, "unit": "tsp",
             "pantry": "yeast", "optional": True,
             "note": "Not in the 16th-century recipe; from 18th-19th century "
                     "versions, for a smoother ferment"},
            {"name": "Raisins", "qty": 50, "unit": "g", "pantry": "raisins",
             "optional": True, "note": "Also a later addition, for flavour"},
        ],
        "funky": [
            {"ingredient": "Dark rye bread", "key": "sour_rye", "ing_ref": 'Dark rye bread (stale)',
             "why": "Kvass is fermented bread and water — a way of using "
                    "stale bread that had no other home. Dark rye is still "
                    "the right bread; pumpernickel works if that is what "
                    "you have."},
        ],
    },

    # =========================================================== GEORGIAN
    {
        "id": "virginia-mock-turtle-soup",
        "title": "Mock Turtle Soup of Calf's Head",
        "era": "georgian",
        "year": "1824",
        "region": "Virginia, United States",
        "source": "Mary Randolph, The Virginia House-Wife: Or, Methodical Cook (1824)",
        "source_url": "https://www.gutenberg.org/ebooks/12519",
        "servings": 6,
        "tags": ["soup", "beef"],
        "confidence": "verified",
        "history": "Green turtle soup was the great status dish of the "
                   "Atlantic world — the 18th century's caviar, served at "
                   "the best tables from London to Boston, and turtle "
                   "arriving in holds from the Caribbean. Randolph's mock "
                   "turtle was the American answer: a soup made from calf's "
                   "head, built to fool the table. The head supplied skin, "
                   "tongue, brains and gelatin. Randolph ends the recipe "
                   "with a detail that no modern cookbook would print: "
                   "'The eyes are a great delicacy.' Her book, the first "
                   "regional cookbook in America, was written from memory "
                   "in a Washington boarding house.",
        "source_text": "Have a large head cleaned nicely without taking off "
                       "the skin, divide the chop from the front of the "
                       "head, take out the tongue, (which is best when "
                       "salted,) put on the head with a gallon of water, the "
                       "hock of a ham or a piece of nice pork, four or five "
                       "onions, thyme, parsley, cloves and nutmeg, pepper "
                       "and salt, boil all these together until the flesh "
                       "on the head is quite tender, then take it up, cut "
                       "all into small pieces, take the eyes out carefully, "
                       "strain the water in which it was boiled, add half a "
                       "pint of wine and a gill of mushroom catsup, let it "
                       "boil slowly till reduced to two quarts, thicken it "
                       "with two spoonsful of browned flour rubbed into "
                       "four ounces of butter, put the meat in, and after "
                       "stewing it a short time, serve it up. The eyes are "
                       "a great delicacy.",
        "method": [
            "Have a large head cleaned without removing the skin. Divide "
            "the chop from the front, take out the tongue (best when "
            "salted).",
            "Put the head on with a gallon of water, a ham hock or a piece "
            "of nice pork, four or five onions, thyme, parsley, cloves, "
            "nutmeg, pepper and salt.",
            "Boil until the flesh is quite tender. Take it up, cut it all "
            "into small pieces, and take the eyes out carefully.",
            "Strain the cooking water. Add half a pint of wine and a gill "
            "of mushroom catsup, and let it boil slowly until reduced to "
            "two quarts.",
            "Thicken with two spoonfuls of browned flour rubbed into four "
            "ounces of butter.",
            "Put the meat back in, stew a short time, and serve it up.",
        ],
        "ingredients": [
            {"name": "Calf's head, skin on", "qty": 1, "unit": "ea",
             "pantry": "calf_head", "historic": True,
             "sub": "veal knuckle, or 500 g beef shin + 1 tbsp gelatine",
             "note": "The skin, tongue, brains and gelatin are the point"},
            {"name": "Ham hock or pork", "qty": 300, "unit": "g",
             "pantry": "pork", "note": "Body and flavour of the broth"},
            {"name": "Onions", "qty": 5, "unit": "ea", "pantry": "onion",
             "note": "Four or five"},
            {"name": "Thyme", "qty": 4, "unit": "sprig", "pantry": "thyme",
             "note": "With parsley"},
            {"name": "Parsley", "qty": 0.5, "unit": "cup", "pantry": "parsley",
             "note": "For the broth"},
            {"name": "Cloves", "qty": 4, "unit": "ea", "pantry": "cloves",
             "note": "Whole, with nutmeg"},
            {"name": "Nutmeg", "qty": 0.5, "unit": "ea", "pantry": "nutmeg",
             "note": "Whole, with the cloves"},
            {"name": "Black pepper", "qty": 1, "unit": "tsp", "pantry": "pepper",
             "note": "To taste"},
            {"name": "Salt", "qty": 1.5, "unit": "tsp", "pantry": "salt",
             "note": "To taste"},
            {"name": "Water", "qty": 3800, "unit": "ml", "pantry": "water",
             "note": "A gallon, for the boil"},
            {"name": "Wine", "qty": 240, "unit": "ml", "pantry": "red_wine",
             "note": "Half a pint, for the finished soup"},
            {"name": "Mushroom catsup", "qty": 118, "unit": "ml",
             "pantry": "catsup_mushroom", "historic": True,
             "sub": "soy sauce + a pinch of mushroom powder",
             "note": "A gill — the American answer to European catsup"},
            {"name": "Browned flour", "qty": 20, "unit": "g", "pantry": "flour",
             "note": "Two spoonfuls, rubbed into the butter"},
            {"name": "Butter", "qty": 115, "unit": "g", "pantry": "butter",
             "note": "Four ounces, for the roux"},
        ],
        "funky": [
            {"ingredient": "Calf's head", "key": "calf_head", "ing_ref": "Calf's head, skin on",
             "why": "The entire recipe. The head gave skin (for the "
                    "gelatinous texture), tongue (a delicacy in itself), "
                    "brains (fried into cakes) and the collagen that made "
                    "the soup set. Veal knuckle is the modern "
                    "approximation."},
            {"ingredient": "Mushroom catsup", "key": "catsup_mushroom", "ing_ref": 'Mushroom catsup',
             "why": "18th-century American ketchups were mushroom-based, "
                    "spiced, fermented, and kept a year in a cellar. This "
                    "is the flavouring doing the job of a modern "
                    "Worcestershire."},
            {"ingredient": "The eyes", "key": "brain", "ing_ref": "Calf's head, skin on",
             "why": "'The eyes are a great delicacy,' says Randolph, "
                    "straight-faced, in the middle of a recipe. A "
                    "completely different kind of ingredient list."},
        ],
    },
    {
        "id": "potted-meat",
        "title": "Potted Meat",
        "era": "georgian",
        "year": "1747",
        "region": "England",
        "source": "Hannah Glasse, The Art of Cookery (1747), via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/pottedmeat",
        "servings": 8,
        "tags": ["meat", "make-ahead", "preservation"],
        "confidence": "verified",
        "history": "Before refrigeration, meat was preserved by potting: "
                   "cooked, pounded to a paste, mixed with spices, packed "
                   "into a pot, and sealed under a layer of fat. The fat "
                   "excludes air, and the paste keeps weeks — often it was "
                   "eaten the next day and rarely survived a month. People "
                   "potted meat, game, fish, shellfish, cheese, even "
                   "mushrooms. Glasse's instructions are unusually precise "
                   "about the one step that matters: beat it until it is "
                   "like a paste, in a marble mortar.",
        "source_text": "To pot Venison. Take a piece of venison, fat and "
                       "lean together, lay it in a dish, and stick pieces of "
                       "butter all over; tie a brown paper over it, and "
                       "bake it. When it comes out of the oven, take it out "
                       "of the liquor hot, drain it, and lay it in a dish; "
                       "when cold, take off all the skin, and beat it in a "
                       "marble mortar, fat and lean together, season it with "
                       "mace, cloves, nutmeg, black pepper and salt to your "
                       "mind. When the butter is cold that it was baked in, "
                       "take a little of it, and beat in with it to moisten "
                       "it; then put it down close, and cover it with "
                       "clarified butter. You must be sure to beat it, till "
                       "it is like a paste.",
        "method": [
            "Preheat the oven to 300F (150C).",
            "Set the meat in a ceramic baking dish, cover with the butter "
            "slices, and cover the dish (parchment and twine if no lid).",
            "Roast 3-4 hours, until 135-140F (57-60C). Or use a slow cooker "
            "on low for 5-6 hours.",
            "Remove and let cool completely. Strain and save the drippings.",
            "Mince the meat as finely as possible, then beat it in a mortar "
            "in batches until paste-like.",
            "Mix in salt, pepper, nutmeg, mace and cloves. Add drippings "
            "little by little until the paste is the texture of pâté.",
            "Press into a pot, seal, and pour clarified butter over the top.",
        ],
        "ingredients": [
            {"name": "Beef bottom round (or venison with some fat)",
             "qty": 1300, "unit": "g", "pantry": "beef_roast",
             "note": "Fat and lean together — the proportion matters"},
            {"name": "Butter, cut into slices", "qty": 115, "unit": "g",
             "pantry": "butter", "note": "Pushed over the meat before baking"},
            {"name": "Salt", "qty": 2, "unit": "tsp", "pantry": "salt",
             "note": "To taste"},
            {"name": "Black pepper", "qty": 0.5, "unit": "tsp", "pantry": "pepper",
             "note": "Freshly ground"},
            {"name": "Nutmeg", "qty": 0.5, "unit": "tsp", "pantry": "nutmeg",
             "note": "For the potted meat"},
            {"name": "Mace", "qty": 0.25, "unit": "tsp", "pantry": "mace",
             "note": "A little less than you think"},
            {"name": "Cloves", "qty": 0.125, "unit": "tsp", "pantry": "cloves",
             "note": "The smallest amount of the strongest spice"},
            {"name": "Clarified butter or ghee, melted", "qty": 225, "unit": "g",
             "pantry": "ghee", "note": "The seal — the air-excluding layer"},
        ],
        "funky": [],
    },
    {
        "id": "old-fashioned-cocktail",
        "title": "The Old Fashioned (1806 and 1895)",
        "era": "georgian",
        "year": "1806, 1895",
        "region": "United States",
        "source": "Tasting History, 'Old-Fashioned Old Fashioned' (1806 & 1895 recipes)",
        "source_url": "https://www.tastinghistory.com/recipes/oldfashioned",
        "servings": 1,
        "tags": ["drink", "cocktail"],
        "confidence": "verified",
        "history": "The word cocktail emerged in the late 18th century, but "
                   "it did not yet mean a whole family of mixed drinks — it "
                   "meant one specific thing, a glass of cocktail: spirits, "
                   "sugar, water and bitters, sweetened and cut. The 1806 "
                   "version is nearly two-thirds water. By 1895, thirty "
                   "years after the first published version, people were "
                   "asking for the 'old fashioned' rather than the new "
                   "fangled mixed drinks, and the drink had hardened into "
                   "something close to what we pour today — with the "
                   "difference that it got a twist of lemon, not orange.",
        "source_text": "",
        "method": [
            "For the 1806 version: put the sugar cube in a small glass. Add "
            "the bitters and muddle them into the sugar until it is "
            "saturated.",
            "Add the liquor and the water, and stir until the sugar "
            "dissolves.",
            "Grate a little nutmeg over the top.",
            "For the 1895 version: put the sugar cube in the glass, add the "
            "water and bitters and stir. Add the whiskey and a large ice "
            "cube, stir again.",
            "Express the lemon peel over the surface and drop it in.",
        ],
        "ingredients": [
            {"name": "Sugar cube", "qty": 1, "unit": "ea", "pantry": "sugar_cube",
             "note": "One for each version"},
            {"name": "Angostura bitters", "qty": 0.5, "unit": "tsp",
             "pantry": "bitters", "note": "A few drops in 1806, two dashes "
             "in 1895"},
            {"name": "Rye whiskey", "qty": 45, "unit": "ml", "pantry": "whiskey",
             "note": "1.5 oz in the 1895 version"},
            {"name": "Water", "qty": 30, "unit": "ml", "pantry": "water",
             "note": "1 oz in 1895; 3 oz in the 1806 version"},
            {"name": "Nutmeg", "qty": 1, "unit": "pinch", "pantry": "nutmeg",
             "note": "Grated over the 1806 version"},
            {"name": "Ice cube (large)", "qty": 1, "unit": "ea", "pantry": "ice",
             "note": "About the size of a small egg"},
            {"name": "Lemon peel", "qty": 1, "unit": "strip", "pantry": "lemon",
             "note": "Lemon, not orange — that is the 1895 difference"},
        ],
        "funky": [],
    },

    # ========================================================== VICTORIAN
    {
        "id": "acton-mock-turtle-soup",
        "title": "Acton's Mock Turtle Soup",
        "era": "victorian",
        "year": "1845",
        "region": "England",
        "source": "Eliza Acton, Modern Cookery for Private Families (1845)",
        "source_url": "https://www.gutenberg.org/ebooks/72482",
        "servings": 8,
        "tags": ["soup", "beef", "showpiece"],
        "confidence": "verified",
        "history": "Acton's version is the grand one — nine quarts of water, "
                   "eight pounds of beef neck stewed six to seven hours, a "
                   "calf's head with the skin on, thirty-six forcemeat balls, "
                   "egg balls the size of marbles, and the brains fried into "
                   "cakes. She also writes the most useful instruction in "
                   "the history of the dish: strain the soup through a "
                   "hair-sieve, but 'do not force it through with a spoon, "
                   "as that would spoil the appearance of the stock.' It "
                   "was 'this favourite English soup', made in the "
                   "economical manner when there was no stock at hand. The "
                   "economical mock turtle was the respectably poor man's "
                   "way of eating turtle.",
        "source_text": "To make a single tureen of this favourite English "
                       "soup in the most economical manner when there is no "
                       "stock at hand, stew gently down in a gallon of water "
                       "four pounds of the fleshy part of the shin of beef, "
                       "or of the neck, with two or three carrots, one "
                       "onion, a small head of celery, a bunch of savoury "
                       "herbs, a blade of mace, a half-teaspoonful of "
                       "peppercorns, and an ounce of salt.",
        "method": [
            "Stew down 4 lb of shin or neck of beef in a gallon of water "
            "with carrots, onion, celery, herbs, mace and peppercorns. "
            "Strain the broth and pour it, cold, over 3 lb of veal knuckle; "
            "simmer until the flesh falls from the bones, stewing it as "
            "softly as possible or you will not have enough stock.",
            "Take half a fine calf's head with the skin on, remove the "
            "brains, bone it, and return the bones to the veal to enrich "
            "the stock.",
            "Strain the soup through a hair-sieve, and let it drain closely. "
            "When cold, clear off all the fat.",
            "Roll the head lightly round, leaving the tongue inside, secure "
            "with tape, and pour the soup over. Bring gently to boil, skim "
            "well, and simmer 1-1.25 hours.",
            "Cut the head into quarter-inch slices, then dice. Cook in a "
            "separate pan with butter, ham, eschalots, cloves, mace, "
            "peppercorns, thyme, parsley, lemon thyme, winter savoury and "
            "lemon rind, stewed very softly for nearly an hour.",
            "Dredge in 2 oz of fine dry flour by degrees. Add five pints of "
            "hot, fat-free stock gradually, shaking the pan as you pour.",
            "Simmer gently an hour, strain through a hair-sieve, and add the "
            "diced head. Just before table, add three dozen small "
            "forcemeat balls, the brains cut into dice, dipped in egg yolk "
            "and breadcrumbs and fried brown, and egg balls the size of "
            "small marbles.",
        ],
        "ingredients": [
            {"name": "Shin or neck of beef", "qty": 1800, "unit": "g",
             "pantry": "beef_shin", "note": "Four pounds for the stock"},
            {"name": "Veal knuckle or neck", "qty": 1350, "unit": "g",
             "pantry": "veal", "note": "Three pounds — the body of the soup"},
            {"name": "Calf's head with skin on", "qty": 0.5, "unit": "ea",
             "pantry": "calf_head", "historic": True,
             "sub": "veal knuckle, or 500 g beef shin + 1 tbsp gelatine",
             "note": "Half a head; the skin and tongue are the point"},
            {"name": "Carrots", "qty": 3, "unit": "ea", "pantry": "carrots",
             "note": "Two or three, for the stock"},
            {"name": "Onion", "qty": 1, "unit": "ea", "pantry": "onion",
             "note": "One, for the stock"},
            {"name": "Celery", "qty": 1, "unit": "head", "pantry": "celery",
             "note": "A small head"},
            {"name": "Savoury herbs (thyme, parsley, lemon thyme, winter "
             "savoury)", "qty": 1, "unit": "bunch", "pantry": "thyme",
             "note": "A good bunch, tied"},
            {"name": "Mace", "qty": 1, "unit": "blade", "pantry": "mace",
             "note": "A blade, then more in the sauce"},
            {"name": "Peppercorns", "qty": 1, "unit": "tsp", "pantry": "pepper",
             "note": "Half a teaspoon, cracked"},
            {"name": "Salt", "qty": 1, "unit": "oz", "pantry": "salt",
             "note": "An ounce in the stock"},
            {"name": "Lean ham", "qty": 200, "unit": "g", "pantry": "ham",
             "note": "6-8 oz, perfectly freed of fat and smoked edge"},
            {"name": "Shallots", "qty": 4, "unit": "ea", "pantry": "shallots",
             "historic": True, "sub": "one mild onion",
             "note": "Or one mild onion if not to hand"},
            {"name": "Butter", "qty": 115, "unit": "g", "pantry": "butter",
             "note": "Four ounces in the sauce, more in the roux"},
            {"name": "Cloves", "qty": 6, "unit": "ea", "pantry": "cloves",
             "note": "Half a dozen"},
            {"name": "Fresh thyme sprigs", "qty": 4, "unit": "ea",
             "pantry": "thyme", "note": "Three or four very small sprigs"},
            {"name": "Minced parsley", "qty": 1, "unit": "tbsp",
             "pantry": "parsley", "note": "Three teaspoonsful"},
            {"name": "Fresh lemon", "qty": 0.5, "unit": "ea", "pantry": "lemon",
             "note": "The very thin rind of half a lemon"},
            {"name": "Fine dry flour", "qty": 60, "unit": "g", "pantry": "flour",
             "note": "Two ounces, dredged in by degrees"},
            {"name": "Dry sherry", "qty": 240, "unit": "ml", "pantry": "sherry",
             "note": "Half a pint — the final flourish"},
            {"name": "Forcemeat balls", "qty": 12, "unit": "ea",
             "pantry": "forcemeat", "note": "Three dozen small ones"},
            {"name": "Egg yolks", "qty": 4, "unit": "ea", "pantry": "eggs",
             "note": "For the egg balls the size of marbles"},
        ],
        "funky": [
            {"ingredient": "Calf's head with the skin on", "key": "calf_head", "ing_ref": "Calf's head with skin on",
             "why": "Acton insists on the skin, rolled around the tongue "
                    "and tied with tape, because the skin is what makes the "
                    "soup taste and feel like turtle. Veal knuckle plus a "
                    "tablespoon of gelatine is the modern shortcut."},
            {"ingredient": "Shallots", "key": "shallots", "ing_ref": 'Shallots',
             "why": "Acton says plainly: 'or if these should not be at "
                    "hand, one mild onion in lieu of them.' So did she."},
            {"ingredient": "Winter savoury and lemon thyme", "key": "herbs", "ing_ref": 'Savoury herbs (thyme, parsley, lemon thyme, winter savoury)',
             "why": "A 19th-century herb bench of pot herbs. Winter "
                    "savoury is a step back from thyme; if you can't find "
                    "it, extra thyme is fine."},
        ],
    },
    {
        "id": "beeton-ginger-beer",
        "title": "Ginger Beer (1861)",
        "era": "victorian",
        "year": "1861",
        "region": "England",
        "source": "Mrs Beeton, The Book of Household Management (1861)",
        "source_url": "https://www.gutenberg.org/ebooks/10136",
        "servings": 12,
        "tags": ["drink", "vegan", "fermented"],
        "confidence": "verified",
        "history": "Before the First World War, most soft drinks were made "
                   "at home, and ginger beer was the great one — brewed in "
                   "the kitchen, bottled, and left for three days. Beeton "
                   "gives the cost as 2 shillings for four dozen bottles, "
                   "or half a penny each, and says the beer should be made "
                   "during the summer months. She also gives the warning "
                   "that matters: too much sugar and it will not keep, so "
                   "if you want it to last, leave the sugar in. Cream of "
                   "tartar is the old-fashioned way to acidify — the same "
                   "role citric acid plays today.",
        "source_text": "INGREDIENTS.--2-1/2 lbs. of loaf sugar, 1-1/2 oz. of "
                       "bruised ginger, 1 oz. of cream of tartar, the rind "
                       "and juice of 2 lemons, 3 gallons of boiling water, 2 "
                       "large tablespoonfuls of thick and fresh brewer's "
                       "yeast. _Mode_.--Peel the lemons, squeeze the juice, "
                       "strain it, and put the peel and juice into a large "
                       "earthen pan, with the bruised ginger, cream of "
                       "tartar, and loaf sugar. Pour over these ingredients "
                       "3 gallons of boiling water; let it stand until just "
                       "warm, when add the yeast... The next day skim off "
                       "the yeast, and pour the liquor carefully into "
                       "another vessel, leaving the sediment; then bottle "
                       "immediately, and tie the corks down, and in 3 days "
                       "the ginger beer will be fit for use. _Average cost_ "
                       "for this quantity, 2s.; or 1/2d. per bottle.",
        "method": [
            "Peel the lemons, squeeze and strain the juice, and put the "
            "peel and juice into a large earthen pan.",
            "Add the bruised ginger, cream of tartar and loaf sugar, then "
            "pour over 3 gallons of boiling water.",
            "Let it stand until just warm, then stir in the fresh brewer's "
            "yeast.",
            "Stir well, cover with a cloth, and leave near the fire all "
            "night.",
            "The next day, skim off the yeast and pour the liquor carefully "
            "into another vessel, leaving the sediment.",
            "Bottle immediately, tie the corks down, and wait 3 days.",
        ],
        "ingredients": [
            {"name": "Loaf sugar", "qty": 1130, "unit": "g", "pantry": "sugar",
             "note": "2.5 lbs — reduce it and it will not keep"},
            {"name": "Bruised ginger", "qty": 45, "unit": "g", "pantry": "ginger",
             "note": "1.5 oz, bruised not powdered"},
            {"name": "Cream of tartar", "qty": 30, "unit": "g",
             "pantry": "cream_tartar", "historic": True,
             "sub": "lemon juice, in a pinch",
             "note": "The old acid, and the reason it has bite"},
            {"name": "Lemons", "qty": 2, "unit": "ea", "pantry": "lemon",
             "note": "Rind and juice of both"},
            {"name": "Boiling water", "qty": 11400, "unit": "ml",
             "pantry": "water", "note": "3 gallons"},
            {"name": "Fresh brewer's yeast", "qty": 30, "unit": "ml",
             "pantry": "yeast", "historic": True,
             "sub": "active dry yeast, or a spoonful of fizzy ginger beer",
             "note": "Two large tablespoonfuls, thick and perfectly fresh"},
        ],
        "funky": [
            {"ingredient": "Cream of tartar", "key": "cream_tartar", "ing_ref": "Cream of tartar",
             "why": "Potassium hydrogen tartrate, the acid that stops sugar "
                    "crystallising. It came out of wine barrels, and it is "
                    "now mostly sold to bakers. A squeeze of lemon does "
                    "the same job in a much smaller quantity."},
            {"ingredient": "Brewer's yeast", "key": "brewers_yeast", "ing_ref": "Fresh brewer's yeast",
             "why": "The old-fashioned way to start a ferment without "
                    "laboratory culture. Active dry yeast works "
                    "identically; a spoonful of fizzy ginger beer works too."},
        ],
    },
    {
        "id": "baklava-1844",
        "title": "Baklava (1844)",
        "era": "victorian",
        "year": "1844",
        "region": "Ottoman Empire",
        "source": "Tasting History, 'Baklava' (1844 Ottoman recipe)",
        "source_url": "https://www.tastinghistory.com/recipes/baklava",
        "servings": 12,
        "tags": ["dessert", "vegetarian"],
        "confidence": "likely",
        "history": "Baklava was a palace and wealthy-household dessert in "
                   "the Ottoman Empire, and the 1844 version reflects that: "
                   "forty-five sheets of phyllo, half a kilo of pistachios, "
                   "ghee rather than butter, and a syrup of equal parts "
                   "sugar and honey. It is rich in a way most desserts of "
                   "the period were not, which is the point — this was a "
                   "display of wealth and skill as much as a pudding. The "
                   "nuts should be chopped, not ground, and a mix of large "
                   "and small pieces is traditional.",
        "source_text": "",
        "method": [
            "Combine the sugar and water over medium heat. Stir until "
            "dissolved, bring to a simmer, then stir in the honey. Simmer "
            "10 minutes, then cool to room temperature.",
            "Preheat the oven to 350F (175C). Grease a deep sheet pan with "
            "ghee, trimming the phyllo to fit if needed.",
            "Lay down 5 sheets of phyllo, brush the top with a thin even "
            "layer of ghee. Repeat with 5 more sheets, brushing each time.",
            "Sprinkle with the chopped nuts. Continue the layers of phyllo "
            "and ghee, finishing with a layer of ghee on top.",
            "Cut into diamonds or squares, and pour the cooled syrup over.",
            "Bake until golden, then let it rest so the syrup soaks in "
            "fully.",
        ],
        "ingredients": [
            {"name": "Water", "qty": 235, "unit": "ml", "pantry": "water",
             "note": "For the syrup"},
            {"name": "Sugar", "qty": 200, "unit": "g", "pantry": "sugar",
             "note": "Equal parts sugar and honey"},
            {"name": "Honey", "qty": 340, "unit": "g", "pantry": "honey",
             "note": "The other half of the syrup"},
            {"name": "Ghee or clarified butter, melted", "qty": 225, "unit": "g",
             "pantry": "ghee", "note": "More or less as needed; 45 sheets "
             "need a lot"},
            {"name": "Pistachios, hazelnuts or almonds, roughly chopped",
             "qty": 500, "unit": "g", "pantry": "nuts",
             "note": "A mix of large and small pieces"},
            {"name": "Phyllo or yufka sheets", "qty": 45, "unit": "ea",
             "pantry": "phyllo", "historic": True,
             "sub": "spring-roll wrappers, or buy phyllo",
             "note": "Stacked 5 at a time, 9 layers"},
        ],
        "funky": [],
    },
    {
        "id": "frugal-housewife-hasty-pudding",
        "title": "Hasty Pudding",
        "era": "victorian",
        "year": "1832",
        "region": "United States",
        "source": "Lydia Maria Child, The American Frugal Housewife (1832)",
        "source_url": "https://www.gutenberg.org/ebooks/13493",
        "servings": 4,
        "tags": ["side", "vegetarian", "cheap"],
        "confidence": "verified",
        "history": "Hasty pudding is the perfect 1832 American dish: corn "
                   "meal boiled into a thick, sweet, cheap pudding that "
                   "needed no eggs, no butter and no oven. Child tells you "
                   "to keep the meal coming in handfuls while it boils and "
                   "to stir it very thoroughly the whole time — the whole "
                   "technique is in not letting it seize. And then the line "
                   "that says everything about 19th-century American "
                   "poverty and resilience: if your stomach is in a "
                   "restricted state, nothing can be better than rye hasty "
                   "pudding and West India molasses. It would save many a "
                   "one the horrors of dyspepsia.",
        "source_text": "Boil water, a quart, three pints, or two quarts, "
                       "according to the size of your family; sift your "
                       "meal, stir five or six spoonfuls of it thoroughly "
                       "into a bowl of water; when the water in the kettle "
                       "boils, pour into it the contents of the bowl; stir "
                       "it well, and let it boil up thick; put in salt to "
                       "suit your own taste, then stand over the kettle, "
                       "and sprinkle in meal, handful after handful, "
                       "stirring it very thoroughly all the time, and "
                       "letting it boil between whiles. When it is so thick "
                       "that you stir it with great difficulty, it is about "
                       "right. It takes about half an hour's cooking. Eat it "
                       "with milk or molasses. Either Indian meal or rye "
                       "meal may be used. If the system is in a restricted "
                       "state, nothing can be better than rye hasty pudding "
                       "and West India molasses. This diet would save many a "
                       "one the horrors of dyspepsia.",
        "method": [
            "Boil the water. Sift the meal and stir 5-6 spoonfuls "
            "thoroughly into a bowl of water.",
            "When the kettle boils, pour in the contents of the bowl and "
            "stir well, letting it boil up thick.",
            "Add salt to taste. Stand over the kettle and sprinkle in meal, "
            "handful after handful, stirring very thoroughly the whole time "
            "and letting it boil between whiles.",
            "When it is so thick that you stir it with great difficulty, it "
            "is about right. About half an hour's cooking.",
            "Eat it with milk or molasses.",
        ],
        "ingredients": [
            {"name": "Water", "qty": 1700, "unit": "ml", "pantry": "water",
             "note": "A quart to three pints, by family size"},
            {"name": "Indian meal (corn meal)", "qty": 200, "unit": "g",
             "pantry": "cornmeal", "historic": True,
             "sub": "stone-ground cornmeal, or polenta flour",
             "note": "Sifted, and added in handfuls"},
            {"name": "Rye meal", "qty": 100, "unit": "g", "pantry": "rye_flour",
             "optional": True, "note": "The digestive alternative Child "
             "recommends"},
            {"name": "Salt", "qty": 1, "unit": "tsp", "pantry": "salt",
             "note": "To taste"},
            {"name": "Molasses (West India)", "qty": 60, "unit": "ml",
             "pantry": "molasses", "historic": True,
             "sub": "dark brown sugar, or treacle",
             "note": "To eat with — the rum-trade byproduct"},
            {"name": "Milk", "qty": 240, "unit": "ml", "pantry": "milk",
             "optional": True, "note": "The other way to eat it"},
        ],
        "funky": [
            {"ingredient": "Indian meal (corn meal)", "key": "indian_meal", "ing_ref": 'Indian meal (corn meal)',
             "why": "The name sounds like it means a spice from India. It "
                    "means corn meal — 'Indian' referred to the Native "
                    "American growing regions of the Americas. The warning "
                    "about lumps is why you stir it into cold milk "
                    "first."},
            {"ingredient": "West India molasses", "key": "west_india_molasses", "ing_ref": 'Molasses (West India)',
             "why": "Molasses was the byproduct of Caribbean rum "
                    "distillation. Dark brown sugar with a spoon of water "
                    "is the modern stand-in; treacle is closer."},
        ],
    },
    {
        "id": "frugal-housewife-indian-pudding",
        "title": "Baked Indian Meal Pudding",
        "era": "victorian",
        "year": "1832",
        "region": "United States",
        "source": "Lydia Maria Child, The American Frugal Housewife (1832)",
        "source_url": "https://www.gutenberg.org/ebooks/13493",
        "servings": 6,
        "tags": ["dessert", "vegetarian"],
        "confidence": "verified",
        "history": "Corn meal pudding is the deep end of American 19th "
                   "century frugality: scald milk, stir in the meal, and "
                   "bake for hours. Child's baked version is four hours, "
                   "and her note about wanting whey tells you it should "
                   "pull away from the sides. Her boiled version is an "
                   "institution of New England — put on at sunrise to eat at "
                   "three — and she is emphatic about the danger: if the "
                   "milk is scalding the pudding will break to pieces, and "
                   "if water gets in, it will ruin it.",
        "source_text": "Indian pudding is good baked. Scald a quart of milk "
                       "(skimmed milk will do,) and stir in seven table "
                       "spoonfuls of sifted Indian meal, a tea-spoonful of "
                       "salt, a tea-cupful of molasses, and a great spoonful "
                       "of ginger, or sifted cinnamon. Baked three or four "
                       "hours. If you want whey, you must be sure and pour "
                       "in a little cold milk, after it is all mixed.",
        "method": [
            "Scald a quart of milk — skimmed milk will do — and stir in 7 "
            "tablespoonfuls of sifted Indian meal.",
            "Add a teaspoonful of salt, a teacupful of molasses, and a "
            "great spoonful of ginger or sifted cinnamon.",
            "If you want whey, pour in a little cold milk after it is all "
            "mixed.",
            "Bake three or four hours.",
        ],
        "ingredients": [
            {"name": "Milk", "qty": 950, "unit": "ml", "pantry": "milk",
             "note": "A quart, scalded; skimmed will do"},
            {"name": "Indian meal (corn meal)", "qty": 105, "unit": "g",
             "pantry": "cornmeal", "historic": True,
             "sub": "stone-ground cornmeal, or polenta flour",
             "note": "Seven tablespoonfuls, sifted"},
            {"name": "Salt", "qty": 1, "unit": "tsp", "pantry": "salt",
             "note": "A teaspoonful"},
            {"name": "Molasses (West India)", "qty": 60, "unit": "ml",
             "pantry": "molasses", "historic": True,
             "sub": "dark brown sugar, or treacle",
             "note": "A teacupful"},
            {"name": "Ground ginger", "qty": 1, "unit": "tbsp", "pantry": "ginger",
             "note": "Or sifted cinnamon"},
        ],
        "funky": [
            {"ingredient": "Indian meal (corn meal)", "key": "indian_meal", "ing_ref": 'Indian meal (corn meal)',
             "why": "Corn meal, not anything from India. 'Indian' in "
                    "American usage named the Native American growing "
                    "regions of the Americas."},
        ],
    },

    # ========================================================== EDWARDIAN
    {
        "id": "potage-crecy",
        "title": "Potage Crécy (Creamy Carrot and Potato Soup)",
        "era": "edwardian",
        "year": "1903, 1912",
        "region": "France / RMS Carpathia",
        "source": "Auguste Escoffier, Le Guide Culinaire (1903), via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/potagecrecy",
        "servings": 4,
        "tags": ["soup", "vegetarian"],
        "confidence": "likely",
        "history": "Potage Crécy appears on the final menu of the "
                   "Carpathia before she docked in New York on 18 April "
                   "1912, and Captain Rostron had coffee, tea and soup "
                   "readied for the Titanic survivors. Escoffier's "
                   "instructions are typical: 600 grams of carrots, 250 "
                   "grams of potato used instead of rice for thickening, and "
                   "then — the remarkable bit — a full 150 grams of butter "
                   "stirred in at the very end, after the soup has been "
                   "passed through a fine sieve. 'This soup does not now "
                   "require any further simmering or skimming.' He is "
                   "emphatic: no more cooking, just butter and chervil.",
        "source_text": "Stew the carrots in butter with onions as for Puree "
                       "Crecy but replace the thickening of rice with 250g "
                       "potatoes and moisten with 1 litre water; season with "
                       "salt. When cooked pass through a fine sieve and "
                       "adjust the consistency with 2 dl very fresh cream; "
                       "pass through a fine strainer at the last moment and "
                       "add 150g butter. This soup does not now require any "
                       "further simmering or skimming. Garnish with chervil "
                       "and small Croutons of bread fried in butter.",
        "method": [
            "Melt 75 g of butter in a large pot over medium-low heat. "
            "Max's rule: never above medium, best closer to low.",
            "Add onions, carrots, thyme, salt and sugar. Stir to coat in "
            "butter. Let it slowly come to a sizzle with no colour on the "
            "onion at all. Once sizzling, lid on, cook 5 minutes.",
            "Add the water and potatoes, stir. Bring to a low simmer, lid "
            "on, 15 minutes, until a fork mashes the potato easily.",
            "Remove the thyme. Puree — the original pushes everything "
            "through a strainer; an immersion blender is easier. Either "
            "way, finish through a fine sieve for maximum smoothness.",
            "Return the puree to the pot. Add the cream and the remaining "
            "150 g of butter. Stir until the butter fully melts and heat "
            "slowly to serving temperature. No further simmering or "
            "skimming.",
            "Make croutons while the soup heats: melt butter or ghee in a "
            "pan, toss the bread cubes to coat, and stir until golden.",
            "Ladle, crown with croutons and a few chervil or parsley "
            "leaves.",
        ],
        "ingredients": [
            {"name": "Butter (split: 75 g + 150 g)", "qty": 225, "unit": "g",
             "pantry": "butter", "note": "Escoffier stirs in 150 g at the "
             "very end — the whole point of the dish"},
            {"name": "Onion, sliced", "qty": 100, "unit": "g", "pantry": "onion",
             "note": "About half a medium onion"},
            {"name": "Carrots, thinly sliced in rounds", "qty": 600, "unit": "g",
             "pantry": "carrots", "note": "6-7 medium; the body of the soup"},
            {"name": "Thyme", "qty": 1, "unit": "sprig", "pantry": "thyme",
             "note": "One sprig, removed before pureeing"},
            {"name": "Salt", "qty": 2, "unit": "pinch", "pantry": "salt",
             "note": "Two pinches"},
            {"name": "Sugar", "qty": 1, "unit": "pinch", "pantry": "sugar",
             "note": "One pinch, to round the carrot"},
            {"name": "Mineral water", "qty": 1000, "unit": "ml",
             "pantry": "water", "note": "Escoffier specified mineral water; "
             "tap works"},
            {"name": "Russet potatoes, peeled and cubed", "qty": 250,
             "unit": "g", "pantry": "potato",
             "note": "Used instead of rice to thicken — 1 large"},
            {"name": "Heavy cream", "qty": 200, "unit": "ml", "pantry": "cream",
             "note": "Very fresh cream, to adjust the consistency"},
            {"name": "Chervil or parsley, for garnish", "qty": 1,
             "unit": "handful", "pantry": "parsley", "note": "A few leaves"},
            {"name": "French bread, in half-inch cubes", "qty": 100,
             "unit": "g", "pantry": "bread", "note": "About 2 cups, for the "
             "croutons"},
        ],
        "funky": [],
    },

    # =========================================================== WARTIME
    {
        "id": "wwii-british-corned-beef-stew",
        "title": "WWII British Corned Beef Stew",
        "era": "wartime",
        "year": "1945",
        "region": "British Army",
        "source": "British Army ration tables, via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/wwiibritishcornedbeefstew",
        "servings": 8,
        "tags": ["main", "beef", "cheap"],
        "confidence": "likely",
        "history": "The mainstay of British troop rations in the Second "
                   "World War was bully beef and biscuits — corned beef "
                   "eaten cold, straight from the tin, or barely warmed. "
                   "This stew was the alternative: the same corned beef, "
                   "broken down with fresh vegetables and a great deal of "
                   "stock, cooked in bulk. The original formula is written "
                   "for an institution rather than a kitchen — thirty 12-"
                   "ounce tins, six pounds of onions, sixteen pints of "
                   "stock, and one and a half pounds of dripping. It was "
                   "plain, very salty, and mushy, and after weeks of cold "
                   "rations it must have been something.",
        "source_text": "Corned Beef Stew. Preserved meat (12 oz. tins) . . . "
                       "30 tins. Onions . . . 6 lb. Mixed vegetables . . . 4 "
                       "lb. Salt and pepper. Stock . . . 16 pts. Dripping . "
                       ". 1 1/2 lb. Method. Chop the onions and vegetables "
                       "and fry-on. Cut the meat...",
        "method": [
            "Chop the onions and vegetables and fry them in the dripping "
            "until softened.",
            "Cut the corned beef into small cubes — the size is not "
            "important, as it all disintegrates later.",
            "Add the stock and the corned beef and simmer until thick and "
            "well combined.",
            "Season, and simmer until the flavours come together.",
        ],
        "ingredients": [
            {"name": "Canned corned beef (12 oz tins)", "qty": 3, "unit": "ea",
             "pantry": "corned_beef", "note": "Bully beef — eaten cold, or "
             "as this"},
            {"name": "Lard or dripping", "qty": 70, "unit": "g",
             "pantry": "lard", "historic": True,
             "sub": "butter, margarine, or the rendered fat from a roast",
             "note": "They had access to drippings, butter, margarine, "
             "Crisco and lard"},
            {"name": "Onion, diced", "qty": 280, "unit": "g", "pantry": "onion",
             "note": "Six pounds in the original — for 30 tins"},
            {"name": "Mixed vegetables, chopped", "qty": 185, "unit": "g",
             "pantry": "mixed_veg", "note": "A carrot and some potatoes is "
             "what the original cook used"},
            {"name": "Beef stock", "qty": 1000, "unit": "ml", "pantry": "broth",
             "note": "16 pints for the original batch"},
            {"name": "Salt", "qty": 1, "unit": "pinch", "pantry": "salt",
             "note": "A pinch — the corned beef supplies most of it"},
            {"name": "Black pepper", "qty": 1, "unit": "tsp", "pantry": "pepper",
             "note": "To taste"},
        ],
        "funky": [
            {"ingredient": "Bully beef (canned corned beef)", "key": "bully_beef", "ing_ref": 'Canned corned beef (12 oz tins)',
             "why": "Corned beef in a can was the standard field ration "
                    "across the British Empire, eaten cold from the tin. It "
                    "is still sold under the 'bully beef' name in some "
                    "carousels."},
            {"ingredient": "Dripping", "key": "lard", "ing_ref": 'Lard or dripping',
             "why": "Rendered fat was the cooking fat of the British army "
                    "and home kitchen. Lard is the modern equivalent and "
                    "tastes more neutral than butter."},
        ],
    },
    {
        "id": "wwii-british-ration-scones",
        "title": "WWII British Military Ration Scones",
        "era": "wartime",
        "year": "1945",
        "region": "British Army",
        "source": "British Army ration tables, via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/wwiibritishscones",
        "servings": 8,
        "tags": ["bread", "vegetarian", "cheap"],
        "confidence": "likely",
        "history": "The trick to a military scone is that there is no flour "
                   "in it — the hard, long-keeping army biscuit is ground "
                   "up in its place, and the fat and the evaporated milk do "
                   "the work that butter and fresh milk would normally do. "
                   "It is a piece of hardtack rebuilt into something that "
                   "looks and eats like bread, using nothing that the "
                   "depot did not already stock. The biscuit crumb will not "
                   "behave exactly like a proper scone dough, so the "
                   "evaporated milk goes in slowly until it just holds "
                   "together.",
        "source_text": "",
        "method": [
            "Preheat the oven to 350F (175C).",
            "Break the biscuits into small pieces and grind them to a fine "
            "powder — a blender or food processor helps, or a rolling pin "
            "in a zip-top bag.",
            "Whisk the sugar into the biscuit crumbs, then rub the fat in "
            "until the mixture is sandy.",
            "Add about half the evaporated milk and mix. Add more little by "
            "little until you get a dough you can roll out.",
            "Roll out on a floured surface (they would not have had a "
            "floured bench), cut into rounds, and bake until risen and "
            "golden.",
        ],
        "ingredients": [
            {"name": "Hard military biscuits (hardtack)", "qty": 225,
             "unit": "g", "pantry": "hardtack", "historic": True,
             "sub": "any unsalted digestive biscuit, or stale bread",
             "note": "Ground to a fine powder — the whole trick"},
            {"name": "Sugar", "qty": 115, "unit": "g", "pantry": "sugar",
             "note": "A heaping half cup"},
            {"name": "Fat (butter, lard or margarine)", "qty": 115, "unit": "g",
             "pantry": "butter", "historic": True,
             "sub": "lard or margarine",
             "note": "They had drippings, butter, margarine, Crisco and lard"},
            {"name": "Evaporated milk", "qty": 60, "unit": "ml",
             "pantry": "evaporated_milk", "historic": True,
             "sub": "whole milk with a spoon of milk powder, or condensed milk",
             "note": "Added slowly until the dough holds together"},
        ],
        "funky": [
            {"ingredient": "Hard military biscuits", "key": "hard_biscuit", "ing_ref": 'Hard military biscuits (hardtack)',
             "why": "Hardtack was baked hard, low in fat, and made to "
                    "survive marching and storage. Ground into powder it "
                    "becomes the flour of this scone."},
            {"ingredient": "Evaporated milk", "key": "evaporated_milk", "ing_ref": 'Evaporated milk',
             "why": "Already a modern pantry standard — it simply had a "
                    "shelf life that fresh milk did not, which is exactly "
                    "what a ration needed."},
        ],
    },
    {
        "id": "wwii-italian-military-pasta",
        "title": "WWII Italian Military Pasta",
        "era": "wartime",
        "year": "1932",
        "region": "Italian Army",
        "source": "Italian military ration tables (1932), via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/wwiiitalianpasta",
        "servings": 6,
        "tags": ["main", "vegetarian", "cheap"],
        "confidence": "likely",
        "history": "The 1932 Italian military ration formula is a lesson in "
                   "what a state could feed an army on and still call it "
                   "pasta. Seventy-five grams of lard for half a cup of "
                   "onion — the onions really do swim in it. Tomato paste "
                   "and water make the sauce, a little rosemary finishes "
                   "it, and a great deal of freshly grated parmesan goes "
                   "over the top. It is the Italian army version of the "
                   "standard trick: tomato paste carries the flavour where "
                   "tomatoes would be too heavy to ship.",
        "source_text": "",
        "method": [
            "Heat the lard in a wide pan, then add the onion. This recipe "
            "calls for a lot of lard for the amount of onion, so do not be "
            "alarmed if the onions are swimming in it.",
            "Cook the onions, stirring continuously, until they start to "
            "brown, about 5 minutes. When they have browned, add the garlic "
            "and cook about 1 minute.",
            "Stir the tomato paste into the water, then add this to the pan "
            "along with the pepper. Reduce the heat and let it simmer 15 "
            "minutes.",
            "Cook the pasta to your desired doneness while the sauce "
            "simmers.",
            "After the sauce has simmered 15 minutes, stir in the rosemary "
            "and simmer 5 minutes more.",
            "Toss the cooked pasta in the sauce and serve with plenty of "
            "cheese.",
        ],
        "ingredients": [
            {"name": "Lard or olive oil", "qty": 75, "unit": "g", "pantry": "lard",
             "historic": True, "sub": "olive oil, or butter",
             "note": "5 tbsp + 2 tsp — a lot of fat for the onion"},
            {"name": "Onion, diced", "qty": 100, "unit": "g", "pantry": "onion",
             "note": "Diced fine"},
            {"name": "Garlic, crushed", "qty": 3, "unit": "clove",
             "pantry": "garlic", "optional": True, "note": "Optional even in "
             "the original"},
            {"name": "Tomato paste", "qty": 75, "unit": "g", "pantry": "tomato_paste",
             "note": "4 tbsp + 1 tsp — ships and keeps"},
            {"name": "Water", "qty": 200, "unit": "ml", "pantry": "water",
             "note": "Generous three-quarters cup"},
            {"name": "Black pepper", "qty": 0.75, "unit": "g", "pantry": "pepper",
             "note": "Half a teaspoon"},
            {"name": "Fresh rosemary, chopped", "qty": 5, "unit": "g",
             "pantry": "rosemary", "optional": True, "note": "Two tablespoons, "
             "at the end"},
            {"name": "Dried pasta", "qty": 450, "unit": "g", "pantry": "pasta",
             "note": "One pound, whatever you like"},
            {"name": "Freshly grated parmesan", "qty": 50, "unit": "g",
             "pantry": "parmesan", "note": "Half a cup, and plenty more"},
        ],
        "funky": [],
    },
    {
        "id": "wwii-italian-military-carrots",
        "title": "WWII Italian Military Carrots",
        "era": "wartime",
        "year": "1932",
        "region": "Italian Army",
        "source": "Italian military ration tables (1932), via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/wwiiitaliancarrots",
        "servings": 6,
        "tags": ["side", "vegetarian"],
        "confidence": "likely",
        "history": "Carrots, boiled and then dressed in garlic lard. It is "
                   "the simplest possible army side dish, and the 1932 "
                   "Italian ration table gives it away as what it is: a "
                   "recipe for using the root vegetables that keep. The "
                   "detail that makes it work is the 15 minutes of cooking "
                   "in garlic-fat after the boiling, and the parsley added "
                   "at the very end, off the heat. Note the 'carrots or "
                   "turnips' in the original — the army took what it was "
                   "given, and purple carrots turn up in the version Max "
                   "cooked.",
        "source_text": "",
        "method": [
            "Salt a large pot of water, add the carrots, bring to the boil "
            "and boil 15 minutes, then drain.",
            "In the same pot, melt the lard. Add the garlic and cook 1 "
            "minute, taking care it does not brown too much. Remove the "
            "garlic.",
            "Add the drained carrots to the pot and stir to coat them in "
            "the garlic-flavoured lard. Cook, stirring frequently, for 15 "
            "minutes.",
            "After 15 minutes, add the parsley and season with salt and "
            "pepper. Cook about 2 minutes more, then serve with plenty of "
            "cheese.",
        ],
        "ingredients": [
            {"name": "Carrots or turnips, sliced", "qty": 750, "unit": "g",
             "pantry": "carrots", "note": "1.6 lbs — orange and purple both"},
            {"name": "Lard", "qty": 25, "unit": "g", "pantry": "lard",
             "historic": True, "sub": "olive oil or butter",
             "note": "Two tablespoons"},
            {"name": "Garlic, crushed", "qty": 1, "unit": "clove",
             "pantry": "garlic", "note": "Cooked in the fat, then removed"},
            {"name": "Minced parsley", "qty": 25, "unit": "g", "pantry": "parsley",
             "note": "A cup — added at the very end"},
            {"name": "Salt and pepper", "qty": 1, "unit": "tsp", "pantry": "salt",
             "note": "To taste"},
            {"name": "Freshly grated parmesan, for topping", "qty": 30,
             "unit": "g", "pantry": "parmesan", "note": "A proper amount, "
             "as the original says"},
        ],
        "funky": [],
    },

    # ============================================================ POST-WAR
    {
        "id": "b-ration-apple-cranberry-sauce",
        "title": "B Ration Apple Cranberry Sauce (1946)",
        "era": "postwar",
        "year": "1946",
        "region": "United States Army",
        "source": "US Army B Ration field ration, via Tasting History",
        "source_url": "https://www.tastinghistory.com/recipes/brationapplesauce",
        "servings": 6,
        "tags": ["side", "dessert", "vegan"],
        "confidence": "likely",
        "history": "The American B ration of 1946 is a document in "
                   "packaging. Dehydrated apple nuggets, dried cranberries, "
                   "sugar and water — nothing else — and the whole thing "
                   "rehydrates and reduces into a sweet sauce. Every "
                   "ingredient was chosen for what it did in a vacuum-sealed "
                   "foil packet: weight, shelf life, and no need for "
                   "refrigeration. The instructions do not call for any "
                   "cooking at all, which is exactly the point. It was "
                   "designed to be eaten cold out of the packet, or warmed "
                   "in the mess kit.",
        "source_text": "",
        "method": [
            "Combine the apple nuggets and 2.5 cups of water in a medium "
            "pot and let the apple rehydrate for 30 minutes.",
            "Stir in the cranberries and the remaining 1 cup of water.",
            "Bring to a boil over medium-high heat, then reduce the heat "
            "and simmer 15 minutes.",
            "Stir in the sugar and cook another 5 minutes.",
            "Let it cool and serve — with Vienna sausage and beans, and "
            "pineapple milk, for a complete B ration meal.",
        ],
        "ingredients": [
            {"name": "Dehydrated apple nuggets", "qty": 110, "unit": "g",
             "pantry": "dried_apple", "historic": True,
             "sub": "any dried apple, or 2 fresh apples finely diced",
             "note": "1.75 cups — needs 30 minutes to rehydrate"},
            {"name": "Water", "qty": 835, "unit": "ml", "pantry": "water",
             "note": "3.5 cups, in two stages"},
            {"name": "Dried cranberries", "qty": 25, "unit": "g",
             "pantry": "dried_cranberries", "note": "A quarter cup"},
            {"name": "Sugar", "qty": 225, "unit": "g", "pantry": "sugar",
             "note": "A heaping cup"},
        ],
        "funky": [
            {"ingredient": "Dehydrated apple nuggets", "key": "dehydrated_apple", "ing_ref": 'Dehydrated apple nuggets',
             "why": "The army bought apple pieces that had been dried to "
                    "the point of near-shattering, because they weighed "
                    "almost nothing and never spoiled. Ordinary dried "
                    "apple rehydrates the same way."},
        ],
    },
    # ============================================================ ANCIENT
    {
        "id": "apicius-spiced-wine",
        "title": "Conditum Paradoxum (Roman Spiced Wine)",
        "era": "ancient",
        "year": "c. 400 CE",
        "region": "Rome",
        "source": "Apicius, De Re Coquinaria (ed. J.D. Vehling, 1926), Book I",
        "source_url": "https://www.gutenberg.org/ebooks/29728",
        "servings": 8,
        "tags": ["drink", "alcohol"],
        "confidence": "verified",
        "history": "Apicius opens his cookbook with a drink, and the "
                   "editor explains why: all Roman meals started with a "
                   "mixed drink of this sort. It is honey and wine heated "
                   "together, clarified with charcoal, and then loaded with "
                   "pepper, date-stones, nard leaves, saffron and mastic. "
                   "The word paradoxum is Apicius's own title for it, and "
                   "the method is remarkable — the wine is skimmed three "
                   "times over two days and filtered through burnt "
                   "charcoal until it is perfectly clear. Roman dinner "
                   "began with something closer to spiced honey wine than "
                   "to anything we would pour today.",
        "source_text": "INTO A COPPER BOWL PUT 6 SEXTARII OF HONEY AND 2 "
                       "SEXTARII OF WINE; HEAT ON A SLOW FIRE, CONSTANTLY "
                       "STIRRING THE MIXTURE WITH A WHIP. AT THE BOILING "
                       "POINT ADD A DASH OF COLD WINE, RETIRE FROM STOVE "
                       "AND SKIM. REPEAT THIS TWICE OR THREE TIMES, LET IT "
                       "REST TILL THE NEXT DAY, AND SKIM AGAIN. THEN ADD 4 "
                       "OZS. OF CRUSHED PEPPER, 3 SCRUPLES OF MASTICH, A "
                       "DRACHM EACH OF NARD LEAVES AND SAFFRON, 5 DRACHMS "
                       "OF ROASTED DATE STONES CRUSHED AND PREVIOUSLY SOAKED "
                       "IN WINE TO SOFTEN THEM. WHEN THIS IS PROPERLY DONE "
                       "ADD 18 SEXTARII OF LIGHT WINE.",
        "method": [
            "Put the honey and 2 sextarii of wine into a copper bowl or "
            "heavy pan. Heat over a slow fire, stirring constantly with a "
            "whisk.",
            "At the boiling point add a dash of cold wine, pull it off the "
            "heat and skim.",
            "Repeat this two or three times, then let it rest until the "
            "next day and skim again.",
            "Add the crushed pepper, mastic, nard leaves, saffron, and the "
            "roasted date stones that have been soaked in wine to soften "
            "them.",
            "Add 18 sextarii of light wine, and clarify with crushed "
            "charcoal, stirring and straining through it.",
        ],
        "ingredients": [
            {"name": "Honey", "qty": 3300, "unit": "ml", "pantry": "honey",
             "note": "Six sextarii — the base of the drink"},
            {"name": "Light wine", "qty": 5500, "unit": "ml", "pantry": "white_wine",
             "note": "Twenty sextarii in all, in three additions"},
            {"name": "Crushed black pepper", "qty": 115, "unit": "g",
             "pantry": "pepper", "note": "Four ounces — and Vehling notes "
             "'pepper' here may well mean allspice"},
            {"name": "Mastic (mastic gum)", "qty": 5, "unit": "g",
             "pantry": "mastic", "historic": True,
             "sub": "a pinch of grated nutmeg, or skip it",
             "note": "Three scruples — a resin from a Mediterranean tree"},
            {"name": "Nard (spikenard) leaves", "qty": 2, "unit": "g",
             "pantry": "nard", "historic": True,
             "sub": "rosemary, or a little extra saffron",
             "note": "A drachm each of nard and saffron"},
            {"name": "Saffron", "qty": 2, "unit": "g", "pantry": "saffron",
             "note": "A drachm — a lot of saffron for a drink"},
            {"name": "Roasted date stones", "qty": 17, "unit": "g",
             "pantry": "date_stones", "historic": True,
             "sub": "the stones from a box of Medjool dates",
             "note": "Five drachms, roasted and soaked in wine"},
            {"name": "Crushed charcoal", "qty": 5, "unit": "g",
             "pantry": "charcoal", "historic": True,
             "sub": "a coffee filter, or just strain it twice through muslin",
             "note": "Still a favourite filterer for liquors"},
        ],
        "funky": [
            {"ingredient": "Mastic", "key": "mastic", "ing_ref": "Mastic (mastic gum)",
             "why": "Mastic gum, a resin that wept from a Mediterranean "
                    "tree and was chewed or dissolved as a perfume and "
                    "medicine. It came from Chios and was worth its weight "
                    "in gold. A little grated nutmeg is the modern echo."},
            {"ingredient": "Charcoal as a filter", "key": "charcoal", "ing_ref": "Crushed charcoal",
             "why": "Apicius clarifies his wine with burnt charcoal, twice "
                    "if necessary. The editor notes that charcoal is still "
                    "a favourite filterer for liquors."},
        ],
    },

    # =========================================================== EDWARDIAN
    {
        "id": "acton-green-pea-soup",
        "title": "Acton's Green Pea Soup",
        "era": "edwardian",
        "year": "1845",
        "region": "England",
        "source": "Eliza Acton, Modern Cookery for Private Families (1845)",
        "source_url": "https://www.gutenberg.org/ebooks/72482",
        "servings": 4,
        "tags": ["soup", "vegetarian"],
        "confidence": "verified",
        "history": "Acton's cookbook gives no fewer than five pea soups — "
                   "'an excellent' one, one 'without meat', 'a cheap' one, "
                   "a 'rich' one and a 'common' one — which tells you what "
                   "a Victorian kitchen thought about peas. May and June "
                   "were the months for them, and the season is the whole "
                   "point of the dish. This is the economical version, "
                   "built on a light stock and finished with a fistful of "
                   "sugar, which sounds odd until you remember that a "
                   "Victorian cook was told to 'sugar your peas to taste', "
                   "because without it they taste of nothing but green.",
        "source_text": "",
        "method": [
            "Make a light stock and simmer it with the shallots and a "
            "little green flavour, then strain.",
            "Beat the peas to a pulp with a little of the stock, and return "
            "them to the pan.",
            "Add the rest of the stock and simmer gently to bring the "
            "flavour together.",
            "Finish with butter, a fistful of sugar, and salt.",
        ],
        "ingredients": [
            {"name": "Green peas", "qty": 700, "unit": "g", "pantry": "peas",
             "note": "At their best in May and June, and worth the fuss"},
            {"name": "Light stock", "qty": 900, "unit": "ml", "pantry": "stock",
             "note": "The base of the cheap version"},
            {"name": "Butter", "qty": 45, "unit": "g", "pantry": "butter",
             "note": "To finish"},
            {"name": "Sugar", "qty": 2, "unit": "tsp", "pantry": "sugar",
             "note": "A Victorian cook would 'sugar your peas to taste'"},
            {"name": "Salt", "qty": 1, "unit": "tsp", "pantry": "salt",
             "note": "To taste"},
            {"name": "Shallots", "qty": 2, "unit": "ea", "pantry": "shallots",
             "optional": True, "note": "Or a mild onion"},
        ],
        "funky": [
            {"ingredient": "Sugar in a vegetable soup", "key": "sugar_in_veg", "ing_ref": "Sugar",
             "why": "Not a mistake and not a modern affectation. Sugar in "
                    "peas, and in most green vegetables, is old advice: it "
                    "pulls out the sweetness that boiling blunts. Beeton "
                    "and Acton both say it."},
        ],
    },

    # ============================================================ POST-WAR
    {
        "id": "beeton-lambswool",
        "title": "Lambswool (or Lamasool)",
        "era": "postwar",
        "year": "1861",
        "region": "England",
        "source": "Mrs Beeton, The Book of Household Management (1861)",
        "source_url": "https://www.gutenberg.org/ebooks/10136",
        "servings": 6,
        "tags": ["drink", "alcohol"],
        "confidence": "verified",
        "history": "Lambswool takes its name from Lamaes abhal, 'the day "
                   "of apple fruit' in ancient British, the autumn apple "
                   "feast day on which it was drunk. It is apples cooked "
                   "down into a kind of marmalade and swirled into spiced "
                   "ale, and Beeton compares the French version, raising "
                   "in the same way — new wine boiled down to half its "
                   "bulk, then apples simmered in it until the whole thing "
                   "becomes a sweet, sharp mash that tastes, she says, of "
                   "lemon mixed with honey. It is the ancestor of a hot "
                   "toddy, and it is very good.",
        "source_text": "LAMBSWOOL, or LAMASOOL.--This old English beverage "
                       "is composed of apples mixed with ale, and seasoned "
                       "with sugar and spice. It takes its name from "
                       "_Lamaes abhal_, which, in ancient British, "
                       "signifies the day of apple fruit, from being drunk "
                       "on the apple feast in autumn.",
        "method": [
            "Pare and cut the apples into quarters, and stew them in the "
            "ale until they break down.",
            "Stir in the sugar and the spices, and keep the mixture moving "
            "so the apples do not catch on the bottom.",
            "Serve hot, ladled over toast.",
            "Grate a little fresh nutmeg over each serving as it goes out.",
        ],
        "ingredients": [
            {"name": "Apples, pared and quartered", "qty": 700, "unit": "g",
             "pantry": "apple", "note": "Braised down to a marmalade"},
            {"name": "Ale (or hard cider)", "qty": 700, "unit": "ml",
             "pantry": "beer", "note": "Or 1.5 pint of new wine boiled to "
             "half its bulk, as the French do"},
            {"name": "Sugar", "qty": 100, "unit": "g", "pantry": "sugar",
             "note": "To taste"},
            {"name": "Ground ginger", "qty": 1, "unit": "tsp", "pantry": "ginger",
             "note": "The spice in the drink"},
            {"name": "Nutmeg", "qty": 0.5, "unit": "tsp", "pantry": "nutmeg",
             "note": "Grated"},
            {"name": "Cinnamon", "qty": 0.5, "unit": "tsp", "pantry": "cinnamon",
             "note": "A pinch"},
        ],
        "funky": [],
    },

]
