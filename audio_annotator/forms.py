from django import forms
from .models import *


class PodcastAnnotationForm(forms.ModelForm):
	class Meta:
		model = Annotation
		fields =['annotation', 'time_from', 'time_to']