import random
from django.shortcuts import render
from .models import *
from haystack.generic_views import SearchView
from .forms import PodcastSearchForm
from haystack.query import SearchQuerySet
import json
from django.http import HttpResponse
from django.views.generic import DetailView
from django.db.models import Q


class PodcastView(DetailView):
	model = Podcast

	def get_context_data(self, *args, **kwargs):
		context = super(PodcastView, self).get_context_data(*args, **kwargs)
		tags =[tag.id for tag in self.object.ner.all()]
		topics = []
		related = Podcast.objects.filter(Q(ner__podcast__in=tags) | Q(topics__podcast__in=topics)).distinct().exclude(id=self.object.id).exclude(active=False)
		context['related'] = related
		return context


def home_page(request):
	keywords = Topic.objects.all()
	keywords = random.choices(keywords,k=5)
	return render(request, 'podcast/home.html', {'keywords': keywords})


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