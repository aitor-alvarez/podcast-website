import datetime
from haystack import indexes
from .models import Podcast


class PodcastIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	summary = indexes.CharField(model_attr='summary')
	title = indexes.EdgeNgramField(model_attr='title')
	title_en = indexes.EdgeNgramField(model_attr='title_en')
	entity = indexes.EdgeNgramField(model_attr='ner')
	language = indexes.CharField(model_attr='language')
	topics = indexes.EdgeNgramField(model_attr='topics')


	def get_model(self):
		return Podcast

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(active=True)

	def prepare_topics(self, object):
		return [topic.name for topic in object.topics.all()]

	def prepare_topics(self, object):
		return [topic.topic_name for topic in object.topics.all()]