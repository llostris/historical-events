"""Computer science Influence Graph - configuration file"""
from settings import DATA_DIR

# Files and directories
COMP_SCI_DATA_DIR = DATA_DIR + '/comp_sci'
COMP_SCI_CATEGORIES_FILE = COMP_SCI_DATA_DIR + '/categories.csv'
COMP_SCI_CATEGORIES_RELEVANT_FILE = COMP_SCI_DATA_DIR + '/categories_relevant.csv'

FIRST_CATEGORY = "Category:Computer Science"

COMP_SCI_FORBIDDEN_CATEGORIES = {}

# Keywords which indicate that category is related to our problem
COMP_SCI_CATEGORY_WHITELIST = {}

# Keywords that indicate that the category or article is not relevant to our search
COMP_SCI_CATEGORY_BLACKLIST = {
}

COMP_SCI_TITLE_BLACKLIST = {}

COMP_SCI_TITLE_WHITELIST = {}
