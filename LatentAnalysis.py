from gensim import corpora
import gensim
import re
from collections import defaultdict

__author__ = 'jan.wojcik'


class LatentAnalysis():
    def __init__(self, articles, file_with_stopwords="./rake/SmartStoplist.txt"):
        self.articles = articles
        # create a list of stopwords
        self.stopwords = []
        for line in open(file_with_stopwords, 'r').readlines():
            # don't include comments
            if line[0] != '#':
                self.stopwords.append(line[:-1])


    def generate_corpus(self, outputfile='./defaultCorpusFile.mm'):
        list_for_corpus = []
        for article in self.articles.articles:
            list_for_article = []
            # Take the text and topic and split it into words. At the moment words include only English letters
            normal_words = map(lambda x: x.lower(), re.findall("[a-zA-z\-']+", article.title + ' ' + article.text))
            for word in normal_words:
                if word not in self.stopwords:
                    list_for_article.append(word)
            list_for_corpus.append(list_for_article)
        self.dictionary = corpora.Dictionary(list_for_corpus)
        print self.dictionary
        # create corpus
        self.corpus = [self.dictionary.doc2bow(list_for_article) for list_for_article in list_for_corpus]
        # print self.corpus

    def save_corpus(self, outputfile='./defaultCorpusFile.mm'):
        corpora.MmCorpus.serialize(outputfile, self.corpus)

    def load_corpus(self, inputfile='./defaultCorpusFile.mm'):
        self.corpus = corpora.MmCorpus(inputfile)

    def save_dictionary(self, outputfile='./defaultDictionaryFile.dict'):
        self.dictionary.save(outputfile)

    def load_dictionary(self, inputfile='./defaultDictionaryFile.dict'):
        self.dictionary = gensim.corpora.Dictionary.load(inputfile)

    def perform_LSA_analysis(self):
        lsi = gensim.models.lsimodel.LsiModel(corpus=self.corpus, id2word=self.dictionary, num_topics=100)
        print lsi.print_topics(20)

    def perform_LDA_analysis(self):
        lda = gensim.models.ldamodel.LdaModel(corpus=self.corpus, id2word=self.dictionary, num_topics=100,
                                              update_every=1, chunksize=10000, passes=1)
        print lda.print_topics(20)
    