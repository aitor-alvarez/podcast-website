from .models import *
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

class PodcastAdmin(admin.ModelAdmin):
  class Meta:
    model = Podcast
    exclude = ['ner',]


  filter_horizontal = ('topics',)

admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Language)
admin.site.register(NerEntity)
admin.site.register(Topic)
