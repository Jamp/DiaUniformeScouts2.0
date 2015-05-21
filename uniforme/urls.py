"""uniforme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'diad.views.home', name='home'),
    url(r'^(\d+)$', 'diad.views.home', name='home'),

    url(r'^subir/$', 'diad.views.subir', name='subir'),

    url(r'^album/(\d+)$', 'diad.views.album', name='album'),

    url(r'^pagina/$', 'diad.views.paginar', name='paginar'),
    url(r'^pagina/(\d+)$', 'diad.views.paginar', name='paginar'),
    url(r'^pagina/(\d+)/(\d+)$', 'diad.views.paginar', name='paginar'),

    url(r'^facebook/$', 'diad.views.facebook_token', name='facebook_token'),
    url(r'^twitter/$', 'diad.views.twitter_token', name='twitter_token'),


    url(r'^admin/', include(admin.site.urls)),
]
