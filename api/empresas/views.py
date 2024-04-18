from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from .models import empresa
from .serializers import EmpresaSerializer


class EmpresaViewSet(viewsets.ViewSet):

    def update(self, request, pk=None):
        try:
            data = request.data

            empresa_obj = empresa.objects.filter(id=pk).first()
            if not empresa_obj:
                return Response({'erro': 'Empresa não encontrada'}, status=status.HTTP_404_NOT_FOUND)

            if not data['telefone_whatsapp']:
                data['telefone_whatsapp'] = None

            empresa_serializer = EmpresaSerializer(empresa_obj, data=data, partial=True)
            if not empresa_serializer.is_valid():
                errors = empresa_serializer.errors
                if errors:
                    return Response({'erro': 'Erro ao atualizar empresa', 'detalhes': str(errors)}, status=status.HTTP_400_BAD_REQUEST)
                
            empresa_serializer.save()
            return Response({'sucesso': 'Empresa atualizada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro': 'Erro ao atualizar empresa', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)