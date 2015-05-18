from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import Album, Fotos
from forms import UploadForm
from datetime import datetime
import simplejson


import logging
logger = logging.getLogger(__name__)


def home(request, id_album=None):

    if not id_album:
        id_album = datetime.now().year
    else:
        id_album = int(id_album)

    albums = Album.objects.all().order_by('-album')
    photos = Fotos.objects.all().filter(album=id_album).order_by('-creado_at')[0:5]

    message = messages.get_messages(request)

    all = len(Fotos.objects.all().filter(album=id_album))
    next = False
    if all > 5:
        next = True

    template = 'index.html'
    return render_to_response(template,context_instance=RequestContext(request,locals()))

def album(request, id_album):

    current = datetime.now().year
    id_album = int(id_album)

    albums = Album.objects.all().order_by('-album')
    photos = Fotos.objects.all().filter(album=id_album).order_by('-creado_at')[0:5]

    all = len(Fotos.objects.all().filter(album=id_album))
    next = False
    if all > 5:
        next = True

    print(locals())

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
