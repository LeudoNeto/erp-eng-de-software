from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

from api.empresas.models import empresa
from api.autenticacao.models import Cargo

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O username é obrigatório')
        
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    foto = models.FileField(upload_to='usuarios/', null=True)
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'telefone']

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)