import logging

API_URL = "https://en.wikipedia.org/w/api.php"

DATA_DIR = "../data"

# Logging

LOG_DIR = "../log"
WIKI_LOG_FILE = LOG_DIR + "/wiki.log"
GRAPH_CREATOR_LOG_FILE = LOG_DIR + "/graph_creator.log"
PARSE_ERROR_LOG_FILE = LOG_DIR + "/parse_error.log"

# Filenames

CATEGORIES_FILENAME = 'categories.csv'
CATEGORIES_UNIQUE_FILENAME = 'categories_unique.csv'
CATEGORIES_RELEVANT_FILENAME = 'categories_relevant.csv'
ARTICLES_FILENAME_TEMPLATE = 'articles_{}.pickle'
GRAPH_IN_PROGRESS_FILENAME = 'in_progress_graph.pickle'
RELATIONSHIP_MAP_FILENAME = 'relationships.pickle'
LANGUAGE_MAP_FILENAME = 'language_map.pickle'
GRAPH_GML_FILENAME = 'graph.gml'
GRAPH_LANGUAGE_GML_FILENAME = 'graph_lang_{}.gml'

CATEGORIES_FILE = DATA_DIR + '/' + CATEGORIES_FILENAME

RELATIONSHIP_MAP_FILE = DATA_DIR + '/relationships.pickle'
DUPLICATE_RELATIONSHIP_MAP_FILE = DATA_DIR + '/relationships_manual.pickle'

GRAPH_IN_PROGRESS_FILE = DATA_DIR + '/in_progress_graph.pickle'

GRAPH_GML_FILE = DATA_DIR + '/graph.gml'

GRAPH_SNAP_FILE = DATA_DIR + '/graph_snap.graph'

LANGUAGE_MAP_FILE = DATA_DIR + '/language_map.graph'


def setup_base_logger(name, filename, loglevel):
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(filename, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(loglevel)
    return logger


def get_graph_logger():
    return setup_base_logger('graph_logger', GRAPH_CREATOR_LOG_FILE, loglevel=logging.INFO)


def get_parse_error_logger():
    return setup_base_logger('parse_logger', PARSE_ERROR_LOG_FILE, loglevel=logging.INFO)


def get_wiki_logger():
    return setup_base_logger('wiki_logger', WIKI_LOG_FILE, loglevel=logging.INFO)


def logging_config():
    logging.basicConfig(level=logging.WARNING)


graph_logger = get_graph_logger()
