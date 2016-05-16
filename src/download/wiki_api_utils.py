import json
import logging
from urllib import urlencode
from urllib2 import urlopen

import settings
from settings import API_URL
from wiki_config import NAMESPACES

settings.loggingConfig()

def run_query(query) :
    """
    Calls Wikimedia API url for given query.
    :param query: Map of query parameters, that will be used to encode the valid API url.
    :return: A map containing the result of the query.
    """
    raw = urlopen(API_URL, urlencode(query).encode()).read()
    try:
        result = json.loads(raw)
    except ValueError as e:
        logging.error("Couldn't parse JSON: " + raw)
        return ""

    return result


def is_query_finished(result) :
    """
    Checks if API's response needs query continuation.
    :param result: Map containt the result of the Wikimedia API query
    :return: Boolean
    """
    if "batchcomplete" in result["query"] and result["query"]["batchcomplete"] :
        # query is finished
        return True
    else :
        # run the query again
        return False


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
