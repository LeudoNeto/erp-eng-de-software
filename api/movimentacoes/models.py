from django.db import models

from api.empresas.models import empresa
from api.produtos.models import produto
from api.usuarios.models import usuario

class transacao(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=255, null=True)
    cliente_endereco = models.CharField(max_length=255, null=True, blank=True)
    vendedor = models.ForeignKey(usuario, on_delete=models.CASCADE, null=True)
    data = models.DateTimeField(auto_now_add=True)
    valor_total_recebido = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_total_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_de_custo_dos_produtos = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_de_venda_dos_produtos = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    lucro = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    taxas = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    TIPO_CHOICES = [
        ('c', 'Compra'),
        ('v', 'Venda'),
        ('t', 'Troca'),
        ('p', 'Serviço Prestado'),
        ('r', 'Serviço Recebido')
    ]
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    METODO_PAGAMENTO_CHOICES = [
        ('d', 'Dinheiro'),
        ('p', 'PIX'),
        ('d', 'Débito'),
        ('c', 'Crédito')
    ]
    metodo_pagamento = models.CharField(max_length=1, choices=METODO_PAGAMENTO_CHOICES, null=True, blank=True)

class produto_transacao(models.Model):
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(produto, on_delete=models.CASCADE)
    transacao = models.ForeignKey(transacao, on_delete=models.CASCADE)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantidade = models.IntegerField()
    TIPO_CHOICES = [
        ('e', 'Entrada'),
        ('s', 'Saída'),
    ]
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)