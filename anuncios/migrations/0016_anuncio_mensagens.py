# Generated by Django 3.2.6 on 2021-09-22 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0015_anuncio_mensagens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensagem',
            name='conversa_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
