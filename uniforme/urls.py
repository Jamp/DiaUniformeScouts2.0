from django.conf.urls import include, url
from django.contrib import admin
import diad.views

urlpatterns = [
    url(r'^$', diad.views.home, name='home'),
    url(r'^(\d+)$', diad.views.home, name='home'),

    url(r'^subir/$', diad.views.subir, name='subir'),

    url(r'^album/(\d+)$', diad.views.album, name='album'),

    url(r'^pagina/$', diad.views.paginar, name='paginar'),
    url(r'^pagina/(\d+)$', diad.views.paginar, name='paginar'),
    url(r'^pagina/(\d+)/(\d+)$', diad.views.paginar, name='paginar'),

    url(r'^facebook/$', diad.views.facebook_token, name='facebook_token'),
    url(r'^twitter/$', diad.views.twitter_token, name='twitter_token'),

    url(r'^admin/', include(admin.site.urls)),
]
