# Generated by Django 3.2.6 on 2021-08-05 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('marca', models.CharField(blank=True, max_length=100, null=True)),
                ('marca_id', models.IntegerField(blank=True, null=True)),
                ('modelo', models.CharField(blank=True, max_length=60, null=True)),
                ('modelo_id', models.IntegerField(blank=True, null=True)),
                ('ano', models.IntegerField(blank=True, null=True)),
                ('cambio', models.CharField(blank=True, max_length=15, null=True)),
                ('clique', models.IntegerField(blank=True, null=True)),
                ('combustivel', models.CharField(blank=True, max_length=15, null=True)),
                ('seguro', models.BooleanField(blank=True, null=True)),
                ('gas', models.BooleanField(blank=True, null=True)),
                ('status_contrato', models.BooleanField(blank=True, null=True)),
                ('status_excluir', models.BooleanField(blank=True, null=True)),
                ('tipo', models.CharField(blank=True, max_length=20, null=True)),
                ('valor', models.FloatField(blank=True, null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('fotos', models.CharField(blank=True, max_length=255, null=True)),
                ('fotos_nome', models.CharField(blank=True, max_length=255, null=True)),
                ('ipva_pago', models.BooleanField(blank=True, null=True)),
                ('status_anuncio', models.BooleanField(blank=True, null=True)),
                ('km', models.CharField(blank=True, max_length=255, null=True)),
                ('anuncio_inicio', models.DateTimeField(blank=True, null=True)),
                ('anuncio_fim', models.DateTimeField(blank=True, null=True)),
                ('local', models.CharField(blank=True, max_length=255, null=True)),
                ('local2', models.CharField(blank=True, max_length=255, null=True)),
                ('local_municipio', models.CharField(blank=True, max_length=255, null=True)),
                ('local_municipio_id', models.IntegerField(blank=True, null=True)),
                ('local_uf', models.CharField(blank=True, max_length=2, null=True)),
                ('local_uf_nome', models.CharField(blank=True, max_length=100, null=True)),
                ('local_uf_id', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('unique_id', models.CharField(blank=True, max_length=255, null=True)),
                ('id_usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
