from django.db import models
from s3direct.fields import S3DirectField
import datetime


class Podcast(models.Model):
	title = models.CharField(max_length=155, blank=False, null=False)
	title_en = models.CharField(max_length=155, blank=False, null=False)
	summary = models.TextField()
	ner = models.ManyToManyField('NerEntity')
	topics = models.ManyToManyField('Topic')
	language = models.ForeignKey('Language')
	podcast_url = models.URLField()
	podcast_file = S3DirectField(dest='podcasts', blank=True)
	duration = models.DurationField()
	created = models.DateTimeField(default=datetime.datetime.now())

	def __str__(self):
		return self.title


class NerEntity(models.Model):
	ner_name = models.CharField(max_length=155, blank=False, null=False)

	def __str__(self):
		return self.ner_name


class Topic(models.Model):
	topic_name = models.CharField(max_length=155, blank=False, null=False)
	time_step = models.DurationField(blank=True, null=True)

	def __str__(self):
		return self.topic_name


class Language(models.Model):
	language_name = models.CharField(max_length=155, blank=False, null=False)

	def __str__(self):
		return self.language_name


class Feedback(models.Model):
	podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
	feedback = models.BooleanField()
	feedback_text = models.TextField()

	def __str__(self):
		return "Feedback for: "+self.podcast.title


