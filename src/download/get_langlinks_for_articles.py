"""Download using Wikipedia API the languages, that the article has a version in."""
import os

from download.articles import RawArticle
from file_operations import load_pickle, save_pickle
from settings import LANGUAGE_MAP_FILE
from tools.utils import batch
from tools.wiki_api_utils import run_query, is_query_finished, handle_query_continuation

DATA_DIR = '../data2'


def get_default_langlink_query(title=""):
    return {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "langlinks",
        "formatversion": 2,
        "lllimit": 500
    }


def add_corresponding_languages_for_batch(query, language_map):
    result = run_query(query)

    if "query" not in result or 'pages' not in result['query']:
        return []

    for page in result['query']['pages']:
        title = page['title']
        page_id = page['pageid'] if 'pageid' in page else None

        languages = set()
        if 'langlinks' in page:
            for lang_link in page["langlinks"]:
                lang = lang_link["lang"]
                languages.add(lang)

        if title in language_map:
            language_map[title]["languages"] = language_map[title]["languages"].union(languages)
        else:
            language_map[title] = {"languages": languages, "wiki_id": page_id}

        print(title, languages)

    if not is_query_finished(result):
        print('continuation query required')
        query = handle_query_continuation(query, result)
        add_corresponding_languages_for_batch(query, language_map)


if __name__ == "__main__":
    article_files = sorted(filter(lambda x: x.startswith('articles.'), os.listdir(DATA_DIR)))

    language_map = load_pickle(LANGUAGE_MAP_FILE)

    for file in article_files:
        print(file)
        article_batch = load_pickle(file, is_list=True)

        for query_batch in batch(article_batch, 50):
            titles = [article.title for article in query_batch if article.title not in language_map]
            if len(titles) > 0:
                query = get_default_langlink_query()
                query['titles'] = "|".join(titles)
                add_corresponding_languages_for_batch(query, language_map)

        print('Saving language map')
        save_pickle(language_map, LANGUAGE_MAP_FILE)
