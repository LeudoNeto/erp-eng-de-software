from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from .models import (
    produto_estoque,
    produto_estoque_transacao
)
from .serializers import ProdutoEstoqueSerializer

class ProdutoEstoqueViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            produto_obj = produto_estoque.objects.get(pk=pk)
            produto_serializer = ProdutoEstoqueSerializer(produto_obj)
            return Response(produto_serializer.data, status=status.HTTP_200_OK)
        except produto_estoque.DoesNotExist:
            return Response({'erro': 'Produto Estoque não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao buscar produto estoque', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data['empresa'] = request.user.empresa.id

            if 'valor_custo' in data:
                data['valor_custo'] = data['valor_custo'].replace('.', '').replace(',', '.')
            if 'valor_venda' in data:
                data['valor_venda'] = data['valor_venda'].replace('.', '').replace(',', '.')

            produto_serializer = ProdutoEstoqueSerializer(data=data)
            if produto_serializer.is_valid():
                produto_serializer.save()
                data = {'sucesso': 'Produto adicionado com sucesso.'}
                return Response(data, status=status.HTTP_200_OK)
            else:
                errors = produto_serializer.errors
                if errors:
                    return Response({'erro': 'Erro ao adicionar produto', 'detalhes': str(errors)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'erro': 'Erro ao adicionar produto', 'detalhes': 'Erro de validação'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': 'Erro ao criar produto', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None):
        try:
            prod = produto_estoque.objects.get(pk=pk)
            data = request.data.copy()
            data['empresa'] = request.user.empresa.id

            if 'valor_custo' in data:
                data['valor_custo'] = data['valor_custo'].replace('.', '').replace(',', '.')
            if 'valor_venda' in data:
                data['valor_venda'] = data['valor_venda'].replace('.', '').replace(',', '.')

            produto_serializer = ProdutoEstoqueSerializer(prod, data=data)
            if produto_serializer.is_valid():
                produto_serializer.save()
                data = {'sucesso': 'Produto Estoque salvo com sucesso.'}
                return Response(data, status=status.HTTP_200_OK)
            else:
                errors = produto_serializer.errors
                if errors:
                    return Response({'erro': 'Erro ao editar produto estoque', 'detalhes': str(errors)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'erro': 'Erro ao editar produto estoque', 'detalhes': 'Erro de validação'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': 'Erro ao editar produto estoque', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            produto_obj = produto_estoque.objects.get(pk=pk)
            produto_obj.delete()
            return Response({'sucesso': 'Produto removido do estoque com sucesso.'}, status=status.HTTP_200_OK)
        except produto_estoque.DoesNotExist:
            return Response({'erro': 'Produto Estoque não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao deletar produto estoque', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)