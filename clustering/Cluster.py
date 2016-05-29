__author__ = 'grzegorz.miejski'


class Cluster:
    def __init__(self, id, words, stats):
        self.id = id
        self.words = words
        self.stats = stats

    def to_string(self):
        "Cluster " + str(self.id) + " with words:\n" + self.words + "\n" + self.stats.to_string()

    def _print(self):
        print("Cluster " + str(self.id) + " with words:")
        print(self.words)
        self.stats._print()