from django.db import models

from api.empresas.models import empresa
from api.clientes.models import clientes
from api.produtos.models import produto

class nota_fiscal(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=255)
    cliente_endereco = models.CharField(max_length=255)
    TIPO_CHOICES = [
        ('v', 'Venda'),
        ('p', 'Serviço Prestado'),
    ]
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    valor_total_produtos = models.DecimalField(max_digits=10, decimal_places=2)
    icms_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    taxas = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateTimeField(auto_now_add=True)

class nota_fiscal_produtos(models.Model):
    id = models.AutoField(primary_key=True)
    nota_fiscal = models.ForeignKey(nota_fiscal, on_delete=models.CASCADE)
    produto = models.ForeignKey(produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_icms = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    