from django.db import models

from api.empresas.models import empresa
from api.clientes.models import clientes
from api.produtos.models import produto
from api.usuarios.models import usuario

class comprovante(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=255)
    vendedor = models.ForeignKey(usuario, on_delete=models.CASCADE)
    METODO_PAGAMENTO_CHOICES = [
        ('d', 'Dinheiro'),
        ('p', 'PIX'),
        ('d', 'Débito'),
        ('c', 'Crédito')
    ]
    metodo_pagamento = models.CharField(max_length=1, choices=METODO_PAGAMENTO_CHOICES)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    taxas = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateTimeField(auto_now_add=True)

class comprovante_produtos(models.Model):
    id = models.AutoField(primary_key=True)
    comprovante = models.ForeignKey(comprovante, on_delete=models.CASCADE)
    produto = models.ForeignKey(produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    