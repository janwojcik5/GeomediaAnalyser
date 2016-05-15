__author__ = 'grzegorz.miejski'


class Cluster:
    def __init__(self, id, words, stats):
        self.id = id
        self.words = words
        self.stats = stats

    def _print(self):
        print("Cluster " + str(self.id) + " with words:")
        print(self.words)
        self.stats._print()