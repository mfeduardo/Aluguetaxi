from django.db.models.fields.related_descriptors import create_forward_many_to_many_manager
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserChangeForm
from anuncios.models import Anuncio, AnuncioCidade

SUCESSO = 50 #messages_tag

@login_required
def usuarioInfo(request):
    usuario = request.user
    
    if not (request.user.cpf or request.user.cidade):
            messages.add_message (request, SUCESSO, 'Atualize suas informações de conta para poder cadastrar um anúncio ou trocar mensagens com outros usuários.')
    return render(request, "usuarios/usuario_info.html", { 'usuario': usuario  })

@login_required
def usuarioEditar(request):
    usuario = request.user
    form = UserChangeForm(instance=usuario)

    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=usuario)
        
        if form.is_valid():
            usuario.save()
            
            #Atualiza Cidade/UF para os anúncios do usuário
            Anuncio.objects.filter(id_usr=request.user.id).update(local_municipio=request.user.cidade, local_uf=request.user.uf)
            
            municipio=AnuncioCidade.objects.filter(cidade=request.user.cidade).first()
            #Verifica se a Cidade já está cadastrada na tabela de cidades               
            if not municipio:
                #Cadastra nova cidade
                AnuncioCidade.objects.create(cidade=request.user.cidade, uf=request.user.uf, id_usuario=request.user.email)      

            return redirect('/usuario/info/')
        else:
            return render(request, "usuarios/usuario_editar.html", { 'form': form, 'usuario': usuario })

    else:  
        if not (request.user.cpf or request.user.cidade):
            messages.add_message (request, SUCESSO, 'Atualize suas informações de conta para poder cadastrar um anúncio ou trocar mensagens com outros usuários.')
        return render(request, "usuarios/usuario_editar.html", { 'form': form, 'usuario': usuario })

