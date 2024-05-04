from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.db import transaction

from .models import comprovante, comprovante_produtos
from .serializers import ComprovanteSerializer, ComprovanteProdutoSerializer
from erp.utils import tratar_erros_serializer

import json

# Create your views here.
class ComprovanteViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            produtos_comprovante = json.loads(data['produtos_comprovante'])

            data['empresa'] = request.user.empresa.id

            with transaction.atomic():
                comprovante_serializer = ComprovanteSerializer(data=data)
                if comprovante_serializer.is_valid():
                    comprovante = comprovante_serializer.save()
                else:
                    return Response({'erro': 'Erro ao emitir o comprovante', 'detalhes': tratar_erros_serializer(comprovante_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto_comprovante in produtos_comprovante:
                    produto_comprovante['comprovante'] = comprovante.id
                    produto_comprovante_serializer = ComprovanteProdutoSerializer(data=produto_comprovante)
                    if produto_comprovante_serializer.is_valid():
                        produto_comprovante_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto_comprovante["produto"]}', 'detalhes': tratar_erros_serializer(produto_comprovante_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            data = {'sucesso': 'Comprovante emitido com sucesso.', "comprovante": comprovante.id}
            return Response(data, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'erro': 'Erro ao emitir o comprovante.', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            comprovante_obj = comprovante.objects.get(pk=pk)
            comprovante_obj.delete()
            return Response({'sucesso': 'Comprovante deletado com sucesso.'}, status=status.HTTP_200_OK)
        except comprovante.DoesNotExist:
            return Response({'erro': 'Comprovante não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'erro': 'Erro ao deletar o comprovante', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)