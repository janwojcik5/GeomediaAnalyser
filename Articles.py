from article import Article


class Articles():
    def __init__(self, feed):
        self.articles = self.parse_articles(feed)
        self.mapped_articles = self.create_articles_map(self.articles)

    def parse_articles(self, feed):
        feed_file = open("./geomedia/cist-sample_geomedia-db/Sample_GeomediaDB/" + feed + "/rss_unique_tagged.csv", "r")
        returnList = list()
        for line in feed_file.readlines():
            parts = line.split('\t')
            article = Article()
            article.id = parts[0]
            article.feed = parts[1]
            article.time = parts[2]
            article.title = parts[3]
            article.text = parts[4]
            article.add_tag(parts[5].replace("\"", ""))
            returnList.append(article)
        return returnList

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
