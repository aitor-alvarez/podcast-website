from django.shortcuts import render
from .models import *


def get_podcasts(request, lang=None):
	podcasts = Podcast.objects.all().order_by('-id')
	return render(request, template_name='podcast/podcasts.html', context={'podcasts':podcasts})


