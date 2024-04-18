from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.db import transaction

from .models import transacao, produto_transacao
from api.produtos_estoque.models import produto_estoque
from api.produtos_estoque.serializers import ProdutoEstoqueSerializer
from api.comprovantes.models import comprovante, comprovante_produtos
from .serializers import TransacaoSerializer, ProdutoTransacaoSerializer
from api.comprovantes.serializers import ComprovanteSerializer, ComprovanteProdutoSerializer

import json

# Create your views here.
class TransacaoViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            transacao = json.loads(data['transacao'])
            transacao['lucro'] = 10.5
            produtos_transacao = json.loads(data['produtos_transacao'])

            with transaction.atomic():
                transacao_serializer = TransacaoSerializer(data=transacao)
                if transacao_serializer.is_valid():
                    transacao = transacao_serializer.save()
                else:
                    return Response({'erro': 'Erro ao cadastrar a movimentação', 'detalhes': str(transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto_transacao in produtos_transacao:
                    produto_transacao['transacao'] = transacao.id
                    produto_transacao_serializer = ProdutoTransacaoSerializer(data=produto_transacao)
                    if produto_transacao_serializer.is_valid():
                        produto_transacao_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto_transacao["produto"]}', 'detalhes': str(produto_transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            data = {'sucesso': 'Movimentação cadastrada com sucesso.'}
            return Response(data, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'erro': 'Erro ao cadastrar movimentação.', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            transacao_obj = transacao.objects.get(pk=pk)
            transacao_obj.delete()
            return Response({'sucesso': 'Movimentação deletada com sucesso.'}, status=status.HTTP_200_OK)
        except transacao.DoesNotExist:
            return Response({'erro': 'Movimentação não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao deletar a movimentação', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class VendaViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            transacao = json.loads(data['transacao'])
            produtos_transacao = json.loads(data['produtos_transacao'])
            produtos_estoque = json.loads(data['produtos_estoque'])
            
            transacao['empresa'] = request.user.empresa.id

            with transaction.atomic():
                transacao_serializer = TransacaoSerializer(data=transacao)
                if transacao_serializer.is_valid():
                    transacao_obj = transacao_serializer.save()
                else:
                    return Response({'erro': 'Erro ao cadastrar a venda', 'detalhes': str(transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto_transacao in produtos_transacao:
                    produto_transacao['transacao'] = transacao_obj.id
                    produto_transacao_serializer = ProdutoTransacaoSerializer(data=produto_transacao)
                    if produto_transacao_serializer.is_valid():
                        produto_transacao_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto_transacao["produto"]}', 'detalhes': str(produto_transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
                    
                if transacao["remover_estoque"]:
                    for produto in produtos_estoque:
                        produto_estoque_obj = produto_estoque.objects.get(id=produto['id'])
                        produto_estoque_obj.quantidade -= int(produto['quantidade'])
                        if produto_estoque_obj.quantidade < 0:
                            raise Exception(f'Quantidade insuficiente para o produto {produto_estoque_obj.produto.nome}')
                        elif produto_estoque_obj.quantidade == 0:
                            produto_estoque_obj.delete()
                        else:
                            produto_estoque_obj.save()

            data = {'sucesso': 'Venda cadastrada com sucesso.', 'venda_id': transacao_obj.id}
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'erro': 'Erro ao cadastrar venda.', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'])
    def comprovante_da_venda(self, request, pk):
        try:
            transacao_obj = transacao.objects.get(pk=pk)
            produtos_transacao = produto_transacao.objects.filter(transacao=transacao_obj).values(
                "produto_id", "quantidade", "valor_venda"
            )

            with transaction.atomic():
                comprovante_serializer = ComprovanteSerializer(data={
                    "empresa": transacao_obj.empresa_id,
                    "cliente": transacao_obj.cliente,
                    "metodo_pagamento": transacao_obj.metodo_pagamento,
                    "subtotal": transacao_obj.valor_de_venda_dos_produtos,
                    "taxas": transacao_obj.taxas,
                    "desconto": transacao_obj.desconto,
                    "total": transacao_obj.valor_total_recebido
                })
                if comprovante_serializer.is_valid():
                    comprovante = comprovante_serializer.save()
                else:
                    return Response({'erro': 'Erro ao emitir o comprovante', 'detalhes': str(comprovante_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto in produtos_transacao:
                    print(produto)
                    produto_comprovante_serializer = ComprovanteProdutoSerializer(data={
                        "comprovante": comprovante.id,
                        "produto": produto["produto_id"],
                        "quantidade": produto["quantidade"],
                        "valor_unitario": produto["valor_venda"],
                        "valor_total": produto["valor_venda"] * produto["quantidade"]
                    })
                    if produto_comprovante_serializer.is_valid():
                        produto_comprovante_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto["produto"]}', 'detalhes': str(produto_comprovante_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            data = {'sucesso': 'Comprovante emitido com sucesso.', "comprovante": comprovante.id}
            return Response(data, status=status.HTTP_200_OK)
        
        except transacao.DoesNotExist:
            return Response({'erro': 'Transação não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao emitir comprovante', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CompraViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            transacao = json.loads(data['transacao'])
            produtos_transacao = json.loads(data['produtos_transacao'])
            
            transacao['empresa'] = request.user.empresa.id

            with transaction.atomic():
                transacao_serializer = TransacaoSerializer(data=transacao)
                if transacao_serializer.is_valid():
                    transacao_obj = transacao_serializer.save()
                else:
                    return Response({'erro': 'Erro ao cadastrar a compra', 'detalhes': str(transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto_transacao in produtos_transacao:
                    produto_transacao['transacao'] = transacao_obj.id
                    produto_transacao_serializer = ProdutoTransacaoSerializer(data=produto_transacao)
                    if produto_transacao_serializer.is_valid():
                        produto_transacao_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto_transacao["produto"]}', 'detalhes': str(produto_transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
                    
                if transacao["adicionar_estoque"]:
                    for produto in produtos_transacao:
                        produto_estoque_obj = produto_estoque.objects.filter(
                            produto=produto['produto'],
                            valor_custo=produto['valor_custo'],
                            valor_venda=produto['valor_venda'],
                            empresa=transacao_obj.empresa,
                        ).first()
                        if produto_estoque_obj:
                            produto_estoque_obj.quantidade += int(produto['quantidade'])
                            produto_estoque_obj.save()
                        else:
                            produto_estoque_serializer = ProdutoEstoqueSerializer(data={
                                "produto": produto['produto'],
                                "empresa": transacao_obj.empresa_id,
                                "quantidade": produto['quantidade'],
                                "valor_custo": produto['valor_custo'],
                                "valor_venda": produto['valor_venda'],
                            })
                            if produto_estoque_serializer.is_valid():
                                produto_estoque_serializer.save()
                            else:
                                return Response({'erro': f'Erro no produto: {produto_estoque_serializer["produto"]}', 'detalhes': str(produto_estoque_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            data = {'sucesso': 'Venda cadastrada com sucesso.', 'venda_id': transacao_obj.id}
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'erro': 'Erro ao cadastrar venda.', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)