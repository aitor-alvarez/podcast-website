from django.shortcuts import render
from .models import *
from haystack.generic_views import SearchView
from .forms import PodcastSearchForm
from collections import Counter
from haystack.query import SearchQuerySet
import json
from django.http import HttpResponse
from django.views.generic import DetailView


class PodcastView(DetailView):
	model = Podcast

	def get_context_data(self, *args, **kwargs):
		context = super(PodcastView, self).get_context_data(*args, **kwargs)
		tags =[tag.id for tag in self.object.tags.all()]
		related = Podcast.objects.filter(tags__in=tags).distinct().exclude(id=self.object.id)
		context['related'] = related
		return context


class PodcastSearch(SearchView):
	form_class = PodcastSearchForm
	template = 'search/search.html'
	paginate_by = 10
	context_object_name = 'object_list'



	def get_context_data(self, *args, **kwargs):
		context = super(PodcastSearch, self).get_context_data(*args, **kwargs)


		return context


def autocomplete(request):
	sug1 = []
	sqs1 = SearchQuerySet().models(Podcast).autocomplete(title=request.GET.get('q', ''))[:5]
	sqs2 = SearchQuerySet().models(Podcast).autocomplete(tags=request.GET.get('q', ''))[:5]
	for result in sqs2:
		for tag in result.tags.split(','):
			sug1.append(tag)
	sug2 = [result.title for result in sqs1]
	suggestions = sug1 + sug2
	the_data = json.dumps({'results': suggestions})
	return HttpResponse(the_data, content_type='application/json')




