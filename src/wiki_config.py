"""Configuration file: keywords used to determine whether or not a category or article is relevant to our problem.
Terms to avoid. 
Terms to include. """

# Various tags used in Wikimedia API calls and results
import re

TAG_QUERY = "query"
TAG_PAGES = "pages"
TAG_TITLE = "title"
CATEGORYMEMBERS = "categorymembers"

# Map of wikimedia namespaces to their IDs (only relevant ones)
NAMESPACES = {
    "category": 14,
    "article": 0,
    "portal": 100
}

# Categories that might have been added while scraping Wikipedia that are not relevant to our search
# Requires adding "Category:" prefix
FORBIDDEN_CATEGORIES = {
    "Philosophy", "Cities and towns during the Syrian Civil War", "School buildings completed in 1870",
    "United States Supreme Court cases", "List of political parties in Namibia", "Units of measurement by country"
}

# Keywords which indicate that category is history-related
CATEGORY_KEYWORDS = {'war', 'battle', 'treaties', 'history', 'century', 'births', 'discoveries', 'deaths',
                     'timelines', 'explosion', 'bomb', 'attack', 'conflict', 'discovery'
                     }

# Keywords that indicate that the category or article is not relevant to our search
FORBIDDEN_CATEGORY_KEYWORDS = {'mountains of', 'biota of', 'fauna of', 'racehorse births', 'museum', 'books about',
                               'region', 'school buildings completed', 'urban districts of', 'boroughs',
                               'units of measurement', 'supreme court of', 'racehorse', 'cannon-class destroyer',
                               'royal norwegian navy ship names', 'ad hoc units and formations', 'submarine classes',
                               'bundism', 'frigates', 'patrol vessels', 'missiles', 'bomber aircraft',
                               'fieseler aircraft', 'modular aircraft', 'military aircraft projects',
                               'rocket artillery', 'rocket launchers', 'artillery', 'anti-tank guns', 'aircraft',
                               'defensive lines', 'warfare by type', 'media issues', 'laws of war', 'cyberwarfare',
                               'propaganda techniques', 'steamships', 'passenger ships', 'military communications',
                               'military terminology', 'humanitarian aid', 'agriculture', 'military units',
                               'disbanded armies', 'field armies', 'equipment', 'in sociology', 'battleships',
                               'polish people of the spanish civil war', 'monitors', 'machine guns', 'military awards',
                               'navy ship names', 'minesweepers', 'minehunters', 'survey ships', 'tank', 'troop ships',
                               'ships of', 'sailing vessels', 'vessels', 'military intelligence', 'torpedo boats',
                               'ships', 'tanks', 'military vehicles', 'armoured cars', 'award', 'software',
                               'video game', 'movie', 'film', 'novels', 'fictional', 'gunboats', 'star wars',
                               'war destroyer', 'cruisers', 'guns of', 'world war ii bombers', 'cities', 'comics',
                               'rifles', 'weapons', 'songs', 'half-tracks of', 'it risk management', 'radio stations',
                               'archaeological sites', 'grenades', 'commotes', 'television episodes', 'revolver',
                               'populated places', 'ethnic groups', 'Vermont in the American Civil War'.lower(),
                               'airfields', 'actresses', 'actors', 'natural history', 'lunar eclipse', 'convoys',
                               'biographies', 'memorials in', 'steamboats', 'hurricane', 'shipwrecks', 'tornado',
                               'tornadoes', 'clothing', 'uniforms', 'cathedrals in', 'buildings', 'television series',
                               'roads in', 'rites of passage', 'manga', 'comic', 'games', 'tv series', 'television',
                               'essays', 'books', 'symphonies', 'restaurants', 'cuisine', 'footballers',
                               'villages in', 'water sports', 'sports', 'journals', 'road incident', 'railway',
                               'accidental deaths', 'lighthouses', 'popular culture', 'churches', 'cathedral',
                               'destroyers', 'network protocols', 'networking', 'mythology', 'football', 'basketball',
                               'rugby', 'skiing', 'soccer', 'vehicles', 'firearm', 'helicopters', 'names of',
                               'names for', 'rivers', 'dance', 'schools in', 'parks', 'currencies', 'capitals',
                               'plays', 'awards', 'lawyers', 'businesspeople', 'historians', 'medical doctors',
                               'dancers', 'singers', 'musicians', 'disestablishments', 'infrastructure', 'texts',


                               # 'sites', # might have some good stuff?
                               # 'deaths', 'poets', 'awards',
                               # people:
                               # 'sculptors', 'painters', 'lawyers', 'physicians', 'architects',
                               # 'writers', 'artists',
                               # 'mathematicians', 'monks', 'warriors',
                               # 'criminals', 'corespondents', 'people', 'personnel',
                               }
# 'politicians',

VALID_CATEGORY_KEYWORDS = {'conflicts', 'battles', 'wars', 'treaties', }

FORBIDDEN_TITLE_KEYWORDS = {'museum', 'list', 'region', '10,000 metres', 'units of measurement', 'utc+',
                            'body count project', 'in sociology', 'topedo boat', 'SMS', 'timeline', 'cheirisophus',
                            'language', 'history of', 'harpalus', 'film', 'movie', 'six plus two group on afghanistan',
                            'cultural representations of', 'cultural depictions', 'cultural backwardness',
                            'battle tactics', 'document exploitation', 'women on the web', 'war cemetery',
                            'historic district', 'yacht', 'tornado', 'document exploitation', 'headwear',
                            'rural district', 'paris in the', 'effects of', 'casualties', 'provincial park',

                            # 'council election',
                            # 'marcus licinius crassus (quaestor)',   # TODO: why?
                            # 'pedro de herrera',  # TODO: why? (content)
                            }

TITLE_KEYWORDS = {'war', 'battle', 'treaties', 'treaty', 'history', 'century', 'birth', 'death', 'discovery',
                  'explosion', 'operation', 'bomb', 'attack', }


# Regular expressions

YEAR_IN_REGEXP = re.compile(r"\d{4} in ")

CATEGORY_REGEXP = re.compile(r"\[\[Category:[^\]]*\]\]")

NUMBER_ONLY_REGEXP = re.compile(r"^\d+$")   # avoid articles of particular years ex. 1945, 1956


# Methods

def is_category_relevant(category_name):
    for white_word in CATEGORY_KEYWORDS:
        if white_word in category_name.lower():
            return True

    for forbidden_word in FORBIDDEN_CATEGORY_KEYWORDS:
        if forbidden_word in category_name.lower():
            return False
    return True


def is_title_relevant(title):
    for white_word in TITLE_KEYWORDS:
        if white_word in title.lower():
            return True

    for forbidden_word in FORBIDDEN_TITLE_KEYWORDS:
        if forbidden_word in title.lower():
            return False

    if YEAR_IN_REGEXP.search(title) is not None or NUMBER_ONLY_REGEXP.search(title) is not None:
        return False

    return True


def is_article_relevant(title, content):
    categories = CATEGORY_REGEXP.findall(content)
    for category in categories:
        if not is_category_relevant(category):
            return False

    return is_title_relevant(title)
