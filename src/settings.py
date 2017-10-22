from __future__ import unicode_literals
import logging

API_URL = "https://en.wikipedia.org/w/api.php"

ENWIKI_DIR = 'D:\Studia\Magisterka\enwiki'

DATA_DIR = "../data2"

LOG_DIR = "../log"

ARTICLE_LOG_FILE = LOG_DIR + "/articles.log"

GRAPH_CREATOR_LOG_FILE = LOG_DIR + "/graph_creator.log"

PARSE_ERROR_LOG_FILE = LOG_DIR + "/parse_error.log"

CATEGORIES_FILE = DATA_DIR + '/categories.csv'

CATEGORIES_RELEVANT_FILE = DATA_DIR + '/categories_relevant.csv'

ARTICLES_FILE = DATA_DIR + '/articles.pickle'

RELATIONSHIP_MAP_FILE = DATA_DIR + '/relationships.pickle'
DUPLICATE_RELATIONSHIP_MAP_FILE = DATA_DIR + '/relationships_manual.pickle'

GRAPH_IN_PROGRESS_FILE = DATA_DIR + '/in_progress_graph.pickle'

GRAPH_GML_FILE = DATA_DIR + '/graph.gml'

GRAPH_SNAP_FILE = DATA_DIR + '/graph_snap.graph'

LANGUAGE_MAP_FILE = DATA_DIR + '/language_map.graph'


def get_graph_logger():
    logger = logging.getLogger('graph_logger')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(GRAPH_CREATOR_LOG_FILE, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


def get_parse_error_logger():
    logger = logging.getLogger('parse_logger')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(PARSE_ERROR_LOG_FILE, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


def logging_config():
    logging.basicConfig(level=logging.ERROR)


graph_logger = get_graph_logger()
