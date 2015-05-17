import os
from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

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

def Redimensionar(URL):
    URI = os.path.join(settings.BASE_DIR, str(URL))
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
    Redimensionar(instance.url)
    PrepararURL(instance)

def PostFotos(sender, instance, **kwargs):
    Redimensionar(instance.url)
    PrepararURL(instance)
    if instance.autorizado:
        PublicarTwitter(instance)
        PublicarFacebook(instance)

def PublicarTwitter(instancia):
    pass

def PublicarFacebook(instancia):
    pass

post_save.connect(PostAlbum, sender=Album, dispatch_uid="prepare_album_url")
post_save.connect(PostFotos, sender=Fotos, dispatch_uid="prepare_fotos_url")