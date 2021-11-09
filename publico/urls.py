from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('politica/', views.politica, name='politica'),
    path('comofunciona/', views.comoFunciona, name='comofunciona'),
    path('termos/', views.termos, name='termos'),
    path('regras/', views.regras, name='regras'),
    path('contato/', views.contato, name='contato'),
    path('logout_page', views.logout_page, name='logout-page'),     
]