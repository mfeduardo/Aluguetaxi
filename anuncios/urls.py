from django.urls import path

from . import views

urlpatterns = [
     path('anuncios/', views.anuncios, name='anuncios'),
     path('anuncio/lista', views.anuncioLista, name='anuncio-lista'),
     path('anuncio/novo', views.anuncioNovo, name='anuncio-novo'),
     path('anuncio/info/<str:slug2>', views.anuncioInfo, name='anuncio-info'),
     path('anuncio/detalhes/<str:slug2>', views.anuncioDetalhes, name='anuncio-detalhes'),
     path('anuncio/editar/<str:slug2>', views.anuncioEditar, name='anuncio-editar'),
     path('anuncio/excluir/<str:slug2>', views.anuncioExluir, name='anuncio-excluir'),
     path('anuncio/fotos/<str:slug2>', views.uploadFotos, name='anuncio-fotos'),
     path('anuncio/fotos/<str:slug2>/<int:id>', views.fotoExluir, name='foto-excluir'),
     path('anuncio/ativar/<str:slug2>', views.anuncioAtivar, name='anuncio-ativar'),
     path('anuncio/mensagens', views.anuncioMensagens, name='anuncio-mensagens'),     
]