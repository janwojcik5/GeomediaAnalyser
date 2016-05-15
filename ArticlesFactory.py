import os
from Articles import Articles
from article import Article

__author__ = 'grzegorz.miejski'


class ArticlesFactory():
    def __init__(self, feeds_directory, language="en"):
        pass

    @staticmethod
    def from_single_newspaper(feed):
        directory_name = feed + "/rss_unique_TAG_country_Ebola.csv"
        return Articles(ArticlesFactory.single_parsed_directory(directory_name))
        pass

    @staticmethod
    def single_parsed_directory(parsed_articles_file):
        articles = []
        print("Parsing " + parsed_articles_file)
        feed_file = open(parsed_articles_file, "r")
        lines = feed_file.readlines()
        for line in lines[1:]:
            parts = line.split('\t')
            article = Article()
            article.id = parts[0]
            article.feed = parts[1]
            article.time = parts[2]
            article.title = parts[3]
            article.text = parts[4]
            article.add_tag(parts[5].replace("\"", ""))
            articles.append(article)
        feed_file.close()
        return articles

    @staticmethod
    def parse_articles(feed_directory, language):
        parsed_articles = list()
        subdirectories = next(os.walk(feed_directory))[1]
        language_filtered_newspapers = list(filter(lambda name: name.startswith(language), subdirectories))
        newspapers_directories = map(lambda l: feed_directory + "/" + l, language_filtered_newspapers)
        for newspaper_dir in newspapers_directories:
            parsed_articles_file = newspaper_dir + "/rss_unique_TAG_country_Ebola.csv"
            articles = ArticlesFactory.single_parsed_directory(parsed_articles_file)
            parsed_articles = parsed_articles + articles
        return parsed_articles

    @staticmethod
    def all_articles(feeds_directory, language="en"):
        return Articles(ArticlesFactory.parse_articles(feeds_directory, language))
        pass
