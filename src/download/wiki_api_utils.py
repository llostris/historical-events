# coding=utf-8
import json
import logging
# from urllib import urlencode
import requests

import settings
from settings import API_URL
from wiki_config import NAMESPACES

settings.logging_config()

def run_query(query) :
    """
    Calls Wikimedia API url for given query.
    :param query: Map of query parameters, that will be used to encode the valid API url.
    :return: A map containing the result of the query.
    """
    response = requests.get(API_URL, query)
    try:
        result = response.json(encoding='utf-8')
    except ValueError as e:
        logging.error("Couldn't parse JSON: " + response.content)
        return ""

    return result


def is_query_finished(result) :
    """
    Checks if API's response needs query continuation.
    :param result: Map containt the result of the Wikimedia API query
    :return: Boolean
    """

    if "continue" not in result :
        # query is finished
        return True
    else :
        # run the query again
        return False


def handle_query_continuation(query, result):
    continue_node = result['continue']
    for node in continue_node:
        query[node] = continue_node[node]

    return query


def get_default_article_query(title):
    query = {
        "action" : "query",
        "generator" : "categorymembers",
        "gcmlimit" : "max",
        "format" : "json",
        "gcmtitle" : title,
        "prop" : "revisions",
        "rvprop" : "content",
        # "rvlimit" : 1,
        "gcmnamespace" : NAMESPACES["article"], #cmnamespace
        "formatversion" : 2
    }
    return query


if __name__ == "__main__" :
    # Example query
    query = {
        "action" : "query",
        "generator" : "categorymembers",
        "cmlimit" : "max",
        "format" : "json",
        "cmnamespace" : NAMESPACES["article"],
        "formatversion" : 2
    }