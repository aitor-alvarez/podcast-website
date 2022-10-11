from django.contrib import admin
from django.urls import path, include
from podcast.views import *
from django.views.generic import TemplateView
from django.conf.urls.static import static
from podcast_website import settings
from podcast.views import autocomplete

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('search/', PodcastSearch.as_view()),
    path('search/auto/', autocomplete),
    path('podcast/<pk>', PodcastView.as_view()),
    path('about', TemplateView.as_view(template_name='podcast/about.html'), name='about')

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
