from Articles import Articles
from  TagsOrigin import TagsOrigin
from RakeTags import RakeTags
import rake.rake as rake
from article import Article


class CSVArticleDao():
    def get_article(self, feed, articleID):
        feed_file = open("./geomedia/cist-sample_geomedia-db/Sample_GeomediaDB/" + feed + "/rss_unique_tagged.csv", "r")
        for line in feed_file.readlines():
            parts = line.split('\t')
            if parts[1] == articleID:
                article = Article()
                article.id = parts[0]
                article.feed = parts[1]
                article.time = parts[2]
                article.title = parts[3]
                article.text = parts[4]
                return article


if __name__ == "__main__":
    tags_origin = TagsOrigin("./geomedia/cist-sample_geomedia-db/Sample_GeomediaDB/Dico_Country_Free.csv")
    articles = Articles('en_AUS_austra_int')
    rake_tags = RakeTags(articles)

    found_tags = rake_tags.find_tags(tags_origin)
    print("")

    # if len(sys.argv) < 2:
    # for article in dao.get_articles('en_AUS_austra_int'):
    #         keywords = rake_object.run(article.text)
    #         print '\n' + article.text
    #         print keywords
    # elif len(sys.argv) == 2:
    #     for article in dao.get_articles(sys.argv[1]):
    #         keywords = rake_object.run(article.text)
    #         print '\n' + article.text
    #         print keywords
    # else:
    #     article = dao.get_article(sys.argv[1], sys.argv[2])
    #     keywords = rake_object.run(article.text)
    #     print '\n' + article.text
    #     print keywords + '\n'
