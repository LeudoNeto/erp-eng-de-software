from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.http import FileResponse

from .models import usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            data = request.data.copy()

            if 'nome' not in data or 'email' not in data or 'password' not in data or 'telefone' not in data or 'cargo' not in data:
                return Response({'erro': 'Nome, e-mail, telefone, cargo e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
            
            data["empresa"] = request.user.empresa_id
            data["is_active"] = True

            serializer = UsuarioSerializer(data=data)
            if not serializer.is_valid():
                return Response({'erro': 'Erro ao cadastrar o funcionário', 'detalhes': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({'sucesso': 'Usuário criado com sucesso'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'erro': 'Erro ao cadastrar o funcionário', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk=None):
        try:
            usuario_obj = usuario.objects.filter(id=pk).first()
            if not usuario_obj:
                return Response({'erro': 'Funcionário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            usuario_obj.delete()
            return Response({'sucesso': 'Usuário deletado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro': 'Erro ao deletar o funcionário', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)