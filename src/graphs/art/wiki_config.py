"""Art Influence Graph - configuration file"""
from settings import DATA_DIR

# Files and directories
ART_DATA_DIR = DATA_DIR + '/art/'
ART_CATEGORIES_FILE = ART_DATA_DIR + '/categories.csv'
ART_CATEGORIES_RELEVANT_FILE = ART_DATA_DIR + '/categories_relevant.csv'


# Place we start off when creating our graph
FIRST_CATEGORY = "Category:Arts"

# Categories that might have been added while scraping Wikipedia that are not relevant to our search
# Requires adding "Category:" prefix
ART_FORBIDDEN_CATEGORIES = {'20 july plot'}

# Keywords which indicate that category is related to our problem
ART_CATEGORY_WHITELIST = {
    'painter', 'painting', 'music', 'play', 'movie', 'film', 'novel', 'poem', 'poetry', 'poet', 'book', 'painter',
    'sculptor', 'sculpture', 'musicians', 'songs', 'architecture', 'operas',
    # 'theatre',
}

# Keywords that indicate that the category or article is not relevant to our search
ART_CATEGORY_BLACKLIST = {
    'venues', 'clubs', 'principals of', 'record labels', 'awards', 'schools of', 'paralympics', 'olympics',
    'british empire games', 'art museums and galleries', 'theatres in', 'theatre companies', 'drama schools in',
    'employees of', 'episodes', 'characters', 'seasons', 'fictional', 'images', 'media cover', 'military district',
    'commanders', 'fleet', 'military region', 'political commissars', 'aircraft', 'generals', 'communist party',
    'establishments', 'medalists', 'subdivisions', 'battles', 'artillery', 'grenade', 'governors', 'casualties',
    'convoys', 'ships', 'warfare', 'battlecruisers', 'boats', 'submarines', 'military of', 'brigades of', 'ship names',
    'bombers', 'bombs', 'mortars', 'museums in', 'archives in', 'events in', 'languages of', 'libraries in', 'sport in',
    'religion in', 'language', 'dialects of', 'grammar', 'economy of', 'parliament of', 'schools in', 'markets in',
    'restaurants', 'office buildings', 'cafés', 'faculty', 'translators', 'lawyers', 'mysticism', 'coaches', 'scholars',
    'columnists', 'journalists', 'correspondents', 'sports', 'diplomats', 'missionaries', 'sport in', 'football',
    'neighbourhoods', 'hotels in', 'districts of', 'sieges of', 'mayors of', 'kings of', 'queens of', 'military',
    'emigrants', 'series endings', 'people excommunicated', 'think thanks', 'merchants', 'nobility', 'advisors',
    'research', 'campaigns', 'reservoirs', 'lakes', 'rivers', 'mountain passes', 'mountains', 'valleys', 'waterfalls',
    'hills', 'basketball', 'baseball', 'players', 'survey', 'parkway', 'landmarks', 'maps of', 'stations', 'places',
    'national forest', 'forests', 'chapter lists', 'episode list', 'presenters', 'settlements', 'descent', 'educators',
    'environmentalists', 'seas', 'emperors', 'bay of', 'gulf', 'tributaries', 'basin', 'landforms', 'geography',
    'politics of', 'deputies', 'tourist', 'towns', 'villages', 'regents', 'monarchy', 'government', 'historians',
    'ministers', 'sport', 'hockey', 'crimes', 'elections', 'psychological', 'assassins of', 'staff', 'wikipedia',
    'commandants', 'in the german resistance',
    'knights of',
    #'castles in',
}

ART_TITLE_BLACKLIST = {'episode list', 'episodes',}

ART_TITLE_WHITELIST = {}
