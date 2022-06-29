from django import forms
from .models import Podcast, Language, Topic
from haystack.forms import SearchForm


class PodcastForm(forms.ModelForm):
	class Meta:
		model = Podcast
		exclude = ['created',]

	def __init__(self, *args, **kwargs):
		super(PodcastForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'



class PodcastSearchForm(SearchForm):
		language = forms.ModelChoiceField(queryset=Language.objects.all(), required=False, empty_label='Select the language')

		def __init__(self, *args, **kwargs):
			super(PodcastSearchForm, self).__init__(*args, **kwargs)
			for visible in self.visible_fields():
				visible.field.widget.attrs['class'] = 'form-control'


		def search(self):

			if self.cleaned_data['q'] =='' and self.cleaned_data['language']:
				sqs = self.searchqueryset.all()
			elif self.cleaned_data['q'] =='':
				sqs = self.searchqueryset.all()
			else:
				sqs = super(PodcastSearchForm, self).search()
			if not self.is_valid():
				return self.no_query_found()

			if self.cleaned_data['language']:
				sqs = sqs.filter(language=self.cleaned_data['language'])

			return sqs
