import random
from django.shortcuts import render
from .models import *
from haystack.generic_views import SearchView
from .forms import PodcastSearchForm
from haystack.query import SearchQuerySet
import json
from django.http import HttpResponse
from django.views.generic import DetailView
from audio_annotator.models import PodcastAnnotation


class PodcastView(DetailView):
	model = Podcast

	def get_context_data(self, *args, **kwargs):
		context = super(PodcastView, self).get_context_data(*args, **kwargs)
		topics =[tag.id for tag in self.object.topics.all()]
		related = Podcast.objects.filter(topics__podcast__in=topics).distinct().exclude(id=self.object.id).exclude(active=False)
		context['annotations'] = PodcastAnnotation.objects.filter(podcast=self.object.id)
		return context


def home_page(request):
	keywords = Topic.objects.all()
	keywords = random.choices(keywords,k=5)
	return render(request, 'podcast/home.html', {'keywords': keywords})


def get_topics(request):
	topics = Topic.objects.all()
	return render(request, 'podcast/topics.html', {'topics': topics})


class PodcastSearch(SearchView):
	form_class = PodcastSearchForm
	template = 'search/search.html'
	paginate_by = 10
	context_object_name = 'object_list'

	def get_context_data(self, **kwargs):
		context = super(PodcastSearch, self).get_context_data(**kwargs)
		context['suggestions'] = random.choices(Topic.objects.all(), k = 8)
		return context


def autocomplete(request):
	sug3 = []
	sqs1 = SearchQuerySet().models(Podcast).autocomplete(title_en=request.GET.get('q', ''))[:2]
	sqs3 = SearchQuerySet().models(Podcast).autocomplete(topics=request.GET.get('q', ''))[:3]


	for result in sqs3:
		for topic in result.object.topics.all():
			sug3.append(topic.topic_name)

	sug2 = [result.title_en for result in sqs1]
	suggestions = sug2 + sug3
	the_data = json.dumps({'results': list(set(suggestions))})
	return HttpResponse(the_data, content_type='application/json')