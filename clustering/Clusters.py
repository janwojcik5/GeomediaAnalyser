from clustering.Cluster import Cluster

__author__ = 'grzegorz.miejski'


class Clusters:
    def __init__(self, clusters, cluster_stats):
        self.clusters = map(lambda c: Cluster(c[0], c[1], cluster_stats[c[0]]), clusters.items())

    def _print(self):
        for cluster in self.clusters:
            cluster._print()