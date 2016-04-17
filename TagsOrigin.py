from  collections import defaultdict


class TagsOrigin:
    def __init__(self, path):
        self.tags = self.prepare_tags_set(path)
        self.tags_by_words = self.get_tags_by_words()
        self.tags_by_language = self.prepare_tags_by_language()


    def prepare_tags_set(self, path):
        connections_file = open(path, "r")
        tags = []
        for line in connections_file.readlines()[1:]:
            parts = line.split('\t')
            tag = TagWord()
            tag.id = parts[0]
            tag.tag = parts[1].replace("\"", "")
            tag.word = parts[2].lower()
            tag.language = parts[5]
            tags.append(tag)
        return tags

    def get_tags_by_words(self):
        result = defaultdict(list)
        for tag in self.tags:
            result[tag.word].append(tag)
        return result

    def get_tags(self, word, language=None):
        if language == None:
            return self.tags_by_words[word]
        else:
            return self.tags_by_language[language][word]

    def prepare_tags_by_language(self):
        result = defaultdict(lambda: defaultdict(list))
        for tag in self.tags:
            result[tag.language][tag.word].append(tag)
        return result

class TagWord:
    def __init__(self):
        pass


