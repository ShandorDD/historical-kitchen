"""Cuisine families for the Historical Kitchen.

The `region` field on a recipe is free text and carries a lot of
detail: "Alcatraz Island, United States of America", "Rome | Britain",
"Titanic | United Kingdom | France".  Showing every distinct string as
a filter button produces ninety chips, most of them matching one
recipe, which is worse than no filter at all.

So we map each region string onto a cuisine family, and the filter
shows families.  The order of the rules below is the order of
precedence: a specific country beats a broad region, so "Roman
Britain" is British, not Roman.
"""
import re

# (family, regex) -- first match wins, so order from specific to broad.
FAMILY_RULES = [
    ("Hungarian", r"\b(hungar\w*|magyar)\b"),
    ("Russian", r"\b(russian|russia\w*)\b"),
    ("Polish", r"\b(polish|poland\w*)\b"),
    ("Jewish (Ashkenazi)", r"\b(jew\w*|kosher)\b"),
    ("Slavic & Eastern European",
     r"\b(slav\w*|ruthen\w*|czech|moravian|bulgarian|serbian|romanian|"
     r"yugoslav|croatian|slovak|silesian|ukrain\w*|moldav\w*|"
     r"transylvan\w*|wallachia|bessarabia|volhynia|galicia|"
     r"carpath\w*|magyars|huns|avars)\b"),
    ("Turkish & Ottoman",
     r"\b(turkish|turkey|ottoman|constantinople|byzantine)\b"),
    ("Greek", r"\b(greek|greece|athen\w*|catalo\w*)\b"),
    ("Ancient & Near Eastern",
     r"\b(sumer\w*|babylon\w*|assyri\w*|mesopotami\w*|abbasid|"
     r"baghdad|caldera|persia\w*|iran\w*|arabia\w*|arabian|"
     r"carthage\w*|phoenicia\w*|phoenician|jerusalem|israel\w*|"
     r"hebrew|palestin\w*|syria\w*|egypt\w*|nubia\w*|mongol\w*|"
     r"gaul|gauls|celtic\w*|pompeii|pompei|viking\w*|norse\w*|"
     r"wampanoag|canada|canadian|soviet union|soviet|"
     r"ö tztal|otztal|alps)\b"),
    ("Ancient Rome", r"\b(roma|roman|rome|latin)\b"),
    ("Italian",
     r"\b(italian|italy|naples|venice|venetian|florence|florentine|"
     r"sicil\w*|milan|milanese|turin|parma|modena|lucca|genoa|genoese|"
     r"bologna|verona|siena|marche\w*|lombard\w*|piedmont\w*|"
     r"tuscan\w*|veneto\w*|sicily|sardinia)\b"),
    ("French",
     r"\b(french|france|paris|lyon|normand\w*|provence|burgund\w*|"
     r"brittany|bretagne|gascon\w*|alsace|champagne|provence|"
     r"gascogne|poitou|anjou|touraine|bordeaux|marseille|"
     r"normandy|dauphine)\b"),
    ("German & Austrian",
     r"\b(german|germany\w*|prussian|bavarian|saxon|swiss|austrian|"
     r"viennese|vienna|tyrol\w*|bohemian|silesian|volhynia|"
     r"rhineland|strassburg|swabia|hessen|westphalia|austria|"
     r"german, |swiss, )\b"),
    ("British & Irish",
     r"\b(english|england|britain|british|scotland|scotch|irish|"
     r"ireland|wales|welsh|manx|cornwall|cumbria|yorkshire|"
     r"lancashire|middlesex|surrey|kent|sussex|essex|devon|"
     r"hertfordshire|hampshire|oxfordshire|wiltshire|dorset|"
     r"northumberland|staffordshire|nottinghamshire|leicestershire|"
     r"london|edinburgh|glasgow|dublin|bristol|oxford|cambridge|"
     r"birmingham|manchester|liverpool|portsmouth|pembroke|"
     r"isle of wight|shropshire|united kingdom|royal navy|"
     r"british army|army, britain)\b"),
    ("Netherlandish & Low Countries",
     r"\b(netherland\w*|dutch|holland|belgi\w*|flemish|flanders|"
     r"zeeland|holland, )\b"),
    ("Iberian & Mediterranean",
     r"\b(spanish|spain|portuguese|portugal|andalus\w*|catalon\w*|"
     r"aragon\w*|castile|morocco|tunisia|algeria|crete|cyprus|"
     r"malta|basque|navarre|balearic|mexico|mexican|tijuana|"
     r"aztec|salsa de los aztecas|pan de muerte)\b"),
    ("Nordic & Baltic",
     r"\b(swedish|sweden|norwegian|norway|danish|denmark|danemark|"
     r"finnish|finland|iceland\w*|baltic|gotland|uppsala|"
     r"gotland|scandinav\w*)\b"),
    ("Chinese", r"\b(chinese|china|peking|cantonese|shanghai|"
     r"szechuan|hunan)\b"),
    ("Japanese", r"\b(japanese|japan|edo|tokyo|kyoto|osaka)\b"),
    ("Indian & South Asian",
     r"\b(indian|india|bengal|madras|bombay|ceylon|curry|"
     r"hyderabad|maratha|moghul|mughal)\b"),
    ("African",
     r"\b(africa\w*|ethiopi\w*|ashanti|zulu|niger\w*|mali|sudan|"
     r"sennar|guinea|congo)\b"),
    ("Asian & Pacific",
     r"\b(korea\w*|korean|hwajeon|thailand|thai|siam\w*|manila|"
     r"philippin\w*|malay\w*|indonesia|japan\w*|chinese|china|"
     r"peking|cantonese|shanghai|szechuan|hunan|panama|"
     r"polynesia|hawai\w*)\b"),
    ("Africa & Latin America",
     r"\b(brazil\w*|feijoada|argentin\w*|chile\w*|peru\w*|colombia\w*|"
     r"venezuela|guatemala|cuba\w*|haiti|dominican|bolivia|ecuador|"
     r"uruguay|paraguay|africa\w*|ethiopi\w*|ashanti|zulu|niger\w*|"
     r"mali|sudan|sennar|guinea|congo)\b"),
    ("American & Caribbean",
     r"\b(united states|u\.s\.|america\w*|california|new york|boston|"
     r"chicago|philadelphia|virginia|maryland|pennsylvania|"
     r"massachusetts|texas|new orleans|new england|pompano|"
     r"barbados|jamaica|trinidad|cuba|puerto rico|havana|"
     r"antigua|alcatraz|florida|manhattan|brooklyn|washington|"
     r"new pittsburgh|colorado|denver|utah|california, |"
     r"kentucky|dakota|michigan|ohio|indiana|illinois|missouri|"
     r"wisconsin|minnesota|oregon|kansas|arkansas|tennessee|"
     r"alabama|louisiana|oklahoma|nebraska|montana|wyoming|"
     r"idaho|nevada|arizona|new mexico)\b"),
    ("Australia & New Zealand",
     r"\b(australia|australian|new zealand|new south wales|new holland)\b"),
]

COMPILED = [(name, re.compile(pat, re.I)) for name, pat in FAMILY_RULES]

# The order the families appear in the filter, most interesting first.
FAMILY_ORDER = [
    "Hungarian",
    "Russian",
    "Slavic & Eastern European",
    "Polish",
    "Jewish (Ashkenazi)",
    "German & Austrian",
    "French",
    "Italian",
    "British & Irish",
    "Ancient Rome",
    "Ancient & Near Eastern",
    "Iberian & Mediterranean",
    "Netherlandish & Low Countries",
    "Greek",
    "Turkish & Ottoman",
    "Middle Eastern & Persian",
    "Nordic & Baltic",
    "Indian & South Asian",
    "Chinese",
    "Japanese",
    "African",
    "Africa & Latin America",
    "Asian & Pacific",
    "American & Caribbean",
    "Australia & New Zealand",
    "Other",
]

FAMILY_BLURB = {
    "Hungarian": "Paprika, fat, and the slow stew. Hungarian cooking of "
                 "the period travelled with the Austro-Hungarian empire "
                 "and put down roots in every kitchen it passed through.",
    "Russian": "The whole fish, the roast, and the sour-sweet soup that "
               "reached the west as borscht.",
    "Slavic & Eastern European": "The eastern European cookery that fed "
                                 "the great migration of the 1880s and "
                                 "1890s, and that arrived in the new world "
                                 "in the trunks.",
    "Polish": "The manor-house roast joint, and the sharp vinegared "
              "vegetables that came with it.",
    "Jewish (Ashkenazi)": "Ashkenazi cooking of the early twentieth "
                           "century, written for a kitchen that was "
                           "still cooking for a holiday table every week "
                           "of the year.",
    "German & Austrian": "The reference cookery of the middle European "
                          "kitchen: the roasts, the ragoûts, the cakes.",
    "French": "French provincial cookery in the plain style the English "
              "kitchen copied, and sometimes got wrong.",
    "Italian": "Italian cooking as it was first written down in English, "
               "and often not quite right.",
    "British & Irish": "The English dinner in its great age, and the "
                        "pudding, the port, and the industrial kitchens "
                        "that made both possible.",
    "Ancient Rome": "Garum, laser, and the appetite of an empire. Apicius "
                    "is the only cookbook that survives from the Roman "
                    "world, and it is a book of the rich.",
    "Ancient & Near Eastern": "Clay tablets, temple kitchens, and the "
                               "river-valley cooking that came before "
                               "Europe had a written recipe at all.",
    "Iberian & Mediterranean": "The cooking of Spain and Portugal, and "
                                "the Mediterranean islands that fed the "
                                "trading ports.",
    "Netherlandish & Low Countries": "Butter, herring, and the "
                                      "preserving that the Low Countries "
                                      "built into an industry.",
    "Greek": "Greek island and mainland cooking as the Mediterranean "
             "trade brought it north.",
    "Turkish & Ottoman": "Ottoman and Turkish cooking as it reached "
                          "western kitchens, usually through the embassy "
                          "table and the shipping trade.",
    "Middle Eastern & Persian": "The cooking of the Ottoman east and "
                                 "Persia: the pilaf, the kebab, the "
                                 "saffron, and the sweet pastries.",
    "Nordic & Baltic": "The cold-country cookery: preserved fish, "
                        "sour dairy, rye, and a great deal of salt.",
    "Indian & South Asian": "Curry as the British kitchen met it, and "
                            "the Anglo-Indian cookbooks that taught the "
                            "household how to make it.",
    "Chinese": "Pork, tea, and the first Western cookbooks to take "
               "Chinese cooking seriously.",
    "Japanese": "The Japanese cookery that the Western world first met "
                "through the tea trade.",
    "African": "The cookery of West Africa, and of the African American "
               "kitchen that grew out of it.",
    "Africa & Latin America": "Brazil and the Caribbean: the feijoada, "
                              "the preserved fruit, and the cooking that "
                              "crossed the Atlantic in the slave trade "
                              "and came back changed.",
    "Asian & Pacific": "The cooking of East and Southeast Asia as the "
                        "western world first met it, through the tea "
                        "trade and the treaty ports.",
    "American & Caribbean": "The American regional kitchen, from "
                            "Virginia to the Caribbean, and the "
                            "preserving and canning that made it travel.",
    "Australia & New Zealand": "Colonial cooking in the southern "
                               "hemisphere, and the native ingredients "
                               "the settlers had to learn to cook.",
    "Other": "Everything else: single dishes from unusual places, and "
             "the odd historical outlier.",
}


def family_for(region):
    """Map a region string onto a cuisine family, or None."""
    if not region:
        return None
    for name, pat in COMPILED:
        if pat.search(region):
            return name
    return None
