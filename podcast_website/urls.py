from django.contrib import admin
from django.urls import path, include
from podcast.views import *
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from podcast_website import settings
from podcast.views import autocomplete
from podcast_user.views import *
from audio_annotator.views import *


urlpatterns = [
    path('accounts/', include(('django.contrib.auth.urls','django.contrib.auth'), namespace='auth'), name="signin"),
    path('accounts/password_change/',TemplateView.as_view(template_name="registration/password_change_form.html"), name="password_change"),
    path('password-done', TemplateView.as_view(template_name="registration/password_change_done.html"), name="password_change_done"),
    path('grappelli/', include('grappelli.urls')),
    path('request-user/', request_user, name='request-user'),
	path('password_reset/',auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
	path('topics/', get_topics),
    path('search/', PodcastSearch.as_view()),
    path('search/auto/', autocomplete),
    path('podcast/<pk>', PodcastView.as_view()),
	path('annotate/<podcast_id>', get_podcast),
    path('about', TemplateView.as_view(template_name='podcast/about.html'), name='about')

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
