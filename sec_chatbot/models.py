from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class AlunoManager(BaseUserManager):
    def create_user(self, ra, nome, password=None, **extra_fields):
        if not ra:
            raise ValueError('O RA deve ser definido')
        user = self.model(ra=ra, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, ra, nome, password=None, **extra_fields):
        """
        Create and return a superuser with a username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(ra, nome, password, **extra_fields)

class Aluno(AbstractBaseUser, PermissionsMixin):
    ra = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    horas_complementares = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Necessário para superusuário
    is_superuser = models.BooleanField(default=False)  # Necessário para superusuário

    USERNAME_FIELD = 'ra'
    REQUIRED_FIELDS = ['nome']

    objects = AlunoManager()

    def __str__(self):
        return self.nome