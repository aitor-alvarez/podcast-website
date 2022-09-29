from django.db import models
import datetime


class Podcast(models.Model):
	title = models.CharField(max_length=155, blank=False, null=False)
	title_en = models.CharField(max_length=155, blank=True, null=True)
	author = models.CharField(max_length=155, blank=True, null=True)
	image = models.ImageField(upload_to='img', blank=True, null=True)
	summary = models.TextField(blank=True, null=True)
	ner = models.ManyToManyField('NerEntity', blank=True)
	topics = models.ManyToManyField('Topic', blank=True)
	language = models.ForeignKey('Language', on_delete=models.CASCADE)
	podcast_url = models.URLField(blank=True)
	podcast_file = models.FileField(upload_to='podcast', blank=True, null=True)
	duration = models.DurationField(blank=True, null=True)
	sophistication = models.IntegerField(blank=True, null=True, decimal_places=2, max_digits=4)
	guid = models.CharField(max_length=155, blank=True, null=True)
	created = models.DateTimeField(default=datetime.datetime.now(), blank=True, null=True)
	active = models.BooleanField(default=False, blank=True, null=True)

	def __str__(self):
		return self.title_en


class NerEntity(models.Model):
	ner_name = models.CharField(max_length=155, blank=False, null=False)

	def __str__(self):
		return self.ner_name


class Topic(models.Model):
	topic_name = models.CharField(max_length=155, blank=False, null=False)
	time_from = models.DurationField(blank=True, null=True)
	time_to = models.DurationField(blank=True, null=True)

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