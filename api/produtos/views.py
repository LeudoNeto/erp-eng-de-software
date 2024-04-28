from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.http import FileResponse

from .models import produto
from .serializers import ProdutoSerializer

class ProdutoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            produto_obj = produto.objects.get(pk=pk)
            produto_serializer = ProdutoSerializer(produto_obj)
            return Response(produto_serializer.data, status=status.HTTP_200_OK)
        except produto.DoesNotExist:
            return Response({'erro': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao buscar produto', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def get_produto_foto(self, request, pk=None):
        try:
            produto_obj = produto.objects.get(pk=pk)
            if produto_obj.foto:
                user_foto = open(str(produto_obj.foto.path), "rb")
                response = FileResponse(user_foto)
                response["Content-Type"] = f'image/{str(produto_obj.foto).split(".")[-1]}'
                return response
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except produto.DoesNotExist:
            print(e)
            return Response({'erro': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'erro': 'Erro ao buscar produto', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data['empresa'] = request.user.empresa.id

            produto_serializer = ProdutoSerializer(data=data)
            if produto_serializer.is_valid():
                produto_serializer.save()
                data = {'sucesso': 'Produto criado com sucesso.'}
                return Response(data, status=status.HTTP_200_OK)
            else:
                errors = produto_serializer.errors
                if errors:
                    return Response({'erro': 'Erro ao criar produto', 'detalhes': str(errors)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'erro': 'Erro ao criar produto', 'detalhes': 'Erro de validação'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': 'Erro ao criar produto', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None):
        try:
            prod = produto.objects.get(pk=pk)
            data = request.data.copy()
            data['empresa'] = request.user.empresa.id

            if 'foto' in data and not data['foto']:
                del data['foto']

            produto_serializer = ProdutoSerializer(prod, data=data)
            if produto_serializer.is_valid():
                produto_serializer.save()
                data = {'sucesso': 'Produto salvo com sucesso.'}
                return Response(data, status=status.HTTP_200_OK)
            else:
                errors = produto_serializer.errors
                if errors:
                    return Response({'erro': 'Erro ao editar produto', 'detalhes': str(errors)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'erro': 'Erro ao editar produto', 'detalhes': 'Erro de validação'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': 'Erro ao editar produto', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            produto_obj = produto.objects.get(pk=pk)
            produto_obj.delete()
            return Response({'sucesso': 'Produto deletado com sucesso.'}, status=status.HTTP_200_OK)
        except produto.DoesNotExist:
            return Response({'erro': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao deletar produto', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)