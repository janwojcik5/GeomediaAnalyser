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

if __name__ == "__main__":
    n_clusters = 10
    articles = ArticlesFactory.from_single_newspaper(
        '../geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA/en_AUS_austra_int')
    documents = map(lambda article: article.text, articles.articles)

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    # calculate k_means
    k_means = KMeans(init='k-means++', n_clusters=n_clusters, max_iter=100, n_init=1)
    k_means.fit(X)
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    clusters = k_means.labels_.tolist()


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
    cluster_stats = {}

    grouped_feeds = defaultdict(list)
    for cluster_with_article in feed_with_cluster:
        grouped_feeds[cluster_with_article[0]].append(cluster_with_article[1])

    clusters_obj = 1

    cluster_stats = map_values(grouped_feeds, group_by_feed_fun)

    Clusters()
    pass

    # import matplotlib.pyplot as plt
    #
    # from sklearn.metrics.pairwise import cosine_similarity
    #
    # dist = 1 - cosine_similarity(X)
    #
    # from sklearn.manifold import MDS
    #
    # MDS()
    #
    # # convert two components as we're plotting points in a two-dimensional plane
    # # "precomputed" because we provide a distance matrix
    # # we will also specify `random_state` so the plot is reproducible.
    # mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    #
    # pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
    #
    # xs, ys = pos[:, 0], pos[:, 1]
    # print()
    # print()
    #
    # titles = map(lambda article: article.title, articles.articles)
    #
    # df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles))
    #
    # # group by cluster
    # groups = df.groupby('label')
    #
    # # set up plot
    # fig, ax = plt.subplots(figsize=(17, 9))  # set size
    # ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
    #
    # cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}
    #
    # # set up cluster names using a dict
    # cluster_names = {0: 'Family, home, war',
    # 1: 'Police, killed, murders',
    # 2: 'Father, New York, brothers',
    # 3: 'Dance, singing, love',
    # 4: 'Killed, soldiers, captain'}
    #
    # #iterate through groups to layer the plot
    # #note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    # for name, group in groups:
    # ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
    # label=cluster_names[name], color=cluster_colors[name],
    # mec='none')
    # ax.set_aspect('auto')
    # ax.tick_params( \
    # axis='x',  # changes apply to the x-axis
    # which='both',  # both major and minor ticks are affected
    # bottom='off',  # ticks along the bottom edge are off
    #         top='off',  # ticks along the top edge are off
    #         labelbottom='off')
    #     ax.tick_params( \
    #         axis='y',  # changes apply to the y-axis
    #         which='both',  # both major and minor ticks are affected
    #         left='off',  # ticks along the bottom edge are off
    #         top='off',  # ticks along the top edge are off
    #         labelleft='off')
    #
    # ax.legend(numpoints=1)  #show legend with only 1 point
    #
    # #add label in x,y position with the label as the film title
    # for i in range(len(df)):
    #     ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)
    #
    # plt.show()  #show the plot
    #
    #
    #
    # # plot #
    # colors = ['#4EACC5', '#FF9C34', '#4E9A06']
    # plt.figure()
    # plt.hold(True)
    # for k, col in zip(range(n_clusters), colors):
    #     my_members = k_means_labels == k
    #     cluster_center = k_means_cluster_centers[k]
    #     plt.plot(X[my_members, 0], X[my_members, 1], 'w',
    #              markerfacecolor=col, marker='.')
    #     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #              markeredgecolor='k', markersize=6)
    # plt.title('KMeans')
    #
