from django.db import models

class Podcast(models.Model):
	title = models.CharField(max_length=155, blank=False, null=False)
	title_en = models.CharField(max_length=155, blank=False, null=False)
	summary = models.TextField()
	ner = models.ManyToManyField('NerEntity')
	topics = models.ManyToManyField('Topic')
	podcast_url = models.URLField()
	podcast_file = models.FileField(upload_to='')
	duration = models.DurationField()

	def __str__(self):
		return self.title


class NerEntity(models.Model):
	ner_name = models.CharField(max_length=155, blank=False, null=False)

	def __str__(self):
		return self.ner_name


class Topic(models.Model):
	topic_name = models.CharField(max_length=155, blank=False, null=False)

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


