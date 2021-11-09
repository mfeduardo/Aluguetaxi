from django.contrib import admin
from anuncios.models import Anuncio, AnuncioFoto


#admin.site.register(Anuncio)
@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ["__str__","email","local_municipio","local_uf"]
    #list_filter =[""]
    search_fields=["email"]
    
@admin.register(AnuncioFoto)
class AnuncioFotoAdmin(admin.ModelAdmin):
    list_display = ["__str__","id_anuncio_id","image","id_usuario"]


#class ItemInline(admin.TabularInline):
 #   model = Item
  #  raw_id_fields = ["modelo"]
 #  extra=0