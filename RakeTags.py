import rake.rake as rake


class RakeTags:
    def __init__(self, articles):
        self.rake_object = rake.Rake("./rake/SmartStoplist.txt", 3, 3, 1)
        self.rake_keywords = self.get_rake_keywords(articles)

    def get_rake_keywords(self, articles):
        rake_tags = {}
        for article in articles.articles:
            rake_tags[article.id] = self.rake_object.run(article.text)
        return rake_tags

    def find_tags(self, tags_origin, language=None):
        per_article_tag_found = {}
        for article_id, rake_tags in self.rake_keywords.iteritems():
            found_tags = set()
            for rake_tag in rake_tags:
                rake_sentences_words = rake_tag[0].split(" ")
                for word in rake_sentences_words:
                    matching_tags = tags_origin.get_tags(word, language)
                    if len(matching_tags) > 0:
                        for x in matching_tags:
                            found_tags.add(x.tag)
            per_article_tag_found[article_id] = found_tags
        return per_article_tag_found

