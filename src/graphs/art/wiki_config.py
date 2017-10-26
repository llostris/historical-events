"""Art Influence Graph - configuration file"""
from settings import DATA_DIR

# Files and directories
ART_DATA_DIR = DATA_DIR + '/art'
ART_CATEGORIES_FILE = ART_DATA_DIR + '/categories.csv'
ART_CATEGORIES_RELEVANT_FILE = ART_DATA_DIR + '/categories_relevant.csv'


# Place we start off when creating our graph
FIRST_CATEGORY = "Category:Arts"

# Categories that might have been added while scraping Wikipedia that are not relevant to our search
# Requires adding "Category:" prefix
ART_FORBIDDEN_CATEGORIES = {}

# Keywords which indicate that category is related to our problem
ART_CATEGORY_WHITELIST = {}

# Keywords that indicate that the category or article is not relevant to our search
ART_CATEGORY_BLACKLIST = {}

ART_TITLE_BLACKLIST = {}

ART_TITLE_WHITELIST = {}
