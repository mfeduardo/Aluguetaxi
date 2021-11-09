import uuid
from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth import get_user_model
import json

#url=requests.get('https://parallelum.com.br/fipe/api/v1/carros/marcas/100/modelos')
#data = url.json()

#https://parallelum.com.br/fipe/api/v1/carros/marcas
#https://parallelum.com.br/fipe/api/v1/carros/marcas/[marca_id]/modelos

MARCAS_ID=[]

def marcas():
    with open('./publico/static/json/marcas.json', 'r', encoding='utf8') as arquivo:
        return json.load(arquivo)

m=marcas()
marcas_list = sorted(m, key=lambda k: k['nome'], reverse=False)

for m in marcas_list:
    marca=int(m['codigo']), m['nome']
    MARCAS_ID.append(marca)

#choices Ano
ANO = []

ano=1999
while ano<2025:
    ano+=1
    a=(ano,ano)
    ANO.append(a)

CAMBIO =[
    ('Automático', 'Automático'),
    ('Manual', 'Manual')
]

GAS =[
    (True, 'Sim'),
    (False, 'Não')
]

SEGURO =[
    (True, 'Sim'),
    (False, 'Não')
]

COMBUSTIVEL =[
    ('Gasolina', 'Gasolina'),
    ('Flex', 'Flex')
]

class Anuncio(models.Model):    
    #model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_usr = models.ForeignKey(get_user_model(), related_name='anuncios', on_delete=models.CASCADE)
    nome=models.CharField(max_length=150, blank=True, null=True)
    sobrenome=models.CharField(max_length=150, blank=True, null=True)
    telefone=models.CharField(max_length=20, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    marca_id = models.IntegerField(verbose_name='Marca', blank=False, null=True, choices=MARCAS_ID)
    modelo = models.CharField(max_length=60, blank=False, null=True)
    modelo_id = models.IntegerField(blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True, choices=ANO)
    cambio = models.CharField(max_length=15, blank=True, null=True, choices=CAMBIO)
    clique = models.IntegerField(blank=True, null=True, default=0)
    combustivel = models.CharField(max_length=15, blank=True, null=True, choices=COMBUSTIVEL)
    seguro = models.BooleanField(blank=True, null=True, choices=SEGURO)
    gas = models.BooleanField(blank=True, null=True, choices=GAS)
    status_contrato = models.BooleanField(blank=True, null=True)
    status_excluir = models.BooleanField(blank=True, null=True, default=False)
    tipo = models.CharField(max_length=20, blank=True, null=True, default="Carro") 
    valor = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    fotos = models.CharField(max_length=255, blank=True, null=True)
    fotos_nome = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name='Foto Principal do Anúncio (Capa)', upload_to="img_capa/%Y/%m/", blank=True)
    ipva_pago = models.BooleanField(blank=True, null=True, default=True)
    status_anuncio = models.BooleanField(blank=True, null=True, default=False)
    km = models.CharField(max_length=255, blank=True, null=True)
    anuncio_inicio = models.DateTimeField(blank=True, null=True, default='2021-09-19 00:36:08.101176-03')
    anuncio_fim = models.DateTimeField(blank=True, null=True, default='2021-09-19 00:36:08.101176-03')
    local = models.CharField(max_length=255, blank=True, null=True)
    local2 = models.CharField(max_length=255, blank=True, null=True)
    local_municipio = models.CharField(max_length=255, blank=True, null=True)
    local_municipio_id = models.IntegerField(blank=True, null=True)
    local_uf = models.CharField(max_length=2, blank=True, null=True)
    local_uf_nome = models.CharField(max_length=100, blank=True, null=True)
    local_uf_id = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    slug2 = AutoSlugField(unique=True, always_update=False, populate_from="modelo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    unique_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.modelo

class AnuncioFoto(models.Model):
    id_anuncio = models.ForeignKey(Anuncio, related_name='fotos_veiculos', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Foto do Veículo', upload_to="img_anuncios/%Y/%m/", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    id_usuario = models.CharField(get_user_model(), max_length=255)

    def __str__(self):
        return self.id_anuncio
    
class AnuncioCidade(models.Model):
    cidade = models.CharField(max_length=255, blank=True, null=True)
    cidade_id = models.IntegerField(blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    uf_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    id_usuario = models.CharField(get_user_model(), max_length=255)

    def __str__(self):
        return self.cidade    

class Conversa(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    anuncio_id = models.ForeignKey(Anuncio, related_name='conversa', on_delete=models.CASCADE)
    motorista_id = models.CharField(max_length=255, blank=True, null=True)
    motorista_nome = models.CharField(max_length=150, blank=True, null=True)
    motorista_sobrenome = models.CharField(max_length=150, blank=True, null=True)
    proprietario_id = models.CharField(max_length=255, blank=True, null=True)
    proprietario_nome = models.CharField(max_length=150, blank=True, null=True)
    proprietario_sobrenome = models.CharField(max_length=150, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.nome    

class Mensagem(models.Model):
    conversa_id = models.ForeignKey(Conversa, related_name='conversa_ref', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, blank=True, null=True)
    mensagem = models.TextField(blank=True, null=True)
    anuncio_id = models.CharField(max_length=150, blank=True, null=True)
    motorista_id = models.CharField(max_length=150, blank=True, null=True)
    motorista_nome = models.CharField(max_length=150, blank=True, null=True)
    motorista_sobrenome = models.CharField(max_length=150, blank=True, null=True)
    proprietario_id = models.CharField(max_length=150, blank=True, null=True)
    proprietario_nome = models.CharField(max_length=150, blank=True, null=True)
    proprietario_sobrenome = models.CharField(max_length=150, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True, default=True)
    criador = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
   
    
    def __str__(self):
        return self.nome    