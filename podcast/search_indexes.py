import datetime
from haystack import indexes
from .models import Podcast


class PodcastIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	summary = indexes.CharField(model_attr='summary')
	title = indexes.EdgeNgramField(model_attr='title')
	title_en = indexes.EdgeNgramField(model_attr='title_en')
	ner = indexes.EdgeNgramField(model_attr='ner')
	language = indexes.CharField(model_attr='language')
	topics = indexes.CharField(model_attr='content_area')


	def get_model(self):
		return Podcast

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(created__lte= datetime.datetime.now())

	def prepare_tags(self, object):
		return [tag.name for tag in object.ner.all()]

	def prepare_topics(self, object):
		return [topic.name for topic in object.topics.all()]