from rest_framework import serializers
from .models import transacao, produto_transacao

class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = transacao
        exclude = ["id"]

class ProdutoTransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = produto_transacao
        exclude = ["id"]