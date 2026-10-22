#!/usr/bin/env python3
"""Turn the mined novel food scenes into a literary section.

The novel passages are not recipes.  We do not pretend they are.  They
are the *evidence* of what was served, in what room, to what mood --
and that is a different kind of history than an ingredient list.

So the output is a separate collection of "literary feasts": each one
is a passage with its book, author, year and chapter, plus the foods
named in it, and a note on why the passage is in the collection.

A scene qualifies if it names at least two real foods and either
mentions a meal occasion, or describes preparation/eating closely
enough that it is unmistakably a food scene.

Output: novels_generated.json
"""
import json
import os
import re
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(BASE, "novels_food.json")
OUT = os.path.join(BASE, "novels_generated.json")

# ------------------------------------------------------------------ books
BOOK_META = {
    "Dracula": ("Bram Stoker", 1897, "gothic"),
    "Carmilla": ("J. S. Le Fanu", 1872, "gothic"),
    "Varney the Vampire": ("Thomas Peckett Prest", 1847, "gothic"),
    "The Vampyre": ("John Polidori", 1819, "gothic"),
    "The Castle of Otranto": ("Horace Walpole", 1764, "gothic"),
    "Frankenstein": ("Mary Shelley", 1818, "gothic"),
    "Dr Jekyll and Mr Hyde": ("Robert Louis Stevenson", 1886, "gothic"),
    "The Turn of the Screw": ("Henry James", 1898, "gothic"),
    "Wuthering Heights": ("Emily Brontë", 1847, "gothic"),
    "The Picture of Dorian Gray": ("Oscar Wilde", 1890, "gothic"),
    "The Fall of the House of Usher": ("Edgar Allan Poe", 1839, "gothic"),
    "The Yellow Wallpaper": ("Charlotte Perkins Gilman", 1892, "gothic"),
    "A Christmas Carol": ("Charles Dickens", 1843, "victorian"),
    "Oliver Twist": ("Charles Dickens", 1838, "victorian"),
    "The Pickwick Papers": ("Charles Dickens", 1836, "victorian"),
    "Great Expectations": ("Charles Dickens", 1861, "victorian"),
    "David Copperfield": ("Charles Dickens", 1850, "victorian"),
    "Silas Marner": ("George Eliot", 1861, "victorian"),
    "Jane Eyre": ("Charlotte Brontë", 1847, "victorian"),
    "Bleak House": ("Charles Dickens", 1852, "victorian"),
    "Middlemarch": ("George Eliot", 1871, "victorian"),
    "Vanity Fair": ("W. M. Thackeray", 1848, "victorian"),
    "War and Peace": ("Leo Tolstoy", 1869, "russian"),
    "Anna Karenina": ("Leo Tolstoy", 1878, "russian"),
    "Emma": ("Jane Austen", 1815, "regency"),
    "Pride and Prejudice": ("Jane Austen", 1813, "regency"),
    "North and South": ("Elizabeth Gaskell", 1855, "industrial"),
    "Cranford": ("Elizabeth Gaskell", 1851, "industrial"),
    "The Moonstone": ("Wilkie Collins", 1868, "sensation"),
    "The Woman in White": ("Wilkie Collins", 1860, "sensation"),
    "Treasure Island": ("Robert Louis Stevenson", 1883, "adventure"),
    "Robinson Crusoe": ("Daniel Defoe", 1719, "adventure"),
    "Moby-Dick": ("Herman Melville", 1851, "sea"),
    "Ivanhoe": ("Walter Scott", 1820, "romance"),
    "The Talisman": ("Walter Scott", 1825, "romance"),
    "The Wandering Jew": ("Eugène Sue", 1844, "gothic"),
    "The Count of Monte Cristo": ("Alexandre Dumas", 1844, "romance"),
    "Les Misérables": ("Victor Hugo", 1862, "romance"),
    "The Mysteries of Paris": ("Eugène Sue", 1842, "gothic"),
    "The Orphan of the Rhine": ("Edward Qi", 1853, "gothic"),
    "The Vampyre (dup set)": ("John Polidori", 1819, "gothic"),
    "Carmilla (dup set)": ("J. S. Le Fanu", 1872, "gothic"),
    "The Three Musketeers": ("Alexandre Dumas", 1844, "romance"),
}

# Books that are the same work under two ids: keep the better-spelled
# title and drop the duplicate set.
DUP_TITLES = {
    "The Vampyre (dup set)": "The Vampyre",
    "Carmilla (dup set)": "Carmilla",
}

# ------------------------------------------------------------- the foods
# We present the foods by their common name.  The mined vocabulary is
# large; this list is the one worth showing the reader.
FOOD_DISPLAY = {
    "ale": "Ale", "beer": "Beer", "wine": "Wine", "port": "Port",
    "sherry": "Sherry", "claret": "Claret", "champagne": "Champagne",
    "burgundy": "Burgundy", "brandy": "Brandy", "rum": "Rum",
    "cider": "Cider", "tea": "Tea", "coffee": "Coffee",
    "chocolate": "Chocolate", "cocoa": "Cocoa",
    "bread": "Bread", "toast": "Toast", "loaf": "Loaf of bread",
    "roll": "Rolls", "biscuit": "Biscuits", "bun": "Buns",
    "cake": "Cake", "pie": "Pie", "tart": "Tart", "pudding": "Pudding",
    "custard": "Custard", "omelette": "Omelette", "omelet": "Omelette",
    "porridge": "Porridge", "oatmeal": "Oatmeal", "barley": "Barley",
    "rice": "Rice", "sugar": "Sugar", "honey": "Honey",
    "jam": "Jam", "jelly": "Jelly", "molasses": "Molasses",
    "butter": "Butter", "cheese": "Cheese", "cream": "Cream",
    "milk": "Milk", "eggs": "Eggs", "salt": "Salt",
    "pepper": "Pepper", "spices": "Spices", "saffron": "Saffron",
    "cinnamon": "Cinnamon", "nutmeg": "Nutmeg", "ginger": "Ginger",
    "garlic": "Garlic", "mustard": "Mustard", "vinegar": "Vinegar",
    "oil": "Oil", "herbs": "Herbs", "parsley": "Parsley",
    "thyme": "Thyme", "mint": "Mint", "sage": "Sage",
    "beef": "Beef", "steak": "Steak", "mutton": "Mutton",
    "lamb": "Lamb", "pork": "Pork", "ham": "Ham", "bacon": "Bacon",
    "sausage": "Sausage", "veal": "Veal", "calf": "Calf",
    "liver": "Liver", "heart": "Heart", "tongue": "Tongue",
    "blood": "Blood", "brawn": "Brawn", "offal": "Offal",
    "chicken": "Chicken", "turkey": "Turkey", "goose": "Goose",
    "duck": "Duck", "fowl": "Fowl", "game": "Game",
    "venison": "Venison", "hare": "Hare", "rabbit": "Rabbit",
    "boar": "Boar", "bear": "Bear", "roe": "Roe",
    "fish": "Fish", "trout": "Trout", "salmon": "Salmon",
    "herring": "Herring", "mackerel": "Mackerel", "carp": "Carp",
    "pike": "Pike", "sole": "Sole", "cod": "Cod", "eel": "Eel",
    "shrimp": "Shrimp", "lobster": "Lobster", "crab": "Crab",
    "oyster": "Oysters", "caviar": "Caviar", "anchovies": "Anchovies",
    "potato": "Potatoes", "onion": "Onions", "carrot": "Carrots",
    "cabbage": "Cabbage", "celery": "Celery", "beet": "Beetroot",
    "peas": "Peas", "beans": "Beans", "lentils": "Lentils",
    "salad": "Salad", "greens": "Greens", "spinach": "Spinach",
    "mushroom": "Mushrooms", "truffle": "Truffles", "asparagus": "Asparagus",
    "cucumber": "Cucumber", "lemon": "Lemon", "apple": "Apples",
    "plum": "Plums", "cherries": "Cherries", "grapes": "Grapes",
    "raisins": "Raisins", "walnuts": "Walnuts", "almonds": "Almonds",
    "oranges": "Oranges", "stew": "Stew", "broth": "Broth",
    "soup": "Soup", "potage": "Potage", "pottage": "Pottage",
    "hash": "Hash", "mince": "Minced meat", "roast": "Roast",
    "boiled": "Boiled", "baked": "Baked", "fried": "Fried",
    "goulash": "Goulash", "goulach": "Goulash",
    "paprika": "Paprika", "borscht": "Borscht", "borsch": "Borscht",
    "pirog": "Pirog", "blini": "Blini", "stew": "Stew",
    "schnitzel": "Schnitzel", "sauerkraut": "Sauerkraut",
    "kasha": "Kasha", "vareniki": "Vareniki",
    "gammon": "Gammon", "haggis": "Haggis", "chops": "Chops",
    "porter": "Porter", "hock": "Hock", "claret": "Claret",
    "sherry": "Sherry", "tokay": "Tokay", "burgundy": "Burgundy",
    "mulled": "Mulled wine", "negus": "Negus", "cup": "Cup",
    "tray": "Tray", "plate": "Plate", "bowl": "Bowl",
    "tureen": "Tureen", "napkin": "Napkin", "tablecloth": "Tablecloth",
    "cutlery": "Cutlery", "knife": "Knife", "fork": "Fork",
    "spoon": "Spoon", "glass": "Glass", "goblet": "Goblet",
    "plateful": "Plateful", "banquet": "Banquet", "feast": "Feast",
    "supper": "Supper", "dinner": "Dinner", "breakfast": "Breakfast",
    "luncheon": "Luncheon", "tea-table": "Tea-table",
    "kitchen": "Kitchen", "pantry": "Pantry", "larder": "Larder",
    "cellar": "Cellar", "cook": "Cook", "butler": "Butler",
    "housekeeper": "Housekeeper", "servant": "Servants",
    "maidservant": "Maidservant", "scullion": "Scullion",
    "mull": "Mulled wine", "negus": "Negus", "sherry": "Sherry",
    "claret": "Claret", "hock": "Hock", "sack": "Sack",
    "canary": "Canary", "cider": "Cider", "perry": "Perry",
    "waters": "Water", "gravy": "Gravy", "broth": "Broth",
    "mustard": "Mustard", "horseradish": "Horseradish",
    "ketchup": "Ketchup", "catsup": "Catsup", "sauce": "Sauce",
    "toast": "Toast", "biscuits": "Biscuits",
    "honey": "Honey", "treacle": "Treacle", "syrup": "Syrup",
    "posset": "Posset", "punch": "Punch", "cup": "Cup",
    "sherry": "Sherry", "brandy": "Brandy", "gin": "Gin",
    "whisky": "Whisky", "whiskey": "Whisky", "rum": "Rum",
    "cognac": "Cognac", "kirsch": "Kirsch", "slingsby": "Slingsby",
    "bottled": "Bottled beer", "ale": "Ale", "porter": "Porter",
    "malt": "Malt", "hops": "Hops", "yeast": "Yeast",
    "cauliflower": "Cauliflower", "broccoli": "Broccoli",
    "beans": "Beans", "lentils": "Lentils", "peas": "Peas",
    "salad": "Salad", "cucumber": "Cucumber", "radish": "Radish",
    "turnip": "Turnip", "parsnip": "Parsnip", "beet": "Beetroot",
    "carrot": "Carrots", "onion": "Onions", "garlic": "Garlic",
    "celery": "Celery", "potatoes": "Potatoes", "potato": "Potatoes",
    "apples": "Apples", "apple": "Apples", "pear": "Pears",
    "plums": "Plums", "cherries": "Cherries", "grapes": "Grapes",
    "oranges": "Oranges", "lemon": "Lemon", "lemonade": "Lemonade",
    "strawberries": "Strawberries", "berries": "Berries",
    "nuts": "Nuts", "walnuts": "Walnuts", "almonds": "Almonds",
    "sugar": "Sugar", "candy": "Candy", "chocolate": "Chocolate",
    "ices": "Ices", "ice": "Ice", "gelatine": "Gelatine",
    "coffee": "Coffee", "tea": "Tea", "chocolate": "Chocolate",
    "cocoa": "Cocoa", "chicory": "Chicory",
    "swan": "Swan", "peacock": "Peacock", "pheasant": "Pheasant",
    "partridge": "Partridge", "plover": "Plover", "teal": "Teal",
    "rooks": "Rooks", "snipe": "Snipe", "hares": "Hare",
    "rabbits": "Rabbit", "wild": "Wild game", "bison": "Bison",
    "elk": "Elk", "deer": "Deer", "venison": "Venison",
    "porridge": "Porridge", "broth": "Broth", "pottage": "Pottage",
    "stew": "Stew", "hash": "Hash", "pie": "Pie", "tart": "Tart",
    "pudding": "Pudding", "cake": "Cake", "biscuit": "Biscuits",
    "bread": "Bread", "rolls": "Rolls", "roll": "Rolls",
    "toast": "Toast", "cheese": "Cheese", "butter": "Butter",
    "cream": "Cream", "milk": "Milk", "eggs": "Eggs",
    "candied": "Candied", "preserves": "Preserves", "jam": "Jam",
    "jelly": "Jelly", "honey": "Honey", "sugar": "Sugar",
    "sack": "Sack", "canary": "Canary", "claret": "Claret",
    "burgundy": "Burgundy", "tokay": "Tokay", "port": "Port",
    "sherry": "Sherry", "hock": "Hock", "negus": "Negus",
    "punch": "Punch", "mulled": "Mulled wine", "blandy": "Blandy",
    "tea": "Tea", "coffee": "Coffee", "chocolate": "Chocolate",
    "waters": "Water", "broth": "Broth", "soup": "Soup",
    "gravy": "Gravy", "sauce": "Sauce", "mustard": "Mustard",
    "horseradish": "Horseradish", "ketchup": "Ketchup",
    "vinegar": "Vinegar", "oil": "Oil", "butler": "Butler",
    "cook": "Cook", "kitchen": "Kitchen", "pantry": "Pantry",
    "larder": "Larder", "cellar": "Cellar", "scullery": "Scullery",
    "servant": "Servants", "housekeeper": "Housekeeper",
    "scullion": "Scullion", "plate": "Plate", "tray": "Tray",
    "bowl": "Bowl", "tureen": "Tureen", "napkin": "Napkin",
    "tablecloth": "Tablecloth", "glass": "Glass", "goblet": "Goblet",
    "spoon": "Spoon", "knife": "Knife", "fork": "Fork",
    "supper": "Supper", "dinner": "Dinner", "breakfast": "Breakfast",
    "luncheon": "Luncheon", "banquet": "Banquet", "feast": "Feast",
    "revel": "Revel", "gorge": "Gorge", "banqueting": "Banqueting",
    "apples": "Apples", "pears": "Pears", "plums": "Plums",
    "cherries": "Cherries", "grapes": "Grapes", "oranges": "Oranges",
    "lemonade": "Lemonade", "berries": "Berries",
    "strawberries": "Strawberries", "goose": "Goose",
    "turkey": "Turkey", "duck": "Duck", "chicken": "Chicken",
    "poultry": "Poultry", "sausage": "Sausage", "ham": "Ham",
    "bacon": "Bacon", "pork": "Pork", "beef": "Beef",
    "mutton": "Mutton", "lamb": "Lamb", "veal": "Veal",
    "calf": "Calf", "steak": "Steak", "chops": "Chops",
    "gammon": "Gammon", "haggis": "Haggis", "liver": "Liver",
    "heart": "Heart", "tongue": "Tongue", "brawn": "Brawn",
    "blood": "Blood", "roast": "Roast", "boiled": "Boiled",
    "baked": "Baked", "fried": "Fried", "grilled": "Grilled",
    "minced": "Minced", "hash": "Hash", "stew": "Stew",
    "goulash": "Goulash", "paprika": "Paprika", "borscht": "Borscht",
    "pirog": "Pirog", "blini": "Blini", "sauerkraut": "Sauerkraut",
    "schnitzel": "Schnitzel", "kasha": "Kasha", "vareniki": "Vareniki",
    "horseradish": "Horseradish", "sugar": "Sugar", "molasses": "Molasses",
    "treacle": "Treacle", "syrup": "Syrup", "ginger": "Ginger",
    "nutmeg": "Nutmeg", "cinnamon": "Cinnamon", "saffron": "Saffron",
    "spices": "Spices", "herbs": "Herbs", "parsley": "Parsley",
    "thyme": "Thyme", "mint": "Mint", "sage": "Sage",
    "rosemary": "Rosemary", "marjoram": "Marjoram",
    "watercress": "Watercress", "cress": "Cress",
    "cauliflower": "Cauliflower", "broccoli": "Broccoli",
    "spinach": "Spinach", "greens": "Greens", "lettuce": "Lettuce",
    "mushrooms": "Mushrooms", "mushroom": "Mushrooms",
    "truffles": "Truffles", "truffle": "Truffles",
    "asparagus": "Asparagus", "radish": "Radish",
    "turnip": "Turnip", "parsnip": "Parsnip", "beet": "Beetroot",
    "beets": "Beetroot", "peas": "Peas", "beans": "Beans",
    "lentils": "Lentils", "salad": "Salad", "cucumber": "Cucumber",
    "potatoes": "Potatoes", "potato": "Potatoes",
    "onions": "Onions", "onion": "Onions", "garlic": "Garlic",
    "celery": "Celery", "carrots": "Carrots", "carrot": "Carrots",
    "leeks": "Leeks", "leek": "Leeks",
    "sugar": "Sugar", "honey": "Honey", "jam": "Jam", "jelly": "Jelly",
    "molasses": "Molasses", "candy": "Candy", "ices": "Ice",
    "ice": "Ice", "chocolate": "Chocolate", "coffee": "Coffee",
    "tea": "Tea", "cocoa": "Cocoa",
    "ale": "Ale", "porter": "Porter", "beer": "Beer", "cider": "Cider",
    "wine": "Wine", "sack": "Sack", "canary": "Canary",
    "claret": "Claret", "burgundy": "Burgundy", "tokay": "Tokay",
    "port": "Port", "sherry": "Sherry", "hock": "Hock", "negus": "Negus",
    "punch": "Punch", "mulled": "Mulled wine", "brandy": "Brandy",
    "gin": "Gin", "whisky": "Whisky", "rum": "Rum", "cognac": "Cognac",
    "kirsch": "Kirsch", "lemonade": "Lemonade", "water": "Water",
    "broth": "Broth", "soup": "Soup", "pottage": "Pottage",
    "porridge": "Porridge", "gravy": "Gravy", "sauce": "Sauce",
    "mustard": "Mustard", "ketchup": "Ketchup", "vinegar": "Vinegar",
    "oil": "Oil", "salt": "Salt", "pepper": "Pepper",
    "butter": "Butter", "cheese": "Cheese", "cream": "Cream",
    "milk": "Milk", "eggs": "Eggs", "rice": "Rice", "barley": "Barley",
    "oatmeal": "Oatmeal", "bread": "Bread", "toast": "Toast",
    "rolls": "Rolls", "roll": "Rolls", "biscuits": "Biscuits",
    "biscuit": "Biscuits", "cake": "Cake", "pie": "Pie", "tart": "Tart",
    "pudding": "Pudding", "custard": "Custard",
    "omelette": "Omelette", "omelet": "Omelette",
    "kitchen": "Kitchen", "pantry": "Pantry", "larder": "Larder",
    "cellar": "Cellar", "scullery": "Scullery", "cook": "Cook",
    "butler": "Butler", "housekeeper": "Housekeeper",
    "servant": "Servants", "scullion": "Scullion",
    "plate": "Plate", "tray": "Tray", "bowl": "Bowl",
    "tureen": "Tureen", "napkin": "Napkin", "tablecloth": "Tablecloth",
    "glass": "Glass", "goblet": "Goblet", "spoon": "Spoon",
    "knife": "Knife", "fork": "Fork", "plateful": "Plateful",
    "supper": "Supper", "dinner": "Dinner", "breakfast": "Breakfast",
    "luncheon": "Luncheon", "banquet": "Banquet", "feast": "Feast",
    "revel": "Revel", "gorge": "Gorge", "banqueting": "Banqueting",
    "goose": "Goose", "turkey": "Turkey", "duck": "Duck",
    "chicken": "Chicken", "poultry": "Poultry", "sausage": "Sausage",
    "ham": "Ham", "bacon": "Bacon", "pork": "Pork", "beef": "Beef",
    "mutton": "Mutton", "lamb": "Lamb", "veal": "Veal", "calf": "Calf",
    "steak": "Steak", "chops": "Chops", "gammon": "Gammon",
    "haggis": "Haggis", "liver": "Liver", "heart": "Heart",
    "tongue": "Tongue", "brawn": "Brawn", "blood": "Blood",
    "roast": "Roast", "boiled": "Boiled", "baked": "Baked",
    "fried": "Fried", "grilled": "Grilled", "minced": "Minced",
    "hash": "Hash", "stew": "Stew", "goulash": "Goulash",
    "paprika": "Paprika", "borscht": "Borscht", "pirog": "Pirog",
    "blini": "Blini", "sauerkraut": "Sauerkraut",
    "schnitzel": "Schnitzel", "kasha": "Kasha", "vareniki": "Vareniki",
    "venison": "Venison", "hare": "Hare", "rabbit": "Rabbit",
    "game": "Game", "boar": "Boar", "bear": "Bear",
    "fish": "Fish", "trout": "Trout", "salmon": "Salmon",
    "herring": "Herring", "mackerel": "Mackerel", "carp": "Carp",
    "pike": "Pike", "sole": "Sole", "cod": "Cod", "eel": "Eel",
    "shrimp": "Shrimp", "lobster": "Lobster", "crab": "Crab",
    "oyster": "Oysters", "caviar": "Caviar", "anchovies": "Anchovies",
    "roe": "Roe",
    "walnuts": "Walnuts", "almonds": "Almonds", "nuts": "Nuts",
    "apples": "Apples", "pears": "Pears", "plums": "Plums",
    "cherries": "Cherries", "grapes": "Grapes", "oranges": "Oranges",
    "lemon": "Lemon", "lemonade": "Lemonade", "berries": "Berries",
    "strawberries": "Strawberries", "watercress": "Watercress",
    "cress": "Cress", "leeks": "Leeks", "leek": "Leeks",
    "peas": "Peas", "beans": "Beans", "lentils": "Lentils",
    "spinach": "Spinach", "greens": "Greens", "lettuce": "Lettuce",
    "mushrooms": "Mushrooms", "truffles": "Truffles",
    "asparagus": "Asparagus", "radish": "Radish", "turnip": "Turnip",
    "parsnip": "Parsnip", "beet": "Beetroot", "beets": "Beetroot",
    "cucumber": "Cucumber", "salad": "Salad", "celery": "Celery",
    "carrots": "Carrots", "carrot": "Carrots", "garlic": "Garlic",
    "onion": "Onions", "onions": "Onions", "potato": "Potatoes",
    "potatoes": "Potatoes", "sugar": "Sugar", "honey": "Honey",
    "jam": "Jam", "jelly": "Jelly", "treacle": "Treacle",
    "syrup": "Syrup", "candy": "Candy", "ices": "Ice", "ice": "Ice",
    "chocolate": "Chocolate", "coffee": "Coffee", "tea": "Tea",
    "cocoa": "Cocoa", "ale": "Ale", "porter": "Porter", "beer": "Beer",
    "cider": "Cider", "wine": "Wine", "sack": "Sack",
    "canary": "Canary", "claret": "Claret", "burgundy": "Burgundy",
    "tokay": "Tokay", "port": "Port", "sherry": "Sherry", "hock": "Hock",
    "negus": "Negus", "punch": "Punch", "mulled": "Mulled wine",
    "brandy": "Brandy", "gin": "Gin", "whisky": "Whisky", "rum": "Rum",
    "cognac": "Cognac", "kirsch": "Kirsch", "lemonade": "Lemonade",
    "water": "Water", "broth": "Broth", "soup": "Soup",
    "pottage": "Pottage", "porridge": "Porridge", "gravy": "Gravy",
    "sauce": "Sauce", "mustard": "Mustard", "ketchup": "Ketchup",
    "vinegar": "Vinegar", "oil": "Oil", "salt": "Salt",
    "pepper": "Pepper", "butter": "Butter", "cheese": "Cheese",
    "cream": "Cream", "milk": "Milk", "eggs": "Eggs", "rice": "Rice",
    "barley": "Barley", "oatmeal": "Oatmeal", "bread": "Bread",
    "toast": "Toast", "rolls": "Rolls", "biscuits": "Biscuits",
    "cake": "Cake", "pie": "Pie", "tart": "Tart", "pudding": "Pudding",
    "custard": "Custard", "omelette": "Omelette",
    "kitchen": "Kitchen", "pantry": "Pantry", "larder": "Larder",
    "cellar": "Cellar", "scullery": "Scullery", "cook": "Cook",
    "butler": "Butler", "housekeeper": "Housekeeper",
    "plate": "Plate", "tray": "Tray", "bowl": "Bowl",
    "tureen": "Tureen", "napkin": "Napkin", "tablecloth": "Tablecloth",
    "glass": "Glass", "goblet": "Goblet", "spoon": "Spoon",
    "knife": "Knife", "fork": "Fork", "plateful": "Plateful",
    "supper": "Supper", "dinner": "Dinner", "breakfast": "Breakfast",
    "luncheon": "Luncheon", "banquet": "Banquet", "feast": "Feast",
    "revel": "Revel", "gorge": "Gorge",
    "goose": "Goose", "turkey": "Turkey", "duck": "Duck",
    "chicken": "Chicken", "poultry": "Poultry", "sausage": "Sausage",
    "ham": "Ham", "bacon": "Bacon", "pork": "Pork", "beef": "Beef",
    "mutton": "Mutton", "lamb": "Lamb", "veal": "Veal", "calf": "Calf",
    "steak": "Steak", "chops": "Chops", "gammon": "Gammon",
    "haggis": "Haggis", "liver": "Liver", "heart": "Heart",
    "tongue": "Tongue", "brawn": "Brawn", "blood": "Blood",
    "roast": "Roast", "boiled": "Boiled", "baked": "Baked",
    "fried": "Fried", "grilled": "Grilled", "minced": "Minced",
    "hash": "Hash", "stew": "Stew", "goulash": "Goulash",
    "paprika": "Paprika", "borscht": "Borscht", "pirog": "Pirog",
    "blini": "Blini", "sauerkraut": "Sauerkraut",
    "schnitzel": "Schnitzel", "kasha": "Kasha", "vareniki": "Vareniki",
    "venison": "Venison", "hare": "Hare", "rabbit": "Rabbit",
    "game": "Game", "boar": "Boar", "bear": "Bear",
    "fish": "Fish", "trout": "Trout", "salmon": "Salmon",
    "herring": "Herring", "mackerel": "Mackerel", "carp": "Carp",
    "pike": "Pike", "sole": "Sole", "cod": "Cod", "eel": "Eel",
    "shrimp": "Shrimp", "lobster": "Lobster", "crab": "Crab",
    "oyster": "Oysters", "caviar": "Caviar", "anchovies": "Anchovies",
    "roe": "Roe", "walnuts": "Walnuts", "almonds": "Almonds",
    "nuts": "Nuts", "apples": "Apples", "pears": "Pears",
    "plums": "Plums", "cherries": "Cherries", "grapes": "Grapes",
    "oranges": "Oranges", "lemon": "Lemon", "berries": "Berries",
    "strawberries": "Strawberries", "watercress": "Watercress",
    "cress": "Cress", "leeks": "Leeks", "peas": "Peas",
    "beans": "Beans", "lentils": "Lentils", "spinach": "Spinach",
    "greens": "Greens", "lettuce": "Lettuce", "mushrooms": "Mushrooms",
    "truffles": "Truffles", "asparagus": "Asparagus",
    "radish": "Radish", "turnip": "Turnip", "parsnip": "Parsnip",
    "beet": "Beetroot", "cucumber": "Cucumber", "salad": "Salad",
    "celery": "Celery", "carrots": "Carrots", "garlic": "Garlic",
    "onion": "Onions", "onions": "Onions", "potatoes": "Potatoes",
    # The mining vocabulary is wider than this display map, so anything
    # it finds but this map lacks is silently dropped -- and if that
    # leaves fewer than two labels the whole passage is thrown away.
    # These are the real foods that were falling through that gap.
    #
    # TRAP: the display label must be the word that is actually in the
    # passage, or the chip lies.  "flesh" in a vampire passage is not
    # "Meat" -- it is what is being eaten, and saying "Meat" when the
    # text says "flesh" is a small lie in a corpus whose whole promise
    # is that the quote is the evidence.  Label it "Flesh".  Same for
    # "pig" -> "Pig", not "Pork": the text says pig, and the animal on
    # the page is the animal the reader can check.
    "meat": "Meat", "flesh": "Flesh", "sheep": "Sheep", "goat": "Goat",
    "pig": "Pig", "ox": "Ox", "baron": "Baron", "egg": "Egg",
    "orange": "Oranges", "grape": "Grapes", "cherry": "Cherries",
    "lime": "Lime", "vegetables": "Vegetables", "spice": "Spices",
    "head": "Head", "kidney": "Kidney", "whey": "Whey", "curds": "Curd",
    "mace": "Mace", "halibut": "Halibut", "perch": "Perch",
    "beefsteak": "Beefsteak", "chop": "Chops", "bones": "Bones",
    "bone": "Bones", "platter": "Platter", "mole": "Mole",
    "mouse": "Mouse", "rat": "Rat", "vermin": "Vermin",
    "red pepper": "Red pepper", "black pepper": "Black pepper",
    "tarts": "Tarts", "cakes": "Cakes", "groove": "Groove",
    "entrails": "Entrails", "carcass": "Carcass", "palate": "Palate",
    "lard": "Lard", "bacon": "Bacon",
}

# the mining vocabulary is noisy: these are structural, not food
NOT_FOOD = {
    "table", "tray", "plate", "bowl", "tureen", "napkin", "tablecloth",
    "glass", "goblet", "spoon", "knife", "fork", "plateful", "cup",
    "kitchen", "pantry", "larder", "cellar", "scullery", "cook",
    "butler", "housekeeper", "servant", "scullion", "supper", "dinner",
    "breakfast", "luncheon", "banquet", "feast", "revel", "gorge",
    "banqueting", "fire", "hearth", "smoke", "fumes", "stench",
    "appetite", "hunger", "thirst", "savour", "savor", "taste",
    "water", "salt", "pepper", "sauce", "gravy", "broth", "soup",
    "mustard", "ketchup", "vinegar", "oil", "herbs", "spices",
    "roast", "boiled", "baked", "fried", "grilled", "minced", "hash",
    "stew", "potage", "pottage", "gorge", "slingsby", "blandy",
    "mulled", "posset", "punch", "negus", "bottled", "gelatine",
    "barm", "candied", "preserves", "ices", "ice", "candy",
    "mutton", "veal", "calf", "steak", "chops", "gammon", "haggis",
    "liver", "heart", "tongue", "brawn", "blood", "offal",
    "poultry", "game", "wild", "roe", "shellfish", "seafood",
    "greens", "salad", "spices", "sugar", "honey", "jam", "jelly",
    "treacle", "syrup", "molasses",
    # Context, adjectives and people, not things on the table.  These
    # were eating the two food slots a passage needs to qualify, and
    # each one that took a slot also cost a real dish its label.
    "dining-room", "dining room", "public-house", "public house",
    "meal", "dish", "dishes", "service", "hospitality", "hospitable",
    "refreshment", "provisions", "provision", "store", "fast",
    "poor", "rich", "simple", "plain", "sweet", "humble", "coarse",
    "meagre", "paltry", "exquisite", "sumptuous", "delicious",
    "savoury", "epicure", "epicurean", "gourmand", "carouse",
    "carousing", "debauch", "merrymaking", "revelry", "orgy", "orgies",
    "avarice", "rapacity", "voracity", "greed", "epicure",
    "maid", "waiter", "footman", "manners", "hostelry", "tavern",
    "inn", "cottage", "hut", "farmhouse", "peasant", "serf",
    "hungarian", "russian", "polish", "bohemian", "russia", "hungary",
    "poland", "christmas", "easter", "holy", "blessed", "stolen",
    "smoking", "odour", "odor", "reeking", "pot", "kettle", "oven",
    "boiler", "ladle", "basin", "mill", "range", "vault", "fires",
    "carve", "carving", "devour", "recipe", "cooking", "cookery",
    "cooks", "basil", "baron",
    # False friends: the word is real, but the matches are not food.
    # "head" is nearly always "headache"/"turned his head"; "fast" is
    # "fast asleep"/"travelling fast"; "baron" is a title, not a cut.
    "head", "fast", "baron",
}

# Passages that are not food scenes but slipped through.  Note that
# dialogue tags like "he said" are NOT grounds for rejection -- a food
# scene in a novel is very often somebody talking at the table, and
# rejecting on "he said" threw away the single best Dracula passage.
REJECT = re.compile(
    r"(?:\bI shall\b|\bI will\b|"
    r"\bthis ebook\b|\bGutenberg\b|\btranscriber\w*\b|"
    r"\bcopyright\b|\bpublic domain\b|\bdonate\b|\bpatreon\b|"
    r"newsletter|\bskip to content\b|\bopen menu\b|\bclose menu\b|"
    r"\bwatch the episode\b|\bmy curated collection\b|"
    r"\baffiliate links\b|\bthanks for reading\b|\bchapter\s+\w+\s*$|"
    r"\[illustration|\ball rights reserved\b)",
    re.I)

# a scene must be really about food
STRONG = re.compile(
    r"\b(?:eat|eating|ate|devour|devoured|feast|feasting|banquet|"
    r"supper|dinner|breakfast|luncheon|meal|table|plate|plateful|"
    r"serve|served|drink|drank|drinking|relish|gorge|glutton|"
    r"appetite|hunger|thirst|cook|cooking|cooked|kitchen|"
    r"dining|tasting|sip|bit|ate)\b", re.I)

# A MEAL actually happening, as opposed to the word "table" turning up
# in "he put the file on the table".  Used to admit a passage that names
# only one food but clearly describes a meal being eaten or laid out:
# "I found supper already laid out" is a food scene even when the only
# dish named is the supper itself.
MEAL_EVENT = re.compile(
    r"\b(?:supper|dinner|breakfast|luncheon|breakfast-room|banquet|feast|"
    r"revel|ate|eat|eaten|eating|devour(?:ed)?|gorge(?:d)?|taste(?:d)?|"
    r"served|serve|dining|meal|dined|dining-room|table was|tablecloth|"
    r"laid out|lay the table|waiter|hostess|butler|servant brought|"
    r"brought in|served up|carve[ds]? the|helpings?|plate of|"
    r"smoked|drank|drinking|drink|glass of|pot of|tureen|platter|"
    r"breakfast-room|supper-room)\b", re.I)


def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "--").replace("–", "-")
    return s


def main():
    scenes = json.load(open(IN))
    out = []
    seen = set()

    for sc in scenes:
        book = sc["book"]
        text = sc["text"]
        if not book or not text:
            continue
        if REJECT.search(text):
            continue
        if not STRONG.search(text):
            continue

        # real foods named
        foods = []
        for w in sc.get("foods", []):
            w = w.lower().strip()
            if not w or w in NOT_FOOD:
                continue
            disp = FOOD_DISPLAY.get(w)
            if not disp:
                continue
            if disp not in foods:
                foods.append(disp)

        # The gate.  A passage qualifies if it names two or more real
        # foods, OR one real food AND an actual meal event -- "I found
        # supper already laid out" is a food scene even when the only
        # dish named is the supper.  Requiring two foods unconditionally
        # threw away more than half the corpus.
        if len(foods) < 2:
            if len(foods) < 1 or not MEAL_EVENT.search(text):
                continue

        # the passage has to actually be about a meal
        if not re.search(
                r"\b(?:supper|dinner|breakfast|luncheon|banquet|feast|"
                r"eat|eating|ate|devour|table|plate|serve|served|"
                r"dining|meal|gorge|appetite|hunger|drink|drank|"
                r"revel|feasting|tasting|supper)\b", text, re.I):
            continue

        meta = BOOK_META.get(book)
        if not meta:
            continue
        author, year, kind = meta
        canon = DUP_TITLES.get(book, book)

        key = (canon, text[:90])
        if key in seen:
            continue
        seen.add(key)

        out.append({
            "id": f"lit-{abs(hash(key)) % 10**9}",
            "book": canon,
            "author": author,
            "year": year,
            "kind": kind,
            "chapter": sc.get("chapter", ""),
            "text": clean(text),
            "foods": foods[:10],
        })

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"Literary feasts: {len(out)}")
    print("  by book:")
    for k, v in Counter(o["book"] for o in out).most_common(20):
        print(f"    {v:>4}  {k}")
    print("  by kind:")
    for k, v in Counter(o["kind"] for o in out).most_common():
        print(f"    {v:>4}  {k}")


if __name__ == "__main__":
    main()
