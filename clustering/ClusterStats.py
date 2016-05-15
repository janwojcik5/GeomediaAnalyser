from collections import defaultdict, Counter
import operator

__author__ = 'grzegorz.miejski'


class ClusterStats:
    def __init__(self, list_of_feed):
        self.total_count = len(list_of_feed)
        self.original_list_of_feeds = list_of_feed
        self.stats = self.calculate_stats(list_of_feed)

    def add_stat(self, feed, percent):
        self.stats[feed] = percent

    def calculate_stats(self, list_of_feed):
        result = defaultdict(list)
        counter = Counter(list_of_feed)

        for feed_name, items_count in counter.items():
            result[feed_name.replace("\"", "")] = float(items_count) / float(self.total_count) * 100
        return sorted(result.items(), key=operator.itemgetter(1), reverse=True)

    def _print(self):
        limit = min(len(self.stats), 6)
        for kv in self.stats[:limit]:
            print(kv)

    def to_string(self):
        result = ""
        for kv in self.stats:
            result += str(kv)
        return result