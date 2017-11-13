"""Configuration file: keywords used to determine whether or not a category or article is relevant to our problem.
Terms to avoid. 
Terms to include. """

# Various tags used in Wikimedia API calls and results
import re

TAG_QUERY = "query"
TAG_PAGES = "pages"
TAG_TITLE = "title"
TAG_LANGLINKS = "langlinks"
TAG_LANG = "lang"
CATEGORYMEMBERS = "categorymembers"

# Map of wikimedia namespaces to their IDs (only relevant ones)
NAMESPACES = {
    "category": 14,
    "article": 0,
    "portal": 100
}

# Regular expressions

YEAR_IN_REGEXP = re.compile(r"\d{4} in ")

CATEGORY_REGEXP = re.compile(r"\[\[Category:[^\]]*\]\]")

NUMBER_ONLY_REGEXP = re.compile(r"^\d+$")   # avoid articles of particular years ex. 1945, 1956
