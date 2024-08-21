# Generated by Django 5.0.7 on 2024-08-21 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
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
    ]
