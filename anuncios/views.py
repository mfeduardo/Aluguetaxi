from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Anuncio, AnuncioFoto, AnuncioCidade, Conversa, Mensagem
from .forms import AnuncioForm, AnuncioFotoForm, ConversaForm, MensagemForm
from django.contrib import messages
from datetime import datetime, timedelta
from pytz import timezone
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMultiAlternatives

SUCESSO = 50  # messages_tag

host = 'https://www.aluguetaxi.com.br'

fuso_horario = timezone('America/Sao_Paulo')


def verificaDataAnuncio(dataReferencia):

    dataVencimento = str(dataReferencia)
    dataVencimento = dataVencimento[0:10]

    dataAtual = str(datetime.now())
    dataAtual = dataAtual[0:10]

    dataAnuncio = datetime.strptime(
        dataVencimento, '%Y-%m-%d')+timedelta(days=1)
    dataHoje = datetime.strptime(dataAtual, '%Y-%m-%d')

    anuncioValido = dataAnuncio >= dataHoje
    print(dataVencimento, anuncioValido, dataAnuncio, dataHoje)

    return anuncioValido


def retornaData(dataReferencia):
    data = str(dataReferencia)
    data = data[0:10]
    data = data[8:10]+'/'+data[5:7]+'/'+data[0:4]

    return data

# Público


def anuncios(request):
    busca = request.GET.get('busca')

    anuncios = Anuncio.objects.order_by('-created_at').filter(local_municipio__icontains=busca).filter(
        status_excluir=False).filter(Q(anuncio_fim__date__range=(datetime.now(), datetime.now()+timedelta(days=15))))

    total = len(anuncios)

    return render(request, 'anuncios/anuncios.html', {'anuncios': anuncios, 'total': total, 'busca': busca})


def anuncioDetalhes(request, slug2):
    anuncio = get_object_or_404(Anuncio, slug2=slug2)

    if not(verificaDataAnuncio(anuncio.anuncio_fim)):
        return redirect('/anuncios/?busca='+anuncio.local_uf)

    img = anuncio.fotos_veiculos.all().order_by('created_at')
    msgs = ''
    total = 0
    if request.user.is_authenticated:
        conversaReferencia = Conversa.objects.order_by('created_at').filter(anuncio_id=anuncio.id).filter(
            motorista_id=request.user.email).filter(proprietario_id=anuncio.email).first()
        msgs = Mensagem.objects.order_by('-created_at').filter(anuncio_id=anuncio.id).filter(
            motorista_id=request.user.email).filter(proprietario_id=anuncio.email)
        total = len(msgs)
        print(type(total))
    if request.method == 'POST':

        if not(request.user.cpf or request.user.cidade):
            return redirect('/usuario/editar')

        form = ConversaForm(request.POST)

        if form.is_valid():

            def enviar_email():  # envia a mensagem par o email do proprietário
                mensagem_p1 = 'Existe uma nova mensagem no AlugueTáxi para você:<br><br>'
                mensagem_p2 = '<br><br>Observação: é preciso estar logado no site da AlugueTáxi para poder acessar a seção de mensagens!<br><br>Equipe AlugueTáxi'
                email = anuncio.email
                assunto = 'AlugueTáxi | Mensagem | ' + slug2 + ' | ' + request.user.first_name
                text_content = request.POST['mensagem']
                html_content = '<strong><span style="color: #BDBDBD;">ALUGUE</span><span class="at" style="color: #FBC02D;">TÁXI</span></strong><br><br>' + mensagem_p1 + \
                    '"' + request.POST['mensagem'] + '"<br><br>De: ' + request.user.first_name + \
                    '<br><br><a href="' + host + '/anuncio/mensagens">' + \
                    host + '/anuncio/mensagens</a>' + mensagem_p2
                msg = EmailMultiAlternatives(
                    assunto, text_content, 'contato@aluguetaxi.com.br', [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.add_message(
                    request, SUCESSO, 'Sua mensagem foi enviada com sucesso! Aguarde resposta do propietário do veículo!')
                messages.add_message(
                    request, SUCESSO, 'As perguntas também são enviadas para o e-mail do proprietário.')
                messages.add_message(
                    request, SUCESSO, 'A conversa é privada - não pode ser visualizada por outros usuários.')

            if conversaReferencia:  # Verifica se já existe a conversa
                form2 = MensagemForm()
                mensagem = form2.save(commit=False)
                mensagem.conversa_id_id = conversaReferencia.id
                mensagem.nome = anuncio.slug2
                mensagem.anuncio_id = anuncio.id
                mensagem.motorista_id = request.user.email
                mensagem.motorista_nome = request.user.first_name
                mensagem.motorista_sobrenome = request.user.last_name
                mensagem.proprietario_id = anuncio.email
                mensagem.proprietario_nome = anuncio.nome
                mensagem.proprietario_sobrenome = anuncio.sobrenome
                mensagem.criador = request.user.email
                mensagem.mensagem = request.POST['mensagem']
                mensagem.save()

                Conversa.objects.filter(id=conversaReferencia.id).update(
                    updated_at=datetime.now().astimezone(fuso_horario))

                enviar_email()

                return redirect('/anuncio/detalhes/'+anuncio.slug2)

            else:
                conversa = form.save(commit=False)
                conversa.nome = request.POST['nome']
                conversa.motorista_id = request.user.email
                conversa.motorista_nome = str.replace(
                    str(request.user.first_name), " ", "")
                conversa.motorista_sobrenome = str.replace(
                    str(request.user.last_name), " ", "")
                conversa.proprietario_nome = str.replace(
                    str(anuncio.nome), " ", "")
                conversa.proprietario_sobrenome = str.replace(
                    str(anuncio.sobrenome), " ", "")
                conversa.save()

                form2 = MensagemForm()
                mensagem = form2.save(commit=False)
                mensagem.conversa_id_id = Conversa.objects.latest('pk').pk
                mensagem.nome = anuncio.slug2
                mensagem.anuncio_id = anuncio.id
                mensagem.motorista_id = request.user.email
                mensagem.motorista_nome = request.user.first_name
                mensagem.motorista_sobrenome = request.user.last_name
                mensagem.proprietario_id = anuncio.email
                mensagem.proprietario_nome = anuncio.nome
                mensagem.proprietario_sobrenome = anuncio.sobrenome
                mensagem.criador = request.user.email
                mensagem.mensagem = request.POST['mensagem']
                mensagem.save()

                enviar_email()

                return redirect('/anuncio/detalhes/'+anuncio.slug2)

    else:
        form = ConversaForm()
        Anuncio.objects.filter(id=anuncio.id).update(clique=anuncio.clique+1)
        return render(request, "anuncios/anuncio_detalhes.html", {'anuncio': anuncio, 'img': img, 'form': form, 'msgs': msgs, 'total': total})

# Usuários


@login_required
def anuncioLista(request):
    anuncios = Anuncio.objects.order_by(
        '-created_at').filter(id_usr=request.user)
    total = anuncios.count()
    data = datetime.now().astimezone(fuso_horario)

    return render(request, 'anuncios/anuncio_lista.html', {'anuncios': anuncios, 'total': total, 'data': data})


@login_required
def anuncioNovo(request):

    if not(request.user.cpf or request.user.cidade):
        return redirect('/usuario/editar')

    if request.method == 'POST':
        form = AnuncioForm(request.POST, request.FILES)

        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.id_usr = request.user
            anuncio.local_uf = request.user.uf
            anuncio.local_municipio = request.user.cidade
            anuncio.email = request.user.email
            anuncio.nome = request.user.first_name
            anuncio.sobrenome = request.user.last_name
            anuncio.telefone = request.user.telefone
            anuncio.marca = request.POST['marca']
            anuncio.save()

            # Verifica se a Cidade já está cadastrada
            municipio = AnuncioCidade.objects.filter(
                cidade=request.user.cidade).first()

            if not municipio:
                # Cadastra nova cidade
                AnuncioCidade.objects.create(
                    cidade=request.user.cidade, uf=request.user.uf, id_usuario=request.user.email)

            messages.info(
                request,  'Anúncio cadastrado com sucesso: ' + anuncio.modelo)
            return redirect('/anuncio/lista')
    else:
        form = AnuncioForm()
        return render(request, 'anuncios/anuncio_novo.html', {'form': form})


@login_required
def anuncioInfo(request, slug2):
    anuncio = get_object_or_404(Anuncio, slug2=slug2)
    img = anuncio.fotos_veiculos.all().order_by('created_at')
    conversaReferencia = anuncio.conversa.all().order_by('-updated_at')
    msgs = Mensagem.objects.order_by('created_at').filter(
        anuncio_id=anuncio.id).filter(proprietario_id=anuncio.email)
    total = len(conversaReferencia)

    if anuncio.id_usr == request.user:

        if request.method == 'POST':

            form = ConversaForm(request.POST)

            if form.is_valid():
                form2 = MensagemForm()
                mensagem = form2.save(commit=False)
                mensagem.conversa_id_id = int(request.POST['conversa_id'])
                mensagem.nome = anuncio.slug2
                mensagem.anuncio_id = anuncio.id
                mensagem.motorista_id = request.POST['motorista_id']
                mensagem.motorista_nome = request.POST['motorista_nome']
                mensagem.motorista_sobrenome = request.POST['motorista_sobrenome']
                mensagem.proprietario_id = request.user.email
                mensagem.proprietario_nome = request.user.first_name
                mensagem.proprietario_sobrenome = request.user.last_name
                mensagem.criador = request.user.email
                mensagem.mensagem = request.POST['mensagem']
                mensagem.save()

                Conversa.objects.filter(id=request.POST['conversa_id']).update(
                    updated_at=datetime.now().astimezone(fuso_horario))

                messages.add_message(
                    request, SUCESSO, 'Sua mensagem foi enviada com sucesso! Aguarde resposta do usuário!')
                messages.add_message(
                    request, SUCESSO, 'A conversa é privada - não pode ser visualizada por outros usuários.')
                messages.add_message(
                    request, SUCESSO, 'As perguntas e respostas também são enviadas para os respectivos e-mails.')

                # return render(request, "anuncios/anuncio_info.html", {'anuncio':anuncio, 'img':img, 'conversas': conversaReferencia, 'msgs': msgs, 'total': total})
                return redirect('/anuncio/info/' + anuncio.slug2)

        else:

            return render(request, "anuncios/anuncio_info.html", {'anuncio': anuncio, 'img': img, 'conversas': conversaReferencia, 'msgs': msgs, 'total': total})

    else:
        return redirect('/anuncio/lista')


@login_required
def anuncioEditar(request, slug2):
    anuncio = get_object_or_404(Anuncio, slug2=slug2)
    form = AnuncioForm(instance=anuncio)

    if request.method == 'POST':

        form = AnuncioForm(request.POST, request.FILES, instance=anuncio)

        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.marca = request.POST['marca']
            anuncio.local_uf = request.user.uf
            anuncio.local_municipio = request.user.cidade
            anuncio.save()
            messages.info(request,  'Anúncio atualizado com sucesso: ' +
                          anuncio.marca + ' ' + anuncio.modelo)
            return redirect('/anuncio/info/' + anuncio.slug2)
        else:
            return render(request, "anuncios/anuncio_editar.html", {'form': form, 'anuncio': anuncio})

    else:

        if anuncio.id_usr == request.user:
            return render(request, "anuncios/anuncio_editar.html", {'form': form, 'anuncio': anuncio})
        else:
            return redirect('/anuncio/lista')


@login_required
def anuncioMensagens(request):

    if not(request.user.cpf or request.user.cidade):
        return redirect('/usuario/editar')

    conversas = Conversa.objects.annotate(search=SearchVector(
        'proprietario_id', 'motorista_id')).filter(search=request.user.email).order_by('-updated_at')
    msgs = Mensagem.objects.annotate(search=SearchVector('proprietario_id', 'motorista_id')).filter(
        search=request.user.email).order_by('created_at')
    total = len(conversas)
    # total_msgs_nao_lidas=len(msgs.filter(status=False))

    if request.method == 'POST':

        form = MensagemForm(request.POST)

        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.conversa_id_id = request.POST['conversa_id']
            mensagem.nome = request.POST['nome']
            mensagem.anuncio_id = request.POST['anuncio_id']
            mensagem.motorista_id = request.POST['motorista_id']
            mensagem.motorista_nome = request.POST['motorista_nome']
            mensagem.motorista_sobrenome = request.POST['motorista_sobrenome']
            mensagem.proprietario_id = request.POST['proprietario_id']
            mensagem.proprietario_nome = request.POST['proprietario_nome']
            mensagem.proprietario_sobrenome = request.POST['proprietario_sobrenome']
            mensagem.criador = request.user.email
            mensagem.mensagem = request.POST['mensagem']
            mensagem.save()

            Conversa.objects.filter(id=request.POST['conversa_id']).update(
                updated_at=datetime.now().astimezone(fuso_horario))

            # envia_email
            if (mensagem.criador == mensagem.motorista_id):
                email = mensagem.proprietario_id
            else:
                email = mensagem.motorista_id

            mensagem_p1 = 'Existe uma nova mensagem no AlugueTáxi para você:<br><br>'
            mensagem_p2 = '<br><br>Observação: é preciso estar logado no site da AlugueTáxi para poder acessar a seção de mensagens!<br><br>Equipe AlugueTáxi'
            assunto = 'AlugueTáxi | Mensagem | ' + \
                mensagem.nome + ' | ' + request.user.first_name
            text_content = request.POST['mensagem']
            html_content = '<strong><span style="color: #BDBDBD;">ALUGUE</span><span class="at" style="color: #FBC02D;">TÁXI</span></strong><br><br>' + mensagem_p1 + \
                '"' + request.POST['mensagem'] + '"<br><br>De: ' + request.user.first_name + \
                '<br><br><a href="' + host + '/anuncio/mensagens">' + \
                host + '/anuncio/mensagens</a>' + mensagem_p2
            msg = EmailMultiAlternatives(
                assunto, text_content, 'contato@aluguetaxi.com.br', [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.add_message(
                request, SUCESSO, 'Sua mensagem foi enviada com sucesso! Aguarde resposta do usuário!')
            messages.add_message(
                request, SUCESSO, 'As perguntas também são enviadas para o e-mail do usuário.')

            # return render(request, "anuncios/anuncio_info.html", {'anuncio':anuncio, 'img':img, 'conversas': conversaReferencia, 'msgs': msgs, 'total': total})
            return render(request, 'anuncios/anuncios_mensagens.html', {'conversas': conversas, 'msgs': msgs, 'total': total})

    else:

        return render(request, 'anuncios/anuncios_mensagens.html', {'conversas': conversas, 'msgs': msgs, 'total': total})


@login_required
def anuncioExluir(request, slug2):
    anuncio = get_object_or_404(Anuncio, slug2=slug2)
    anuncio.delete()

    messages.info(request,  'Este anúncio foi deletado: ' +
                  anuncio.marca + ' ' + anuncio.modelo)

    return redirect('/anuncio/lista')


@login_required
def fotoExluir(request, slug2, id):
    anuncio = Anuncio.objects.all().filter(slug2=slug2).first()
    foto = get_object_or_404(AnuncioFoto, pk=id)

    if foto.id_usuario == str(request.user.id):
        foto.delete()
        messages.info(request,  'Foto excluída para este anúncio: ' +
                      anuncio.marca + ' ' + anuncio.modelo)
    else:
        messages.info(request,  'Não foi possível excluir esta foto!')

    return redirect('/anuncio/fotos/' + slug2)


@login_required
def uploadFotos(request, slug2):
    anuncio = Anuncio.objects.all().filter(slug2=slug2).first()
    if (anuncio.id_usr == request.user):
        img = anuncio.fotos_veiculos.all().order_by('created_at')

        if request.method == 'POST':
            form = AnuncioFotoForm(request.POST, request.FILES)

            if form.is_valid():
                anuncio_foto = form.save(commit=False)
                anuncio_foto.id_anuncio_id = anuncio.id
                anuncio_foto.id_usuario = request.user.id
                anuncio_foto.save()
                messages.info(request, 'Foto cadastrado com sucesso para o anúncio: ' +
                              anuncio.marca + ' ' + anuncio.modelo)
                return render(request, 'anuncios/anuncio_upfoto.html', {'form': form, 'anuncio': anuncio, 'img': img})
        else:
            form = AnuncioFotoForm()
            return render(request, 'anuncios/anuncio_upfoto.html', {'form': form, 'anuncio': anuncio, 'img': img})
    else:
        return redirect('/anuncio/lista')


@login_required
def anuncioAtivar(request, slug2):
    # Ativar Promoção
    anuncio = get_object_or_404(Anuncio, slug2=slug2)

    if (anuncio.id_usr == request.user):
        # Verifica se já tem mais de 30 dias desde a última promoção
        data_ref = datetime.now().astimezone(fuso_horario) - anuncio.anuncio_fim
        promo = timedelta(days=30) - (data_ref)

        if data_ref > timedelta(days=30):

            anuncio.anuncio_inicio = datetime.now().astimezone(fuso_horario)
            anuncio.anuncio_fim = datetime.now().astimezone(fuso_horario)+timedelta(days=7)
            anuncio.save()

            data_inicio = retornaData(anuncio.anuncio_inicio)
            data_fim = retornaData(anuncio.anuncio_fim)

            mensagem_p1 = 'Olá, a sua promoção mensal de anúncio foi ativada <strong>(7 dias grátis)!</strong><br><br>' + '- Período de exibição do anúncio: de ' + data_inicio + ' - ' + data_fim + \
                '<br><br>- Seus anúncios podem ser renovados para um novo período de 15 dias, sempre que você precisar. Basta ir na sessão Meus Anúncios do nosso site e reativar qualquer anúncio cadastrado anteriormente, mediante pagamento de uma nova taxa de R$ 15,00 (valor atual) por anúncio.'
            mensagem_p2 = '<br><br>- As informações cadastradas para o seu anúncio podem ser editadas a qualquer tempo, sempre que você achar necessário, basta ir na sessão Meus Anúncios do nosso site.<br><br>- Link para o seu anúncio: <a href="' + host + '/anuncio/detalhes/' + slug2 + '">' + host + '/anuncio/detalhes/' + \
                slug2 + '</a><br><br>Agradecemos por utilizar nossos serviços,<br><br>Equipe AlugueTáxi.'

            email = request.user.email
            assunto = 'AlugueTáxi | Promoção Mensal Ativada | ' + slug2
            text_content = mensagem_p1 + mensagem_p2
            html_content = '<strong><span style="color: #BDBDBD;">ALUGUE</span><span class="at" style="color: #FBC02D;">TÁXI</span></strong><br><br>' + mensagem_p1 + mensagem_p2

            msg = EmailMultiAlternatives(
                assunto, text_content, 'contato@aluguetaxi.com.br', [email], ['duda604@hotmail.com', 'mf.eduardo@yahoo.com'])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            #message1 = (assunto, 'Existe uma nova promoção para sua região', 'contato@aluguetaxi.com.br', ['duda604@gmail.com'])
            #message2 = (assunto, 'Existe uma nova promoção para sua região', 'contato@aluguetaxi.com.br', ['duda604@hotmail.com'], ['duda@hotmail.com'])
            #send_mass_mail((message1, message2), fail_silently=False)

            # datatuple = (
            #(assunto, 'Existe uma nova promoção para sua região', 'contato@aluguetaxi.com.br', ['duda604@gmail.com']),
            #(assunto, 'Existe uma nova promoção para sua região', 'contato@aluguetaxi.com.br', ['duda604@hotmail.com']),
            # )
            # send_mass_mail(datatuple)

            messages.info(request,  anuncio.marca + ' ' + anuncio.modelo +
                          ' | Período do Anúncio: ' + data_inicio + ' - ' + data_fim)

        else:
            messages.info(request, anuncio.marca + ' ' + anuncio.modelo + ' | Anúncio fora do período de promoção! Próxima Promoção: ' +
                          retornaData(datetime.now().astimezone(fuso_horario)+promo+timedelta(days=1)))
            return redirect('/anuncio/lista')

    return redirect('/anuncio/lista')
