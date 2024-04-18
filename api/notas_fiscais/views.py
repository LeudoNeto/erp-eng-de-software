from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.db import transaction

from .models import nota_fiscal, nota_fiscal_produtos
from .serializers import NotaFiscalSerializer, NotaFiscalProdutoSerializer

import json

# Create your views here.
class NotaFiscalViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            produtos_nota_fiscal = json.loads(data['produtos_nota_fiscal'])

            data['empresa'] = request.user.empresa.id

            with transaction.atomic():
                nota_fiscal_serializer = NotaFiscalSerializer(data=data)
                if nota_fiscal_serializer.is_valid():
                    nota_fiscal_obj = nota_fiscal_serializer.save()
                else:
                    return Response({'erro': 'Erro ao emitir a nota fiscal', 'detalhes': str(nota_fiscal_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

                for produto_nota_fiscal in produtos_nota_fiscal:
                    produto_nota_fiscal['nota_fiscal'] = nota_fiscal_obj.id
                    produto_nota_fiscal_serializer = NotaFiscalProdutoSerializer(data=produto_nota_fiscal)
                    if produto_nota_fiscal_serializer.is_valid():
                        produto_nota_fiscal_serializer.save()
                    else:
                        return Response({'erro': f'Erro no produto: {produto_nota_fiscal["produto"]}', 'detalhes': str(produto_nota_fiscal_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            data = {'sucesso': 'Nota fiscal emitida com sucesso.', "nota_fiscal": nota_fiscal_obj.id}
            return Response(data, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'erro': 'Erro ao emitir a nota_fiscal.', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)