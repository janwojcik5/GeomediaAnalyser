from collections import defaultdict

from datetime import datetime
from datetime import timedelta

from ArticlesFactory import ArticlesFactory
from clustering.ClusterStats import ClusterStats
from clustering.Clusters import Clusters

#for drawing charts
import pandas as pd
import matplotlib.pyplot as plt

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
        
    #analyse dates and times
    time_with_cluster = zip(k_means_labels, map(lambda article: article.time, articles.articles))
    
    time_lists=defaultdict(list)
    time_means=[]
    time_deviation=[]
    
    for cluster_with_time in time_with_cluster:
	d=datetime.strptime(cluster_with_time[1].strip("\""),"%Y-%m-%d %H:%M:%S")
	time_lists[cluster_with_time[0]].append(d)
    
    #print data for chart
    i=0
    for cluster_nr in time_lists.keys():
	f=open("cluster_nr"+str(i)+".txt","w")
	f.write("date"+str(i)+"\n")
	for dt in time_lists[cluster_nr]:
	  f.write(dt.strftime("%Y-%m-%d\n"))# %H:%M:%S")+"\n")
	i+=1
	
    #calculate means
    for cluster_nr in time_lists.keys():
	for i in range(len(time_lists[cluster_nr])-1):
	    delta=((time_lists[cluster_nr][i+1]-time_lists[cluster_nr][i])*(i+1))/(i+2)
	time_means.append(time_lists[cluster_nr][0]+delta)
	
    #calculate standard deviation
    #for cluster_nr in time_lists.keys():
	#for i in range(len(time_lists[cluster_nr])-1):
	 #   delta=((time_lists[cluster_nr][i+1]-time_lists[cluster_nr][i
    
    print map(lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"),time_means)
    
    print("Calculate cluster statistics")
    cluster_stats = map_values(grouped_feeds, group_by_feed_fun)
    return Clusters(clusters_keywords, cluster_stats)

def print_histograms(n_clusters=10,plot_kind='line'):
    df=pd.DataFrame()
    for i in range(n_clusters):
      new_df=pd.read_csv("cluster_nr"+str(i)+".txt")
      new_df['date'+str(i)]=pd.DatetimeIndex(new_df['date'+str(i)]).normalize()
      new_df=new_df.groupby([new_df['date'+str(i)].dt.year,new_df['date'+str(i)].dt.month]).count()
      #print new_df
      df=pd.concat([df,new_df],axis=1)#,ignore_index=True)
    #print df
    df.plot(kind=plot_kind)
    plt.show()
    
if __name__ == "__main__":
    n_clusters = 10
    #articles = ArticlesFactory.all_articles('../geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA')
    articles = ArticlesFactory.from_single_newspaper('../geomedia/Geomedia_extract_AGENDA/Geomedia_extract_AGENDA/en_AUS_austra_int')

    clusters = calculate_clusters(articles, n_clusters)
    clusters._print()
    print_histograms(n_clusters)
    print
