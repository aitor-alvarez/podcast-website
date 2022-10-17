from django.db import models
from podcast.models import Podcast

class PodcastAnnotation(models.Model):
	podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
	annotations = models.ManyToManyField('Annotation', blank=True, null=True)

	def __str__(self):
		return self.podcast.title


class Annotation(models.Model):
	annotation = models.TextField()
	time_from = models.DurationField()
	time_to = models.DurationField()

