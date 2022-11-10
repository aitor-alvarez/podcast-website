from django.shortcuts import render
from podcast.models import *
from .models import *
from .forms import *
from django.http import HttpResponse


def get_podcast(request, podcast_id):
	podcast = Podcast.objects.get(id=podcast_id)
	podcast_form = PodcastForm()
	return  render(request, 'audio_annotator/annotator.html', {'form': podcast_form, 'podcast': podcast})


def save_annotation(request, data, podcast_id):
	if request.is_ajax() and request.method == 'POST':
		if PodcastAnnotation.objects.get(podcast=podcast_id).exists():
			podcast_annotation = PodcastAnnotation.objects.get(podcast=podcast_id)
			annotation = Annotation.objects.create(annotation=data[0], time_from=data[1], time_to=data[2])
			podcast_annotation.annotations.add(annotation.id)
			return HttpResponse("Annotation saved")
		else:
			podcast = Podcast.objects.get(id=podcast_id)
			podcast_annotation = PodcastAnnotation.objects.create(podcast=podcast)
			annotation = Annotation.objects.create(annotation=data[0], time_from=data[1], time_to=data[2])
			podcast_annotation.annotations.add(annotation.id)



