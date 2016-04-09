from  collections import defaultdict


class TagsOrigin:
    def __init__(self, path):
        self.tags = self.prepare_tags_set(path)
        self.tags_by_words = self.get_tags_by_words()

    def prepare_tags_set(self, path):
        connections_file = open(path, "r")
        tags = []
        for line in connections_file.readlines():
            parts = line.split('\t')
            tag = TagWord()
            tag.id = parts[0]
            tag.tag = parts[1]
            tag.word = parts[2].lower()
            tags.append(tag)
        return tags

    def get_tags_by_words(self):
        result = defaultdict(list)
        for tag in self.tags:
            if tag.word in result.keys():
                print("duplicate")
            result[tag.word].append(tag)
        return result

    def get_tags(self, word):
        return self.tags_by_words[word]


class TagWord:
    def __init__(self):
        pass


