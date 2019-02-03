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
ART_FORBIDDEN_CATEGORIES = {'20 july plot', 'countries', }

# Keywords which indicate that category is related to our problem
ART_CATEGORY_WHITELIST = {
    'painter', 'painting', 'play', 'movie', 'novel', 'poem', 'poetry', 'poet', 'book', 'painter',
    'sculptor', 'sculptures', 'musicians', 'architecture', 'operas', 'genres', 'concertos',
    'piano', 'photography', 'photographers', 'woodcarvers', 'literature', 'writers', 'on film', 'literature',
    # 'theatre', 'songs',
}

# Keywords that indicate that the category or article is not relevant to our search
ART_CATEGORY_BLACKLIST = {
    'venues', 'clubs', 'principals of', 'record labels', 'awards', 'schools of', 'paralympic', 'olympic',
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
    'emigrants', 'series endings', 'people excommunicated', 'think tanks', 'merchants', 'nobility', 'advisors',
    'research', 'campaigns', 'reservoirs', 'lakes', 'rivers', 'mountain passes', 'mountains', 'valleys', 'waterfalls',
    'hills', 'basketball', 'baseball', 'players', 'survey', 'parkway', 'landmarks', 'maps of', 'stations', 'places',
    'national forest', 'forests', 'chapter lists', 'episode list', 'presenters', 'settlements', 'descent', 'educators',
    'environmentalists', 'seas', 'emperors', 'bay of', 'gulf', 'tributaries', 'basin', 'landforms', 'geography',
    'politics of', 'deputies', 'tourist', 'towns', 'villages', 'regents', 'monarchy', 'government', 'historians',
    'ministers', 'sport', 'hockey', 'crimes', 'elections', 'psychological', 'assassins of', 'staff', 'wikipedia',
    'commandants', 'in the german resistance', 'philosophers', 'manufacturers', 'companies', 'supermarkets', 'airlines',
    'descent', 'knights', 'cemeteries', 'shops', 'shopping malls', 'concentration', 'camps', 'pipelines', 'festivals',
    'biathlets', 'skiers', 'ski jumpers', 'jumpers', 'competitions', 'bobsledders', 'recipients of', 'ambassadors',
    'people murdered', 'resistance members', 'expatriates', 'drugs', 'institute of', 'rapists', 'universities',
    'colleges', 'people from', 'prisons', 'residences', 'parties', 'common law', 'organisations', 'media', 'mobsters',
    'librarians', 'coats of arms', 'retail buildings', 'music venues', 'geology', 'rabbis', 'lighthouses',
    'fairy tales', 'victims', 'survivors', 'politicians', 'dragons', 'book covers', 'creatures', 'stamps', 'flags',
    'hazzans', 'secretaries', 'burials in', 'protected areas', 'national parks', 'parks', 'heroes', 'people of',
    'geography', 'archeological', 'settlements', 'colonies', 'tribes', 'people from', 'biota', 'administrative',
    'canals', 'sciences', 'people by university', 'university', 'college', 'commercial buildings', 'pornographic',
    'entertainment districts', 'talent agents', 'ranches', 'trails', 'districts', 'museums', 'natural monuments',
    'railway', 'accidents', 'karateka', 'pornography', 'devotees', 'televangelism', 'railroad', 'dolmens', 'massacres',
    'political posters', 'organizations', 'art galleries', 'bodies of water', 'springs', 'education', 'gaza strip',
    'music schools', 'administration', 'officials', 'christians', 'muslims', 'crusade', 'kingdom of jerusalem',
    'conflict', 'territories', 'governorate', 'oganization', 'prostitution', 'holidays', 'dominicans', 'sex positions',
    'criminals', 'executions', 'people executed', 'prisoners', 'kidnapping', 'murder in', 'deaths by', 'corruption in',
    'escapes from', 'people convicted', 'prisoners sentenced to', 'cardinals by', 'archeological sites', 'homelessness',
    'unsolved murders', 'activism', 'terrorist incidents in', 'albums', 'score', 'astrology', 'diseases', 'resolutions',
    'birth defects', 'disasters', 'conventions', 'treaties', 'declaration', 'programming', 'united nations',
    'supremacist', 'referendums', 'exhibitions', 'operating systems', 'computer science', 'video game', 'anime',
    'songs', 'sailors', 'critics', 'houses in', 'election', 'murderers', 'martial artists', 'centuries in',
    'television series', 'album covers', 'templates', 'sex workers', 'audio samples', 'gangs in', 'violence in',
    'buildings and structures', 'crime in', 'terrorism', 'suicides in', 'attacks in', 'riots in', 'speeches by',
    'anarchism', 'articles', 'sex industry', 'erotic films', 'pimps', 'courtesans', 'sexologists', 'antisemitism in',
    'house of representatives', 'ku klux klan', 'neo-nazis', 'inmates', 'holocaust deniers', 'ghetto', 'century jews',
    'biblical rulers', 'pharaophs of', 'physicians', 'wetlands', 'palenontology', 'energy', 'infrastructure',
    'natural history', 'departments', 'enforcement', 'jails', 'years in', 'penal system', 'shooting', 'hospitals',
    'film editors', 'runners', 'aftermath of', 'brand', 'linux', 'scientists', 'engineer', 'games', 'linguist',
    'orders', 'environmentalism', 'flora', 'science', 'fauna', 'history of', 'deaths from', 'footwear', 'anthropology',
    'bones', 'wrestlers', 'boots', 'parades in', 'carnival', 'parade', 'orienteering', 'mountain hut', 'bowling',
    'sprinters', 'diet', 'sport', 'trampolinist', 'entrepreneurs', 'anthroposophist', 'waldorf schools', 'fairs',
    'anthroposophy', 'blogger', 'writer navigational boxes', 'wikipedia', 'academic', 'newspaper', 'voice of',
    'printer', 'periodical', 'magazine', 'printing', 'publishing', 'gods', 'goddesses', 'deities', 'natural history',
    'middle-earth', 'locations', 'redirects', 'characters', 'incident', 'torture', 'prisoner', 'weapons', 'activities',
    'relations', 'settlement', 'court', 'diaspora', 'communities', 'private schools', 'cuisine', 'ballromm houses',
    'ball culture', 'location', 'activist', 'civil servants', 'business', 'assassinated', 'deaths', 'people killed',
    'agency', 'school siege', 'hostage crisis', 'operations of', 'terrorist incidents', 'militant group',
    'by occupation', 'immigrants to', 'ethnic or national', 'people by', 'pacifist', 'feminist', 'dissident',
    'dynasties', 'yeshivas', 'miners', 'industries', 'record charts', 'charts', 'martial artists', 'practitioners',
    'martial arts', 'judoka', 'boxer', 'boxing', 'fencer', 'savateurs', 'wushu in', 'wrestling', 'fashion', 'states',
    'infobox', 'time zones', 'offsets', 'descartes', 'maths', 'curves', 'coordinate', 'castes', 'colony', 'war',
    'colonial', 'royalty', 'hoaxes', 'controversy', 'racism', 'affirmative action', 'blacksmith', 'outreach',
    'region', 'mining', 'coal', '3d graphic artifacts', 'interpolation', 'morphology', 'color', 'ray tracing',
    'algorithm', 'chemistry', 'chemist', 'mathematics', 'physics', 'biology', 'computational', 'artificial life',
    'computation', 'chaos theory', 'informatics', 'analysis', 'computing', 'cult of', 'mythology', 'muses',
    'mythological', 'sexism', 'discrimination', 'vandalism', 'judicial', 'ethics', 'issues', 'stereotype',
    'personality', 'cthulhu', 'constituencies', 'lists of members', 'executioner', 'marriage', 'cities',
    'data structures', 'zionism', 'zionist', 'television presentation', 'commercials', 'advertisements', 'commercial',
    'logos', 'technology', 'fandom', 'surveillance', 'terminology', 'podcast', 'on demand', 'radio', 'databases',
    'gateways', 'streaming', 'networks', 'webcams', 'channels', 'youtube', 'computers', 'ipad', 'phones',
    'media players', 'media', 'player', 'devices', 'cable', 'interface', 'broadcasting', 'spectrum', 'frequency',
    'recommendations', 'telecommunication', 'internet', 'postal', 'communications', 'philately', 'satellites',
    'judaism', 'resistance', 'fighters', 'disciples', 'revolt', 'kahanists', 'insurgency', 'nationalism', 'rebellions',
    'bundism', 'wind farms', 'mills', 'wind power', 'electric', 'thoroughbred', 'racehorse', 'arc winner', 'winners',
    'deaths', 'births', 'family', 'authorities', 'personnel', 'officer', 'dogs', 'saints', 'confederacy', 'tribe',
    'reserves', 'exchange', 'stock', 'politics', 'animals', 'streets in', 'bazaars', 'food in', 'piazzas',
    'public squares', 'plazas', 'islamism', 'politics', 'graffiti', 'family', 'nazis', 'nationalism', 'denomination',
    'rabbi', 'converts', 'judaism', 'cars of', 'by country', 'housing in', 'hydroxides', 'women rulers', 'carnivora',
    'animals', 'events', 'detectives', 'natural gas', 'gas', 'gender in', 'floods', 'ethnic groups', 'priests',
    'world heritage sites', 'manufacturing', 'technology',  'events', 'tsunamis', 'citizens', 'species', 'billionaires',
    'politician', 'andrologists', 'sites', 'navigational', 'hurdles', 'swamps', 'canoeists', 'decades', 'fossil',
    'fuel', 'millennia', 'wealth', 'monasteries', 'art collectors', 'missiles', 'products',
    # 'sentiment',
    

    #'castles in',

    # These are relevant but we want to reduce the size of the graph
    'skyscrapers',
    'albums', 'songs',
}

ART_TITLE_BLACKLIST = {
    'episode list', 'episodes', 'list of', 'museum', 'birth defects', 'videography', 'discography', 'filmography',
    'united nations', 'timeline of', 'aftermath of', 'supremacist', 'album', '(characters)', 'episode)', '(episode)',
    'same-sex marriage in', 'missile', '(song)',
}

ART_TITLE_WHITELIST = {}
