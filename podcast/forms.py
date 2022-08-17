from django import forms
from .models import Podcast, Language, Topic, NerEntity
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
		entity = forms.CharField(required=False, widget=forms.HiddenInput)
		topic = forms.CharField(required=False, widget=forms.HiddenInput)

		def __init__(self, *args, **kwargs):
			super(PodcastSearchForm, self).__init__(*args, **kwargs)
			for visible in self.visible_fields():
				visible.field.widget.attrs['class'] = 'form-control'


		def search(self):

			if self.cleaned_data['q'] =='' and self.cleaned_data['language']:
				sqs = self.searchqueryset.all()
			elif self.cleaned_data['q'] =='' and self.cleaned_data['entity']:
				sqs = self.searchqueryset.all()
			elif self.cleaned_data['q'] =='' and self.cleaned_data['topic']:
				sqs = self.searchqueryset.all()
			else:
				sqs = super(PodcastSearchForm, self).search()

			if not self.is_valid():
				return self.no_query_found()

			if self.cleaned_data['language']:
				sqs = sqs.filter(language=self.cleaned_data['language'])

			if self.cleaned_data['entity']:
				entity = NerEntity.objects.filter(id=self.cleaned_data['entity'])
				sqs = sqs.filter(ner__in=entity)

			if self.cleaned_data['topic']:
				topic = NerEntity.objects.filter(id=self.cleaned_data['topic'])
				print(topic)
				sqs = sqs.filter(topics__in=topic )

			return sqs
