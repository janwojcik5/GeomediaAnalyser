from clustering.Cluster import Cluster

__author__ = 'grzegorz.miejski'


class Clusters:
    def __init__(self, clusters, cluster_stats):
        self.clusters = map(lambda c: Cluster(c[0], c[1], cluster_stats[c[0]]), clusters.items())

    def _print(self):
        for cluster in self.clusters:
            cluster._print()

    def save_to_file(self, filename):
        with open(filename, mode="w") as result_file:
            for cluster in self.clusters:
                for word in cluster.words:
                    for stat in cluster.stats.stats:
                        result_file.write(word + "," + stat[0] + "," + str(stat[1]) + "\n")

    def save_to_file_ids_only(self, filename):
        with open(filename, mode="w") as result_file:
            for cluster in self.clusters:
                for stat in cluster.stats.stats:
                    result_file.write(stat[0] + "," + str(cluster.id) + "," + str(stat[1]) + "\n")
