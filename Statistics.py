# This Python file uses the following encoding: utf-8

import collections
import operator

import numpy as np
import matplotlib.pyplot as plt


class Statistics:
    def __init__(self, list_of_items, statistics_name):
        self.statistics_name = statistics_name
        self.stats = self.get_stats(list_of_items)


    def get_stats(self, list_of_items):
        stats = collections.defaultdict(lambda: 0)
        for item in list_of_items:
            stats[item] += 1
        return stats

    def print_stats(self, printThreshold=0):
        sorted_by_occurrences = sorted(self.stats.items(), key=operator.itemgetter(1))
        sorted_by_occurrences.reverse()
        sorted_by_occurrences = filter(lambda tuple: tuple[0] != '', sorted_by_occurrences)
        sorted_by_occurrences = filter(lambda tuple: tuple[1] > printThreshold, sorted_by_occurrences)

        for tuple in sorted_by_occurrences:
            print(tuple)

        print(self.statistics_name + ": total items count = " + str(sum(map(lambda x: x[1], sorted_by_occurrences))))

    def show_chart(self, printThreshold=0):
        sorted_by_occurrences = sorted(self.stats.values())
        sorted_by_occurrences.reverse()
        sorted_by_occurrences = filter(lambda x: x > printThreshold, sorted_by_occurrences)

        print sorted_by_occurrences
        # sorted_by_occurrences=[1,1,2,2,10,15]
        np_format_data = np.asarray(sorted_by_occurrences)
        n, bins, patches = plt.hist(np_format_data, 100)
        print n
        print bins
        print patches
        plt.plot(bins, n)
        # plt.axis([0,200, 0, 500])
        plt.ylim(0, 75)
        plt.title(u"Histogram częstości występowania tagów")
        #plt.axis('scaled')
        plt.xlabel('w ilu postach jednoczesnie jest tag')
        plt.ylabel('ilosc tagow')
        plt.show()