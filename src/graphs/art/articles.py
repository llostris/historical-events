from graphs.art.categories import ArtCategoryMatcher
from graphs.art.wiki_config import ART_DATA_DIR
from tools.article_scraper import ArticleScraper

if __name__ == "__main__":
    article_scraper = ArticleScraper(data_dir=ART_DATA_DIR, category_matcher=ArtCategoryMatcher())
    article_scraper.download_articles(start=0)
