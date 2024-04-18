from django.db import models

from api.empresas.models import empresa

class CategoriaPermissao(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=63)

class Permissao(models.Model):
    id = models.AutoField(primary_key=True)
    codename = models.CharField(max_length=63)
    categoria = models.ForeignKey(CategoriaPermissao, on_delete=models.CASCADE)

class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=63)
    descricao = models.CharField(max_length=255)
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    permissoes = models.ManyToManyField(Permissao, blank=True)
    nivel_acesso = models.IntegerField() # 1 a 10, sendo 1 o menor nível de acesso e 10 o maior