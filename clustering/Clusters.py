__author__ = 'grzegorz.miejski'


class Clusters:
    def __init__(self, clusters):
        self.clusters = dict((k, v) for k, v in map(lambda x: (x.id, x), clusters))
