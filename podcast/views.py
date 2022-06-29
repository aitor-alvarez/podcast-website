from django.shortcuts import render
from .models import *
from haystack.generic_views import SearchView
from .forms import PodcastSearchForm
from collections import Counter


class PodcastSearch(SearchView):
	form_class = PodcastSearchForm
	template = 'search/search.html'
	paginate_by = 5
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



