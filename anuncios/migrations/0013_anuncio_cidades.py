# Generated by Django 3.2.6 on 2021-09-21 14:58

from django.db import migrations, models
import usuarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0012_anuncio_dados_contato'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnuncioCidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidade', models.CharField(blank=True, max_length=255, null=True)),
                ('cidade_id', models.IntegerField(blank=True, null=True)),
                ('uf', models.CharField(blank=True, max_length=2, null=True)),
                ('uf_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id_usuario', models.CharField(max_length=255, verbose_name=usuarios.models.Usuario)),
            ],
        ),
        migrations.AlterField(
            model_name='anuncio',
            name='image',
            field=models.ImageField(blank=True, upload_to='img_capa/%Y/%m/', verbose_name='Foto Principal do Anúncio (Capa)'),
        ),
    ]
