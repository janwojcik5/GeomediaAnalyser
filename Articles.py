import os
from article import Article


class Articles():
    def __init__(self, feeds_directory, language="en"):
        self.articles = self.parse_articles(feeds_directory, language)
        self.mapped_articles = self.create_articles_map(self.articles)

    def parse_articles(self, feed_directory, language):
        parsed_articles = list()
        subdirectories = next(os.walk(feed_directory))[1]
        language_filtered_newspapers = list(filter(lambda name: name.startswith(language), subdirectories))
        newspapers_directories = map(lambda l: feed_directory + "/" + l, language_filtered_newspapers)
        for newspaper_dir in newspapers_directories:
            parsed_articles_file = newspaper_dir + "/rss_unique_TAG_country_Ebola.csv"
            print("Parsing " + parsed_articles_file)
            feed_file = open(parsed_articles_file, "r")
            lines = feed_file.readlines()
            for line in lines:
                parts = line.split('\t')
                article = Article()
                article.id = parts[0]
                article.feed = parts[1]
                article.time = parts[2]
                article.title = parts[3]
                article.text = parts[4]
                article.add_tag(parts[5].replace("\"", ""))
                parsed_articles.append(article)
            feed_file.close()
        return parsed_articles

    def create_articles_map(self, articles):
        articles_by_id = {}
        for article in articles:
            if articles_by_id.has_key(article.id) and article.has_tag():
                articles_by_id.get(article.id).add_tag(article.tags[0])
            else:
                articles_by_id[article.id] = article
        return articles_by_id
        # return {k: v for k, v in ((x.id, x) for x in self.articles)}

    def get_article(self, id):
        self.mapped_articles.get(id)

    def articles_with_more_than_one_tag(self):
        return filter(lambda x: len(x.tags) > 1, self.mapped_articles.values())
