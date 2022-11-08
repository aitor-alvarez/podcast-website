from django import forms
from .models import *


class PodcastForm(forms.ModelForm):
	class Meta:
		model = Annotation
		fields =['annotation', 'time_from', 'time_to']