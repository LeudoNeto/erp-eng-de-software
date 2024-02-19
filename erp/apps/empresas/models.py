from django.db import models

class empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    telefone_whatsapp = models.CharField(max_length=15, null=True, unique=True)
    email = models.CharField(max_length=255, unique=True)
    endereco = models.CharField(max_length=255)