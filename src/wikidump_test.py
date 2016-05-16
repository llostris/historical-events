from urllib import urlencode
from urllib2 import urlopen

import wikidump as wd
# import wikitools as wt
# import mwclient as mwc
import mwparserfromhell as hell
import json

from safestring import safe_str
from settings import API_URL


def date_matcher(x):
    contains_date = '{{start date' in x.lower() or '{{end date' in x.lower()
    return contains_date and len(x) < 50

def test_hell_api():
    title = "World War II"
    data = {"action": "query", "prop": "revisions", "rvlimit": 1,
            "rvprop": "content", "format": "json", "titles": title}
    raw = urlopen(API_URL, urlencode(data).encode()).read()
    res = json.loads(raw)
    # print res
    text = res["query"]["pages"].values()[0]["revisions"][0]["*"]
    # print text
    page_tree = hell.parse(text)
    print(safe_str(page_tree))

    print(page_tree.get_tree())

    print(page_tree.filter_wikilinks()) # for extracting references to other articles

    print('dates:')
    filtered = page_tree.filter(forcetype=hell.nodes.Node,
                           matches=date_matcher)
    print(filtered)

    print(len(filtered))
    # now extract date
    # print(page_tree.filter(forcetype='date'))


    # for node in page_tree:
    #     print node
    return page_tree

if __name__ == "__main__":
    print "ala"
    test_hell_api()
    pass


