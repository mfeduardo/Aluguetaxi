# Generated by Django 3.2.6 on 2021-09-27 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0018_anuncio_mensagens_idfk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensagem',
            name='conversa',
        ),
        migrations.AddField(
            model_name='mensagem',
            name='conversa_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
