from django.db import models
import uuid, requests, json
from django.contrib.auth.models import AbstractUser
#choice UF
UF = []

def estados():
    with open('./publico/static/json/estados.json', 'r', encoding='utf8') as arquivo:
        return json.load(arquivo)

u=estados()
uf_list = sorted(u, key=lambda k: k['sigla'], reverse=False)

for u in uf_list:
    uf=(u['sigla'], u['sigla'])
    UF.append(uf)

#choice Cidades
CIDADES = []

url=requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios')
cidade = url.json()
cidade_list = sorted(cidade, key=lambda k: k['nome'], reverse=False)

for c in cidade_list:
    cidade=(c['nome'], c['nome'])
    CIDADES.append(cidade)


class Usuario(AbstractUser):
    
    #model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(unique=True, max_length=255)
    telefone = models.CharField(max_length=255, blank=False, null=True)
    telefone2 = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField(verbose_name='CPF',max_length=255, blank=False, null=True)
    licenca = models.CharField(max_length=255, blank=True, null=True)
    foto = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name='Imagem do Perfil', upload_to="images/%Y/%m/%d", blank=True)
    data_nascimento = models.DateField(blank=True, null=True)
    tipo_pessoa = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    admin = models.BooleanField(blank=True, null=True)
    nivel = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=False, null=True, choices=CIDADES)
    cidade_id = models.CharField(max_length=255, blank=True, null=True)
    uf_id = models.CharField(max_length=255, blank=True, null=True)
    uf = models.CharField(max_length=255, blank=False, null=True, choices=UF)
    uf_nome = models.CharField(max_length=255, blank=True, null=True)
    promo = models.BooleanField(blank=True, null=True)
    promo_extra = models.CharField(max_length=255, blank=True, null=True)
    contagem_anuncios = models.IntegerField(blank=True, null=True)
    lista_automoveis = models.CharField(max_length=255, blank=True, null=True)
    newsletter = models.BooleanField(blank=True, null=True)
    sobre = models.CharField(max_length=255, blank=True, null=True)
    zap = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
            return self.first_name

