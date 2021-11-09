from django.urls import path

from . import views

urlpatterns = [
    path('usuario/info/', views.usuarioInfo, name='usuario-info'),
    path('usuario/editar/', views.usuarioEditar, name='usuario-editar'),
]