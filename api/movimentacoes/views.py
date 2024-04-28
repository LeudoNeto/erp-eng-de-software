from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.db import transaction

from .models import transacao, produto_transacao
from api.produtos.models import produto
from api.produtos_estoque.models import produto_estoque
from api.comprovantes.models import comprovante, comprovante_produtos
from api.notas_fiscais.models import nota_fiscal, nota_fiscal_produtos
from .serializers import TransacaoSerializer, ProdutoTransacaoSerializer
from api.produtos_estoque.serializers import ProdutoEstoqueSerializer
from api.comprovantes.serializers import ComprovanteSerializer, ComprovanteProdutoSerializer
from api.notas_fiscais.serializers import NotaFiscalSerializer, NotaFiscalProdutoSerializer

import json

# Create your views here.
class TransacaoViewSet(viewsets.ViewSet):

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
            venda = json.loads(data['transacao'])
            produtos_transacao = json.loads(data['produtos_transacao'])
            produtos_estoque = json.loads(data['produtos_estoque'])
            
            venda['empresa'] = request.user.empresa.id
            venda['lucro'] = round(float(venda['valor_total_recebido']) - venda['valor_total_pago'])

            with transaction.atomic():
                venda_serializer = TransacaoSerializer(data=venda)
                if venda_serializer.is_valid():
                    transacao_obj = venda_serializer.save()
                else:
                    return Response({'erro': 'Erro ao cadastrar a venda', 'detalhes': str(venda_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto_transacao in produtos_transacao:
                    produto_transacao['transacao'] = transacao_obj.id
                    produto_transacao_serializer = ProdutoTransacaoSerializer(data=produto_transacao)
                    if produto_transacao_serializer.is_valid():
                        produto_transacao_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto_transacao["produto"]}', 'detalhes': str(produto_transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
                    
                if venda["remover_estoque"]:
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
                    "vendedor": transacao_obj.vendedor_id,
                    "metodo_pagamento": transacao_obj.metodo_pagamento,
                    "subtotal": transacao_obj.valor_de_venda_dos_produtos,
                    "taxas": transacao_obj.taxas,
                    "desconto": transacao_obj.desconto,
                    "total": transacao_obj.valor_total_recebido
                })
                if comprovante_serializer.is_valid():
                    comprovante_obj = comprovante_serializer.save()
                else:
                    return Response({'erro': 'Erro ao emitir o comprovante', 'detalhes': str(comprovante_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto in produtos_transacao:
                    produto_comprovante_serializer = ComprovanteProdutoSerializer(data={
                        "comprovante": comprovante_obj.id,
                        "produto": produto["produto_id"],
                        "quantidade": produto["quantidade"],
                        "valor_unitario": produto["valor_venda"],
                        "valor_total": produto["valor_venda"] * produto["quantidade"]
                    })
                    if produto_comprovante_serializer.is_valid():
                        produto_comprovante_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto["produto_id"]}', 'detalhes': str(produto_comprovante_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            data = {'sucesso': 'Comprovante emitido com sucesso.', "comprovante": comprovante_obj.id}
            return Response(data, status=status.HTTP_200_OK)
        
        except transacao.DoesNotExist:
            return Response({'erro': 'Transação não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao emitir comprovante', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

    @action(detail=True, methods=['post'])
    def nota_fiscal_da_venda(self, request, pk):
        try:
            transacao_obj = transacao.objects.get(pk=pk)
            produtos_transacao = produto_transacao.objects.filter(transacao=transacao_obj).values(
                "produto_id", "quantidade", "valor_venda"
            )

            with transaction.atomic():
                nota_fiscal_serializer = NotaFiscalSerializer(data={
                    "empresa": transacao_obj.empresa_id,
                    "cliente": transacao_obj.cliente,
                    "cliente_endereco": transacao_obj.cliente_endereco,
                    "tipo": transacao_obj.tipo,
                    "valor_total_produtos": transacao_obj.valor_de_venda_dos_produtos,
                    "desconto": transacao_obj.desconto,
                    "taxas": transacao_obj.taxas,
                    "total": transacao_obj.valor_total_recebido,
                    "total_liquido": transacao_obj.valor_total_recebido
                })
                if nota_fiscal_serializer.is_valid():
                    nota_fiscal_obj = nota_fiscal_serializer.save()
                else:
                    return Response({'erro': 'Erro ao emitir a nota fiscal', 'detalhes': str(nota_fiscal_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                icms_total = 0
                for produto_nf in produtos_transacao:
                    produto_obj = produto.objects.get(id=produto_nf["produto_id"])
                    valor_icms = (produto_obj.aliquota_icms/100) * produto_nf["valor_venda"] * produto_nf["quantidade"]
                    valor_total_liquido = produto_nf["valor_venda"] - valor_icms
                    produto_nota_fiscal_serializer = NotaFiscalProdutoSerializer(data={
                        "nota_fiscal": nota_fiscal_obj.id,
                        "produto": produto_nf["produto_id"],
                        "quantidade": produto_nf["quantidade"],
                        "valor_unitario": produto_nf["valor_venda"],
                        "valor_total": produto_nf["valor_venda"] * produto_nf["quantidade"],
                        "valor_icms": round(valor_icms, 2),
                        "valor_total_liquido": round(valor_total_liquido, 2)
                    })
                    icms_total += valor_icms
                    if produto_nota_fiscal_serializer.is_valid():
                        produto_nota_fiscal_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto_nf["produto_id"]}', 'detalhes': str(produto_nota_fiscal_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                nota_fiscal_obj.icms_total = round(icms_total, 2)
                nota_fiscal_obj.total_liquido = round(nota_fiscal_obj.total - nota_fiscal_obj.icms_total, 2)
                nota_fiscal_obj.save()

            data = {'sucesso': 'Nota fiscal emitida com sucesso.', "nota_fiscal": nota_fiscal_obj.id}
            return Response(data, status=status.HTTP_200_OK)
        
        except transacao.DoesNotExist:
            return Response({'erro': 'Venda não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao emitir nota fiscal', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompraViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            transacao = json.loads(data['transacao'])
            produtos_transacao = json.loads(data['produtos_transacao'])
            
            transacao['empresa'] = request.user.empresa.id
            transacao['lucro'] = 0

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
        
class TrocaViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            transacao = json.loads(data['transacao'])
            produtos_transacao = json.loads(data['produtos_transacao'])

            transacao['empresa'] = request.user.empresa.id

            transacao['lucro'] = 0
            if transacao['calcular_lucro']:
                transacao['lucro'] = round(transacao['valor_total_recebido'] - transacao['valor_total_pago'])

            with transaction.atomic():
                transacao_serializer = TransacaoSerializer(data=transacao)
                if transacao_serializer.is_valid():
                    transacao = transacao_serializer.save()
                else:
                    return Response({'erro': 'Erro ao cadastrar a troca', 'detalhes': str(transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto_transacao in produtos_transacao:
                    produto_transacao['transacao'] = transacao.id
                    produto_transacao_serializer = ProdutoTransacaoSerializer(data=produto_transacao)
                    if produto_transacao_serializer.is_valid():
                        produto_transacao_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto_transacao["produto"]}', 'detalhes': str(produto_transacao_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            data = {'sucesso': 'Troca cadastrada com sucesso.'}
            return Response(data, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'erro': 'Erro ao cadastrar a troca.', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)