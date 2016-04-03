import rake.rake as rake
import os
from article import Article
import operator
import sys

class CSVArticleDao():
	
	def get_articles(self,feed):
		feed_file=open("./geomedia/cist-sample_geomedia-db/Sample_GeomediaDB/"+feed+"/rss_unique.csv","r")
		returnList=list()
		for line in feed_file.readlines():
			parts=line.split('\t')
			article=Article()
			article.id=parts[0]
			article.feed=parts[1]
			article.time=parts[2]
			article.title=parts[3]
			article.text=parts[4]
			returnList.append(article)
		return returnList

	def get_article(self,feed,articleID):
		feed_file=open("./geomedia/cist-sample_geomedia-db/Sample_GeomediaDB/"+feed+"/rss_unique.csv","r")
		for line in feed_file.readlines():
			parts=line.split('\t')
			if parts[1]==articleID:
				article=Article()
				article.id=parts[0]
				article.feed=parts[1]
				article.time=parts[2]
				article.title=parts[3]
				article.text=parts[4]
				return article

dao=CSVArticleDao()
#print dao.get_articles('en_AUS_austra_int')
#for article in dao.get_articles('en_AUS_austra_int'):
#	print article.id
#	print article.feed
#	print article.time
#	print article.title
#	print article.text

rake_object=rake.Rake("./rake/SmartStoplist.txt",3,3,1)

if len(sys.argv)<2:
	for article in dao.get_articles('en_AUS_austra_int'):
		keywords=rake_object.run(article.text)
		print '\n'+article.text
		print keywords
elif len(sys.argv)==2:
	for article in dao.get_articles(sys.argv[1]):
		keywords=rake_object.run(article.text)
		print '\n'+article.text
		print keywords
else:
	article=dao.get_article(sys.argv[1],sys.argv[2])
	keywords=rake_object.run(article.text)
	print '\n'+article.text
	print keywords+'\n'
