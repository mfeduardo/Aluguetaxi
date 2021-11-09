# Generated by Django 3.2.6 on 2021-08-19 18:11

from django.db import migrations, models
import django.db.models.deletion
import usuarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0006_alter_anuncio_valor'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnuncioFoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='img_anuncios', verbose_name='Foto do Veículo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id_usuario', models.CharField(max_length=255, verbose_name=usuarios.models.Usuario)),
                ('id_anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos_veiculos', to='anuncios.anuncio')),
            ],
        ),
    ]
