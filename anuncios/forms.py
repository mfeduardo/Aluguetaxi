from django import forms
#from django.forms.forms import Form

from .models import Anuncio, AnuncioFoto, AnuncioCidade, Conversa, Mensagem
from django.contrib.auth import get_user_model

class AnuncioForm(forms.ModelForm):
    class Meta:
        model=Anuncio
        fields=[
        'marca_id',
        'modelo', 
        'ano', 
        'cambio',
        'combustivel',
        'gas',
        'seguro',
        'valor',
        'image',
        'comentario',
       ]    

class AnuncioFotoForm(forms.ModelForm):
    #id_anuncio=forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model=AnuncioFoto
        fields=[
        'image',
        ]

class AnuncioCidadeForm(forms.ModelForm):
    class Meta:
        model=AnuncioCidade
        fields=[
        'cidade',
        'cidade_id',
        'uf',
        'uf_id',
        ]
class ConversaForm(forms.ModelForm):
    class Meta:
        model=Conversa
        fields='__all__'

class MensagemForm(forms.ModelForm):
    class Meta:
        model=Mensagem
        fields='__all__'