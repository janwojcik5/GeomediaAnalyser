from Articles import Articles
from ArticlesFactory import ArticlesFactory
from Statistics import Statistics
from  TagsOrigin import TagsOrigin
from RakeTags import RakeTags
import rake.rake as rake
from article import Article
from itertools import chain

def print_true_false_table(articles_by_id, found_tags, number_of_tags):
    false_negative = 0
    false_positive = 0
    true_negative = 0
    true_positive = 0
    for article in articles_by_id.values():
        original_tag_set = set(article.tags)
        found_tag_set = found_tags[article.id].copy()

        # clearing sets from empty tags (sometimes happens in file with tagged feeds)
        if '' in original_tag_set:
            original_tag_set.remove('')
        if '' in found_tag_set:
            found_tag_set.remove('')
        # print original_tag_set,found_tag_set

        article_true_positive = 0
        for tag in original_tag_set:
            if tag in found_tag_set:
                article_true_positive += 1
                found_tag_set.remove(tag)
            else:
                false_negative += 1
        for tag in found_tag_set:
            false_positive += 1
        true_positive += article_true_positive
        true_negative += (number_of_tags - article_true_positive)

    print "\t\t\t found tags\tnot found tags\nactually present tags\t\t", true_positive, "\t", false_negative, "\nactually absent tags\t\t", false_positive, "\t", true_negative


if __name__ == "__main__":
    tags_origin = TagsOrigin("./geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA/Dico_Country_Free.csv")
    # articles = ArticlesFactory.all_articles('./geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA')
    articles = ArticlesFactory.from_single_newspaper(
        './geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA/en_AUS_austra_int')
    rake_tags = RakeTags(articles)

    rake_tags.print_keyword_stats(100)
    # found_tags = rake_tags.find_tags(tags_origin,"en")
    rake_tags_per_article = rake_tags.find_tags_for_sentences(tags_origin, "en")
    # for article in articles.articles:
    articles_count = len(articles.articles)
    original_articles_with_tags = len(filter(lambda x: len(x.tags) > 0, articles.articles))
    recreated_articles_with_tags = len(filter(lambda x: len(x[1]) > 0, rake_tags_per_article))

    matching_tags_count = 0.0
    for article in articles.articles:
        original_tags = article.tags
        for found_tag in rake_tags_per_article.get(article.id):
            if found_tag in original_tags:
                matching_tags_count += 1
                break
    print(matching_tags_count / articles_count)

    # compute the number of tags
    tag_set = set()
    for tag in tags_origin.tags:
        tag_set.add(tag.tag)
    if '' in tag_set:
        tag_set.remove('')

    # print statistics:
    all_original_tags = list(chain.from_iterable(map(lambda article: article.tags, articles.articles)))
    Statistics(all_original_tags).print_stats(100)

    flatmapped_rake_tags = list(chain.from_iterable(rake_tags_per_article.values()))
    Statistics(flatmapped_rake_tags).print_stats(100)

    print_true_false_table(articles.create_articles_map(articles.articles), rake_tags_per_article, len(tag_set))
