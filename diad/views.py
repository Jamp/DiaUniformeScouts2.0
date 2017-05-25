# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template.context import RequestContext
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import Album, Fotos
from forms import UploadForm
from datetime import datetime
from django.conf import settings
from twython import Twython
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
    photos = Fotos.objects.all().filter(album=id_album, autorizado=True).order_by('-id')[0:5]

    message = messages.get_messages(request)

    all = len(Fotos.objects.all().filter(album=id_album, autorizado=True))
    next = False
    if all > 5:
        next = True

    ## FIXME: Permitir que el inicie el día del uniforme y este abierto una semana
    active = True

    ## TODO: Convertir en una opción para ser manejada por el panel y no HardCoding
    if datetime.now().strftime('%d/%m/%Y') == '24/05/2017':
        active = True

    template = 'index.html'
    return render(request, template, locals())

def album(request, id_album):

    current = datetime.now().year
    id_album = int(id_album)

    albums = Album.objects.all().order_by('-album')
    photos = Fotos.objects.all().filter(album=id_album, autorizado=True).order_by('-id')[0:5]

    all = len(Fotos.objects.all().filter(album=id_album, autorizado=True))
    next = False
    if all > 5:
        next = True

    template = 'album.html'
    return render(request, template, locals())

def subir(request):
    try:
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                NewPhoto = Fotos(album=request.POST['album'], url=request.FILES['url'])
                NewPhoto.save()
                messages.success(request, 'Imagen subida exitosamente!!! Por favor espere que nuestros administradores la aprueben para que pueda verla publicada')
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

    photos = Fotos.objects.all().filter(album=id_album, autorizado=True).order_by('-id')[inicio:final]

    output = []
    for photo in photos:
        item = {
            'id': photo.id,
            'url': str(photo.url),
            'creado_at': photo.creado_at.strftime('%d/%m/%Y %H:%M')
        }
        output.append(item)

    if len(photos) == 0:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    return JsonResponse({'photos': output})


## Get Token FB/Twitter
def twitter_token(request):
    ## Tomamos el absolute path de donde esta corriendo
    callback = request.build_absolute_uri()


    if request.GET:
        auth = request.session['twitter_auth']
        ttoken = auth['oauth_token']
        tsecret = auth['oauth_token_secret']

        verifier = request.GET['oauth_verifier']

        twitter = Twython(settings.TW_KEY, settings.TW_SECRET, ttoken, tsecret)

        oauth = twitter.get_authorized_tokens(verifier)

        token = oauth['oauth_token']
        secret = oauth['oauth_token_secret']
    else:
        twitter = Twython(settings.TW_KEY, settings.TW_SECRET)
        ## Se arma la URL para autenticar
        auth = twitter.get_authentication_tokens(callback_url=callback)
        url = auth['auth_url']
        request.session['twitter_auth'] = auth

    template = 'twitter_token.html'
    return render(request, template, locals())

def facebook_token(request):
    ## Tomamos el absolute path de donde esta corriendo
    callback = request.build_absolute_uri()

    if request.GET:
        code = request.GET['code']

        ## Con el Code que recibimos de FB solicitamos un Access Token temporal
        params = facebook.GraphAPI().get_access_token_from_code(code, callback, settings.FB_API, settings.FB_SECRET)

        ## Solicitamos el un Access Token "Permanente" 2 Meses aproximadamente
        arg = {
            'grant_type': 'fb_exchange_token',
            'client_id': settings.FB_API,
            'client_secret': settings.FB_SECRET,
            'fb_exchange_token': params['access_token']
        }
        req = requests.request("GET","https://graph.facebook.com/oauth/access_token", params=arg).json()

        token = req['access_token']
        expires = req['expires_in']
    else:
        ## Se arma la URL para autenticar
        url = facebook.auth_url(settings.FB_API, callback, ['user_about_me','user_photos','publish_actions'])

    template = 'facebook_token.html'
    return render(request, template, locals())
