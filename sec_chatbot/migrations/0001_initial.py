# Generated by Django 5.1 on 2024-09-01 18:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id_curso', models.AutoField(primary_key=True, serialize=False)),
                ('nome_curso', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('ra', models.CharField(max_length=20, unique=True)),
                ('nome', models.CharField(max_length=100)),
                ('horas_complementares', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('curso', models.CharField(max_length=50)),
                ('turma', models.CharField(max_length=3)),
                ('situacao_matricula', models.CharField(max_length=30)),
                ('semestre', models.DecimalField(decimal_places=0, default=0, max_digits=2)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id_materia', models.AutoField(primary_key=True, serialize=False)),
                ('nome_materia', models.CharField(max_length=100, unique=True)),
                ('ementa_materia', models.TextField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sec_chatbot.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trabalho_um', models.DecimalField(decimal_places=2, max_digits=5)),
                ('trabalho_dois', models.DecimalField(decimal_places=2, max_digits=5)),
                ('prova', models.DecimalField(decimal_places=2, max_digits=5)),
                ('media', models.DecimalField(decimal_places=2, max_digits=5)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sec_chatbot.curso')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sec_chatbot.materia')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rp', models.CharField(max_length=20, unique=True)),
                ('nome', models.CharField(max_length=100)),
                ('formacao', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sec_chatbot.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigla_turma', models.CharField(max_length=10, unique=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sec_chatbot.curso')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioAula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.CharField(max_length=20)),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sec_chatbot.materia')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sec_chatbot.turma')),
            ],
        ),
    ]
