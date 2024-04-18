from django.db import models

class clientes(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, null=True)
    cnpj = models.CharField(max_length=18, null=True)
    telefone = models.CharField(max_length=15, null=True)
    telefone_whatsapp = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=255, null=True)
    endereco = models.CharField(max_length=255, null=True)