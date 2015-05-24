# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import Album, Fotos
from forms import UploadForm
from datetime import datetime
from django.conf import settings
from twython import Twython
import simplejson
import facebook
import requests


import logging
logger = logging.getLogger(__name__)


def home(request, id_album=None):

    if not id_album:
        id_album = datetime.now().year
    else:
        id_album = int(id_album)

    albums = Album.objects.all().order_by('-album')
    photos = Fotos.objects.all().filter(album=id_album, autorizado=True).order_by('-creado_at')[0:5]

    message = messages.get_messages(request)

    all = len(Fotos.objects.all().filter(album=id_album, autorizado=True))
    next = False
    if all > 5:
        next = True

    active = False
    ## TODO: Convertir en una opción para ser manejada por el panel y no HardCoding
    if datetime.now().strftime('%d/%m/%Y') == '28/05/2015':
        active = True

    template = 'index.html'
    return render_to_response(template,context_instance=RequestContext(request,locals()))

def album(request, id_album):

    current = datetime.now().year
    id_album = int(id_album)

    albums = Album.objects.all().order_by('-album')
    photos = Fotos.objects.all().filter(album=id_album, autorizado=True).order_by('-creado_at')[0:5]

    all = len(Fotos.objects.all().filter(album=id_album, autorizado=True))
    next = False
    if all > 5:
        next = True

    template = 'album.html'
    return render_to_response(template,context_instance=RequestContext(request,locals()))

def subir(request):

    try:
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                NewPhoto = Fotos(album=request.POST['album'], url=request.FILES['url'])
                NewPhoto.save(form)
                messages.success(request, 'Imagen subida exitosamente!!!')
            else:
                messages.error(request, 'Formato de archivo no aceptado')
        else:
            messages.error(request, 'Error al subir imagen')
    except Exception, e:
        logger.debug(e)
        messages.error(request, 'Error al subir imagen')

    return HttpResponseRedirect(reverse('home'))

def paginar(request, pagina='2', id_album=None):
    pagina = int(pagina)

    if not id_album:
        id_album = datetime.now().year

    inicio = (6 * (pagina - 1)) - 1
    final = inicio + 6
    if pagina == 1:
        inicio = 0
        final = 5

    photos = Fotos.objects.all().filter(album=id_album).order_by('-creado_at')[inicio:final]

    output = []
    for photo in photos:
        item = {}
        item['url'] = str(photo.url)
        item['creado_at'] = photo.creado_at.strftime('%d/%m/%Y %H:%M')
        output.append(item)

    if len(photos) == 0:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return HttpResponse(simplejson.dumps(output), content_type="application/json")


## Get Token FB/Twitter
def twitter_token(request):
    ## Tomamos el absolute path de donde esta corriendo
    callback = request.build_absolute_uri()


    if request.GET:
        auth = request.session['twitter_auth']
        token = auth['oauth_token']
        secret = auth['oauth_token_secret']
    else:
        twitter = Twython(settings.TW_KEY, settings.TW_SECRET)
        ## Se arma la URL para autenticar
        auth = twitter.get_authentication_tokens(callback_url=callback)
        url = auth['auth_url']
        request.session['twitter_auth'] = auth

    template = 'twitter_token.html'
    return render_to_response(template, locals())

def facebook_token(request):
    ## Tomamos el absolute path de donde esta corriendo
    callback = request.build_absolute_uri()

    if request.GET:
        code = request.GET['code']

        ## Con el Code que recibimos de FB solicitamos un Access Token temporal
        params = facebook.get_access_token_from_code(code, callback, settings.FB_API, settings.FB_SECRET)

        ## Solicitamos el un Access Token "Permanente" 2 Meses aproximadamente
        arg = {'grant_type': 'fb_exchange_token', 'client_id': settings.FB_API, 'client_secret': settings.FB_SECRET, 'fb_exchange_token': params['access_token']}
        req = requests.request("GET","https://graph.facebook.com/oauth/access_token", params=arg).text

        ## Carpinteria
        s = req.split('&')
        t, token = s[0].split('=')
        e, expires = s[1].split('=')
    else:
        ## Se arma la URL para autenticar
        url = facebook.auth_url(settings.FB_API, callback, ['user_about_me','user_photos','publish_actions'])

    template = 'facebook_token.html'
    return render_to_response(template, locals())
