import os
import logging
from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from datetime import datetime
from twython import Twython
from facebook import GraphAPI

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
    except IOError:
        pass

def PrepararURL(instancia):
    if str(instancia.url).find(settings.APP_NAME) == -1:
        pass
    else:
        instancia.url = str(instancia.url).replace(settings.APP_NAME, '')
        instancia.save()

def PostAlbum(sender, instance, **kwargs):
    url = str(instance.url)
    Redimensionar(url)
    PrepararURL(instance)

def PostFotos(sender, instance, **kwargs):
    url = str(instance.url)

    Redimensionar(url)
    PrepararURL(instance)

    if instance.autorizado and instance.album == datetime.now().year:
        uri = os.path.join(settings.BASE_DIR,settings.APP_NAME)+url
        PublicarTwitter(uri)
        PublicarFacebook(uri)


def PublicarTwitter(uri):
    try:
        twitter = Twython(settings.TW_KEY, settings.TW_SECRET, settings.TW_TOKEN, settings.TW_TOKEN_SECRET)

        image_id = twitter.upload_media(media=open(uri, 'rb'))
        twitter.update_status(status=descripcion, media_ids=image_id['media_id'])
    except Exception, e:
        logging.error(e)

def PublicarFacebook(uri):
    try:
        api = GraphAPI(settings.FB_TOKEN)

        api.put_photo(open(uri,"rb"), message=descripcion)
    except Exception, e:
        logging.error(e)

post_save.connect(PostAlbum, sender=Album, dispatch_uid="prepare_album_url")
post_save.connect(PostFotos, sender=Fotos, dispatch_uid="prepare_fotos_url")
