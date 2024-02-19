from django.db import models

class produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, null=True)
    foto = models.FileField(upload_to='produtos/', null=True)
    codigo_referencia = models.CharField(max_length=63)
    valor_custo_padrao = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_venda_padrao = models.DecimalField(max_digits=10, decimal_places=2, null=True)