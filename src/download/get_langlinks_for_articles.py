"""Download using Wikipedia API the languages, that the article has a version in."""
import os

from download.articles import RawArticle
from download.wiki_api_utils import run_query
from file_operations import load_pickle, save_pickle
from graph.model.vertex_extractor import ARTICLE_FILE_NAME_PREFIX, load_article_from_pickle
from settings import DATA_DIR, LANGUAGE_MAP_FILE


def get_default_langlink_query(title=""):
    return {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "langlinks",
        "formatversion": 2
    }


def get_corresponding_languages(query):
    result = run_query(query)

    if "query" not in result or 'pages' not in result['query']:
        return []
    languages = set()
    for page in result['query']['pages']:
        if 'langlinks' in page:
            for lang_link in page["langlinks"]:
                lang = lang_link["lang"]
                languages.add(lang)
    print(languages)
    return languages


def add_corresponding_languages_for_batch(query, language_map):
    result = run_query(query)

    if "query" not in result or 'pages' not in result['query']:
        return []

    for page in result['query']['pages']:
        languages = set()
        title = page['title']
        page_id = page['pageid'] if 'pageid' in page else None
        if 'langlinks' in page:
            for lang_link in page["langlinks"]:
                lang = lang_link["lang"]
                languages.add(lang)
        language_map[title] = {"languages": languages, "wiki_id": page_id}

        print(title, languages)


def batch(iterable, batch_size=1):
    iterable_length = len(iterable)
    for index in range(0, iterable_length, batch_size):
        yield iterable[index:min(index + batch_size, iterable_length)]


if __name__ == "__main__":
    article_files = sorted(filter(lambda x: x.startswith(ARTICLE_FILE_NAME_PREFIX), os.listdir(DATA_DIR)))
    query = get_default_langlink_query()

    language_map = load_pickle(LANGUAGE_MAP_FILE)

    for file in article_files:
        print(file)
        article_batch = load_article_from_pickle(file)

        for query_batch in batch(article_batch, 50):
            titles = [article.title for article in query_batch if article.title not in language_map]
            if len(titles) > 0:
                query['titles'] = "|".join(titles)
                add_corresponding_languages_for_batch(query, language_map)

        save_pickle(language_map, LANGUAGE_MAP_FILE)

