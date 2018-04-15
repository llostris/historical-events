# coding=utf-8
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import ReadTimeoutError

import settings
from settings import API_URL

settings.logging_config()


def get_session(retries=3):
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


session = get_session()


def run_query(query):
    """
    Calls Wikimedia API url for given query.
    :param query: Map of query parameters, that will be used to encode the valid API url.
    :return: A map containing the result of the query.
    """
    response = session.get(API_URL, params=query)
    try:
        if response.status_code == 200:
            result = response.json(encoding='utf-8')
            return result
    except ValueError:
        logging.error("Couldn't parse JSON: " + response.content)
        return ""
    except ReadTimeoutError as e:
        # Try again
        print(query)
        raise e

    return {}


def is_query_finished(result):
    """
    Checks if API's response needs query continuation.
    :param result: Map containt the result of the Wikimedia API query
    :return: Boolean
    """
    if "continue" not in result:
        return True     # query is finished
    else:
        return False    # run the query again


def handle_query_continuation(query, result):
    """Handle problem of query continuation for multi-paged result sets, so the following pages are also downloaded"""
    continue_node = result['continue']
    for node in continue_node:
        query[node] = continue_node[node]

    return query


