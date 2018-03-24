import logging
import pickle

from requests.exceptions import ChunkedEncodingError


# LOGGER = logging.getLogger()
logging.debug('test')
logging.info('test2')

CATEGORIES_BUGS = []


class RawArticle:

    def __init__(self, pageid, title, content):
        self.pageid = pageid
        self.title = title
        self.content = content

    def __repr__(self):
        return "(%s, %s, %s)" % (self.pageid, self.title, self.content[:100])

