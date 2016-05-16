# Various tags used in Wikimedia API calls and results
import re

TAG_QUERY = "query"
TAG_PAGES = "pages"
TAG_TITLE = "title"
CATEGORYMEMBERS = "categorymembers"

# Map of wikimedia namespaces to their IDs (only relevant ones)
NAMESPACES = {
    "category" : 14,
    "article" : 0,
    "portal" : 100
}

# Categories that might have been added while scraping Wikipedia that are not relevant to our search
# Requires adding "Category:" prefix
FORBIDDEN_CATEGORIES = {
    "Philosophy", "Cities and towns during the Syrian Civil War", "School buildings completed in 1870",
    "United States Supreme Court cases", "List of political parties in Namibia", "Units of measurement by country"
}

# Keywords which indicate that category is history-related
CATEGORY_KEYWORDS = { 'war', 'battles', 'treaties', 'history', 'century', 'births', 'discoveries', 'deaths',
                      'timelines', 'explosion', 'bomb', 'attack' }

# Keywords that indicate that the category or article is not relevant to our search
FORBIDDEN_CATEGORY_KEYWORDS = { 'mountains of', 'biota of', 'fauna of', 'racehorse births', 'novels', 'actresses',
                                'actors', 'sculptors', 'painters', 'lawyers', 'physicians', 'architects', 'writers',
                                'artists', 'businesspeople', 'historians', 'medical doctors', 'mathematicians',
                                'racehorse', 'monks', 'warriors', 'dancers', 'singers', 'musicians', 'people',
                                'criminals', 'personnel', 'museum', 'deaths', 'poets', 'corespondents',
                                'books about', 'awards', 'region', 'school buildings completed', 'film', 'movie',
                                'software', 'video game', 'urban districts of', 'boroughs', 'units of measurement',
                                'supreme court of' }
# 'politicians',

FORBIDDEN_TITLE_KEYWORDS = { 'museum', 'list', 'region', 'film', 'movie', '10,000 metres', 'units of measurement',
                             'utc+' }

TITLE_KEYWORDS = { 'war', 'battle', 'treaties', 'treaty', 'history', 'century', 'births', 'discoveery', 'explosion',
                   'bomb', 'attack', }

YEAR_IN_REGEXP = re.compile(r"\d{4} in ")

def is_category_relevant(category_name):
    for forbidden_word in FORBIDDEN_CATEGORY_KEYWORDS:
        if forbidden_word in category_name.lower():
            return False
    return True

def is_title_relevant(title):
    for forbidden_word in FORBIDDEN_TITLE_KEYWORDS:
        if forbidden_word in title.lower():
            return False

    if YEAR_IN_REGEXP.search(title) is not None:
        return False

    return True


CATEGORY_REGEXP = re.compile(r"\[\[Category:[^\]]*\]\]")