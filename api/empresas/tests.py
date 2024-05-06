from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from django.urls import reverse
from .views import EmpresaViewSet
from .models import empresa

class EmpresaViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = EmpresaViewSet.as_view({'put': 'update'})

        # Criar uma empresa para usar nos testes
        self.empresa = empresa.objects.create(
            nome='Empresa Teste',
            cnpj='12.345.678/0001-01',
            telefone='(12) 3456-7890',
            telefone_whatsapp='(12) 98765-4321',
            email='empresa@teste.com',
            endereco='Rua da Empresa, 123'
        )

    def test_update_empresa_success(self):
        data = {
            'nome': 'Nova Empresa Teste',
            'cnpj': '98.765.432/0001-21',
            'telefone': '(99) 8765-4321',
            'telefone_whatsapp': '(99) 8765-4321',
            'email': 'novaempresa@teste.com',
            'endereco': 'Rua da Nova Empresa, 456'
        }
        request = self.factory.put('/api/empresas/1/', data)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_nonexistent_empresa(self):
        data = {
            'nome': 'Nova Empresa Teste',
            'cnpj': '98.765.432/0001-21',
            'telefone': '(99) 8765-4321',
            'telefone_whatsapp': '(99) 8765-4321',
            'email': 'novaempresa@teste.com',
            'endereco': 'Rua da Nova Empresa, 456'
        }
        request = self.factory.put('/api/empresas/9931899/', data)
        response = self.view(request, pk=9931899)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
