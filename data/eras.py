"""Era taxonomy for The Historical Kitchen.

Nine eras, 2000 BCE to 1946. Order is chronological and drives the filter
rail and the timeline. `era` keys are stable; `label` is what the user reads.
"""

ERAS = [
    {
        "key": "ancient",
        "label": "Ancient",
        "span": "3000 – 1000 BCE",
        "blurb": "Clay tablets, temple kitchens, river-valley agriculture. "
                 "Recipes here are often lists of goods rather than instructions.",
    },
    {
        "key": "roman",
        "label": "Roman",
        "span": "100 BCE – 500 CE",
        "blurb": "The most complete surviving Roman cookbook, compiled around "
                 "400 CE. Salt, garum, laser, and a taste for game.",
    },
    {
        "key": "medieval",
        "label": "Medieval",
        "span": "1200 – 1500",
        "blurb": "English and French manuscripts in Middle English and Latin. "
                 "Saffron, almond milk, and spices worth their weight in silver.",
    },
    {
        "key": "renaissance",
        "label": "Renaissance & Colonial",
        "span": "1500 – 1650",
        "blurb": "Old World and New collide. Aztec moles, Russian kvass, "
                 "and the first printed cookbooks.",
    },
    {
        "key": "georgian",
        "label": "Georgian",
        "span": "1700 – 1830",
        "blurb": "Potted meats, first cocktails, and the birth of American "
                 "regional cooking in Virginia.",
    },
    {
        "key": "victorian",
        "label": "Victorian",
        "span": "1837 – 1901",
        "blurb": "The age of Mrs Beeton. Temperance recipes, Ottoman baklava, "
                 "and mock turtle for every aspirational table.",
    },
    {
        "key": "edwardian",
        "label": "Edwardian",
        "span": "1901 – 1914",
        "blurb": "Escoffier at the peak of the great hotels — silk-smooth "
                 "purées and butter used like a spice.",
    },
    {
        "key": "wartime",
        "label": "Wartime",
        "span": "1914 – 1945",
        "blurb": "Two wars of rationing. Officers and soldiers improvised "
                 "from whatever the depot issued that week.",
    },
    {
        "key": "postwar",
        "label": "Post-War",
        "span": "1945 – 1960",
        "blurb": "Dehydrated rations, standardised packaging, and the "
                 "beginning of the processed-food century.",
    },
]

ERA_ORDER = [e["key"] for e in ERAS]
ERA_BY_KEY = {e["key"]: e for e in ERAS}
