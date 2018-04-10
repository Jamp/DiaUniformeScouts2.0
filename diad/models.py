# -*- coding: utf-8 -*-
import os
import logging
from PIL import Image
from django.conf import settings
from django.db import models
from django.core.signals import request_finished
from django.db.models.signals import post_save
from datetime import datetime
from twython import Twython
from facebook import GraphAPI
from PIL import Image
import urllib, cStringIO

import cloudinary
import cloudinary.uploader
import cloudinary.api

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

descripcion = 'Nueva imagen subida a http://uniforme.scout.org.ve, \
Celebrando el orgullo de ser Scout #DiadelUniformeScout'

# Create your models here.
class Album(models.Model):
    album = models.IntegerField()
    url = models.ImageField(upload_to=settings.APP_NAME+'/static/img/portada', max_length=250)
    creado_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albumes'

class Fotos(models.Model):
    album = models.IntegerField()
    url = models.ImageField(upload_to=settings.APP_NAME+'/static/img/album/%Y', max_length=250)
    autorizado = models.BooleanField(default=False)
    creado_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'

def Redimensionar(uri):
    uri = os.path.join(settings.BASE_DIR, uri)
    size = 450, 350

    try:
        im = Image.open(uri)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(uri, "JPEG")

        # FIXME: Pasar esto a clase a parte y parametrizar el folder en cloudinary
        # Moviendo a cloudinary
        cloudinary.config(
          cloud_name = settings.CL_NAME,
          api_key = settings.CL_API,
          api_secret = settings.CL_SECRET
        )
        return cloudinary.uploader.upload(uri, folder="diadeluniforme/2017")
    except IOError:
        pass

def PrepararURL(instancia):
    if str(instancia.url).find(settings.APP_NAME) == -1 or str(instancia.url).find('cloudinary.com'):
        pass
    else:
        instancia.url = str(instancia.url).replace(settings.APP_NAME, '')
        instancia.save()

# TODO: subir estás imágenes a cloudinary igual que lo hago con las fotos
def PostAlbum(sender, instance, **kwargs):
    post_save.disconnect(PostAlbum, sender=Album, dispatch_uid="prepare_album_url")

    url = str(instance.url)
    Redimensionar(url)
    PrepararURL(instance)

    post_save.connect(PostAlbum, sender=Album, dispatch_uid="prepare_album_url")

def PostFotos(sender, instance, **kwargs):
    # FIXME: Refactorizar este código, sobre todo el enviar las imagenes a cloudinary
    post_save.disconnect(PostFotos, sender=Fotos, dispatch_uid="prepare_fotos_url")

    url = str(instance.url)

    if str(url).find('cloudinary.com') == -1 :
        cloud = Redimensionar(url)
        instance.url = str(cloud['url'])

    instance.save()

    if instance.autorizado and instance.album == datetime.now().year:
        uri = str(url)
        PublicarTwitter(uri)
        PublicarFacebook(uri)

    post_save.connect(PostFotos, sender=Fotos, dispatch_uid="prepare_fotos_url")

def PublicarTwitter(uri):
    try:
        twitter = Twython(settings.TW_KEY, settings.TW_SECRET, settings.TW_TOKEN, settings.TW_TOKEN_SECRET)

        image_from_url = cStringIO.StringIO(urllib.urlopen(uri).read())

        image_id = twitter.upload_media(media=image_from_url)
        twitter.update_status(status=descripcion, media_ids=image_id['media_id'])
    except Exception, e:
        logging.error(e)

def PublicarFacebook(uri):
    try:
        api = GraphAPI(settings.FB_TOKEN)

        image_from_url = cStringIO.StringIO(urllib.urlopen(uri).read())

        api.put_photo(image_from_url, message=descripcion)
    except Exception, e:
        logging.error(e)

post_save.connect(PostAlbum, sender=Album, dispatch_uid="prepare_album_url")
post_save.connect(PostFotos, sender=Fotos, dispatch_uid="prepare_fotos_url")
