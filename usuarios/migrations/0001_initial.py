# Generated by Django 3.2.6 on 2021-08-04 21:31

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('sobrenome', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('telefone', models.CharField(blank=True, max_length=255, null=True)),
                ('telefone2', models.CharField(blank=True, max_length=255, null=True)),
                ('cpf', models.CharField(blank=True, max_length=255, null=True)),
                ('licenca', models.CharField(blank=True, max_length=255, null=True)),
                ('foto', models.CharField(blank=True, max_length=255, null=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('tipo_pessoa', models.CharField(blank=True, max_length=255, null=True)),
                ('categoria', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('admin', models.BooleanField(blank=True, null=True)),
                ('nivel', models.IntegerField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('cidade', models.CharField(blank=True, max_length=255, null=True)),
                ('cidade_id', models.CharField(blank=True, max_length=255, null=True)),
                ('uf_id', models.CharField(blank=True, max_length=255, null=True)),
                ('uf', models.CharField(blank=True, max_length=255, null=True)),
                ('uf_nome', models.CharField(blank=True, max_length=255, null=True)),
                ('promo', models.BooleanField(blank=True, null=True)),
                ('promo_extra', models.CharField(blank=True, max_length=255, null=True)),
                ('contagem_anuncios', models.IntegerField(blank=True, null=True)),
                ('lista_automoveis', models.CharField(blank=True, max_length=255, null=True)),
                ('newsletter', models.BooleanField(blank=True, null=True)),
                ('sobre', models.CharField(blank=True, max_length=255, null=True)),
                ('zap', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
