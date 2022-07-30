from django.shortcuts import render
from .models import *
from haystack.generic_views import SearchView
from .forms import PodcastSearchForm
from collections import Counter
from haystack.query import SearchQuerySet
import json
from django.http import HttpResponse


class PodcastSearch(SearchView):
	form_class = PodcastSearchForm
	template = 'search/search.html'
	paginate_by = 10
	context_object_name = 'object_list'



	def get_context_data(self, *args, **kwargs):
		context = super(PodcastSearch, self).get_context_data(*args, **kwargs)
		ner_tags = [(s.object.ner, s.object.content_area.id)  for s in context['object_list']]
		ner_tags = Counter(ner_tags)
		ner_tags = [(n, ner_tags[n]) for n in ner_tags ]
		context.update({'ner_tags': ner_tags})

		languages = [(s.object.language, s.object.language.id) for s in context['object_list']]
		languages = Counter(languages)
		languages = [(l, languages[l]) for l in languages]
		context.update({'languages': languages})

		topics = [(s.object.get_content_type_display(), s.object.content_type) for s in context['object_list']]
		topics = Counter(topics)
		topics = [(t, topics[t]) for t in topics]
		context.update({'topics': topics})

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




