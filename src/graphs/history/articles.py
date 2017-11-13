from graphs.history.categories import HistoryCategoryMatcher
from settings import HISTORY_DATA_DIR
from tools.article_scraper import ArticleScraper

if __name__ == "__main__":
    article_scraper = ArticleScraper(data_dir=HISTORY_DATA_DIR, category_matcher=HistoryCategoryMatcher())
    article_scraper.download_articles(start=0)
