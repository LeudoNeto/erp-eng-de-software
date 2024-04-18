from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from django.contrib.auth import login, logout

from .models import Cargo
from api.usuarios.models import usuario
from .serializers import (
    CargoSerializer,
    CategoriaPermissaoSerializer,
    PermissaoSerializer
)

class LoginViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            data = request.data

            if 'email' not in data or 'senha' not in data:
                return Response({'erro': 'Email e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

            usuario_obj = usuario.objects.filter(email=data['email']).first()
            if not usuario_obj or not usuario_obj.check_password(data['senha']):
                return Response({'erro': 'E-mail ou senha incorretos'}, status=status.HTTP_401_UNAUTHORIZED)
            
            login(request, usuario_obj)

            return Response({'sucesso': 'Usuário autenticado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro': 'Erro ao autenticar usuário', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['get'])
    def logout(self, request):
        logout(request)
        return Response({'sucesso': 'Usuário deslogado com sucesso'}, status=status.HTTP_200_OK)


class CargoViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            data = request.data.copy()

            if 'nome' not in data or 'descricao' not in data or 'nivel_acesso' not in data:
                return Response({'erro': 'Nome, descrição e nível de acesso são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
            
            data["empresa"] = request.user.empresa_id

            serializer = CargoSerializer(data=data)
            if not serializer.is_valid():
                return Response({'erro': 'Erro ao criar cargo', 'detalhes': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({'sucesso': 'Cargo criado com sucesso'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'erro': 'Erro ao criar cargo', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            cargo = Cargo.objects.filter(empresa=request.user.empresa, id=pk).first()
            if not cargo:
                return Response({'erro': 'Cargo não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            cargo.delete()
            return Response({'sucesso': 'Cargo deletado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro': 'Erro ao deletar cargo', 'detalhes': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)