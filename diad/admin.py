from django.contrib import admin
from models import Album, Fotos

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album', 'portada',)

    def portada(self, obj):
        url = obj.url
        return '<img src="%s">' % url

    portada.allow_tags = True

class FotosAdmin(admin.ModelAdmin):
    list_display = ('album', 'imagen', 'autorizado')

    def imagen(self, obj):
        url = obj.url
        return '<img src="%s">' % url

    imagen.allow_tags = True


admin.site.register(Album, AlbumAdmin)
admin.site.register(Fotos, FotosAdmin)
