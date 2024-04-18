from django.db import models

from api.empresas.models import empresa
from api.produtos.models import produto
from api.usuarios.models import usuario

class produto_estoque(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    produto = models.ForeignKey(produto, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255, null=True)
    quantidade = models.IntegerField()
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    localizacao = models.CharField(max_length=255, null=True)

class produto_estoque_transacao(models.Model):
    id = models.AutoField(primary_key=True)
    produto_estoque = models.ForeignKey(produto_estoque, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255, null=True)
    quantidade = models.IntegerField()
    TIPO_CHOICES = [
        ('e', 'Entrada'),
        ('s', 'Saída'),
    ]
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
