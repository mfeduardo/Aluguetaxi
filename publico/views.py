from django.shortcuts import render, redirect
#from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from anuncios.models import AnuncioCidade
from django.contrib.auth import logout

def index(request):
    cidades = AnuncioCidade.objects.order_by('uf','cidade')
    searchbox=True
    return render(request, 'publico/index.html', { 'cidades': cidades, 'searchbox': searchbox})

def politica(request):
    return render(request, 'publico/politica.html')

def termos(request):
    return render(request, 'publico/termos.html')

def regras(request):
    return render(request, 'publico/regras.html')

def contato(request):

    if request.method == 'POST':
        
        nome = request.POST['nome']
        email = request.POST['email']
        assunto = 'AlugueTáxi | '+ request.POST['assunto'] + ' (Fale Conosco)'
        mensagem = request.POST['mensagem']
        text_content = mensagem
        html_content = '<strong><span style="color: #BDBDBD;">ALUGUE</span><span class="at" style="color: #FBC02D;">TÁXI</span></strong><br><br>' + mensagem + '<br><br>' + 'De: ' + nome + '<br>Email: ' + email
        
        msg = EmailMultiAlternatives(assunto, text_content, 'contato@aluguetaxi.com.br', ['contato@aluguetaxi.com.br'])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        #send_mail (
        #    assunto, menssagem, 
         #   email,#settings.EMAIL_HOST_USER,

          #  ['contato@aluguetaxi.com'], 
          #  fail_silently=True)

    return render(request, 'publico/contato.html')

def comoFunciona(request):
    return render(request, 'publico/comofunciona.html')

def logout_page(request):
    logout(request)
    return redirect ('/accounts/login')

def erro404(request, exception):
    return render(request, 'publico/404.html')

def erro500(request):
    return render(request, 'publico/500.html')