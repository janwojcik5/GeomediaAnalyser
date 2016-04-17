import collections
import operator


class Statistics:
    def __init__(self, list_of_items):
        self.stats = self.get_stats(list_of_items)


    def get_stats(self, list_of_items):
        stats = collections.defaultdict(lambda: 0)
        for item in list_of_items:
            stats[item] += 1
        return stats

    def print_stats(self,printThreshold=0):
        sorted_by_occurrences = sorted(self.stats.items(), key=operator.itemgetter(1))
        sorted_by_occurrences.reverse()
        sorted_by_occurrences = filter(lambda tuple: tuple[0] != '', sorted_by_occurrences)
        sorted_by_occurrences = filter(lambda tuple: tuple[1] > printThreshold,sorted_by_occurrences)

        for tuple in sorted_by_occurrences:
            print(tuple)

        print("total items count = " + str(sum(map(lambda x: x[1], sorted_by_occurrences))))
