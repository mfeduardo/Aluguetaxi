# Generated by Django 3.2.6 on 2021-09-30 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_anuncio_conversa_nomes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(max_length=255, null=True, verbose_name='CPF'),
        ),
    ]
