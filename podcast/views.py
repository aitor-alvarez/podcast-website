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
from django.db.models import Q


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
	podcasts_ar = Podcast.objects.filter(language_id=3)
	topics_ar = [(t.id, t.topic_name) for c in podcasts_ar for t in c.topics.all()]
	podcasts_chn = Podcast.objects.filter(language_id=1)
	topics_chn = [(t.id, t.topic_name) for c in podcasts_chn for t in c.topics.all()]
	podcasts_ru = Podcast.objects.filter(language_id=2)
	topics_ru = [(t.id, t.topic_name) for c in podcasts_ru for t in c.topics.all()]
	podcasts_br = Podcast.objects.filter(language_id=4)
	topics_br = [(t.id, t.topic_name) for c in podcasts_br for t in c.topics.all()]
	return render(request, 'podcast/topics.html', {'topics_ar': set(topics_ar),'topics_chn': set(topics_chn),
												   'topics_ru': set(topics_ru), 'topics_br': set(topics_br) })


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


#API search view
def api_search(request):
	sqs1 = SearchQuerySet().models(Podcast).filter(language=request.GET.get('language', ''))\
		.filter(Q(title_en__icontains= request.GET.get('q', '')) | Q(summary__icontains= request.GET.get('q', '')))
	sqs2 = SearchQuerySet().models(Podcast).filter(topics__topic_name__contains=request.GET.get('q', ''))
	sqs1 += [s for s in sqs2 if s not in sqs1]
	pods = [{"title": s.title_en, "summary": s.summary, "topics": [t.topic_name for t in s.topics.all], "uri": "/podcast/"+s.id} for s in sqs1]
	podcasts = json.dumps({'results': pods})
	return podcasts
