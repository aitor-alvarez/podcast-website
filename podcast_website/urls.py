from django.contrib import admin
from django.urls import path, include
from podcast.views import *
from django.views.generic import TemplateView
from django.conf.urls.static import static
from podcast_website import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='podcast/home.html'), name='home'),
    path('search/', PodcastSearch.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
