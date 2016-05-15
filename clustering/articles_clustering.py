from collections import defaultdict

from ArticlesFactory import ArticlesFactory
from clustering.ClusterStats import ClusterStats
from clustering.Clusters import Clusters


__author__ = 'grzegorz.miejski'
from sklearn.feature_extraction.text import TfidfVectorizer


def map_values(dictionary, function):
    return dict(map(lambda (k, v): (k, function(v)), dictionary.iteritems()))


def group_by_feed_fun(list_of_feed):
    return ClusterStats(list_of_feed)


from sklearn.cluster import KMeans


def calculate_clusters(articles, n_clusters=10):
    documents = map(lambda article: article.text, articles.articles)

    print("Vectorize articles")
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    print("Calculate k_means")
    k_means = KMeans(init='k-means++', n_clusters=n_clusters, max_iter=100, n_init=1)
    k_means.fit(X)
    k_means_labels = k_means.labels_

    # get clusters keywords
    order_centroids = k_means.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    clusters_keywords = {}
    print("Top terms per cluster:")
    for i in range(n_clusters):
        print "Cluster %d:" % i,
        c_words = []
        for ind in order_centroids[i, :10]:
            c_words.append(terms[ind])
            print ' %s' % terms[ind],
        clusters_keywords[i] = c_words
        print

    # join clusters with articles
    feed_with_cluster = zip(k_means_labels, map(lambda article: article.feed, articles.articles))

    grouped_feeds = defaultdict(list)
    for cluster_with_article in feed_with_cluster:
        grouped_feeds[cluster_with_article[0]].append(cluster_with_article[1])

    print("Calculate cluster statistics")
    cluster_stats = map_values(grouped_feeds, group_by_feed_fun)
    return Clusters(clusters_keywords, cluster_stats)


if __name__ == "__main__":
    n_clusters = 30
    articles = ArticlesFactory.all_articles('../geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA')
    # articles = ArticlesFactory.from_single_newspaper('../geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA/en_AUS_austra_int')
    # articles.articles = articles.articles[:4000]

    clusters = calculate_clusters(articles, n_clusters)
    clusters._print()
    clusters.save_to_file("./results/clusters.csv")
    clusters.save_to_file_ids_only("./results/clusters_to_cluster_id.csv")
    print
