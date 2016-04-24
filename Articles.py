class Articles():
    def __init__(self, articles):
        self.articles = articles
        self.mapped_articles = self.create_articles_map(self.articles)

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
