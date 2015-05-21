import os
import logging
from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from twython import Twython
from facebook import GraphAPI

descripcion = 'Nueva imagen subida a http://uniforme.scoutsfalcon.org, Celebrando el orgullo de ser Scout #DiadelUniformeScout'

# Create your models here.
class Album(models.Model):
    album = models.IntegerField()
    url = models.ImageField(upload_to=settings.APP_NAME+'/static/img/portada/%Y')
    creado_at = models.DateTimeField(auto_now_add=True)

class Fotos(models.Model):
    url = models.ImageField(upload_to=settings.APP_NAME+'/static/img/album/%Y')
    album = models.IntegerField()
    autorizado = models.BooleanField(default=False)
    creado_at = models.DateTimeField(auto_now_add=True)

def Redimensionar(uri):
    size = 450, 350

    try:
        im = Image.open(URI)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(URI, "JPEG")
    except IOError:
        pass

def PrepararURL(instancia):
    if str(instancia.url).find(settings.APP_NAME) == -1:
        pass
    else:
        Redimensionar(instancia.url)
        instancia.url = str(instancia.url).replace(settings.APP_NAME, '')
        instancia.save()

def PostAlbum(sender, instance, **kwargs):
    uri = os.path.join(settings.BASE_DIR, str(instance.url))
    Redimensionar(uri)
    PrepararURL(instance)

def PostFotos(sender, instance, **kwargs):
    uri = os.path.join(settings.BASE_DIR, str(instance.url))

    Redimensionar(uri)
    PrepararURL(instance)

    if instance.autorizado:
        PublicarTwitter(uri)
        PublicarFacebook(uri)

def PublicarTwitter(uri):
    try:
        twitter = Twython(settings.TW_KEY, settings.TW_SECRET, settings.TW_TOKEN, settings.TW_TOKEN_SECRET)

        image_id = twitter.upload_media(media=open(uri, 'rb'))
        twitter.update_status(status=descripcion+' // @ScoutsFalcon @scoutsvenezuela', media_ids=image_id['media_id'])
    except Exception, e:
        logging.error(e)


def PublicarFacebook(uri):
    try:
        api = GraphAPI(settings.FB_TOKEN)

        api.put_photo(open(uri,"rb"), descripcion)
    except Exception, e:
        logging.error(e)

post_save.connect(PostAlbum, sender=Album, dispatch_uid="prepare_album_url")
post_save.connect(PostFotos, sender=Fotos, dispatch_uid="prepare_fotos_url")