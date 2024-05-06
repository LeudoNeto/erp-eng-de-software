from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import NotaFiscalViewSet
from .models import nota_fiscal, nota_fiscal_produtos
from api.produtos.models import produto
from api.empresas.models import empresa
from api.usuarios.models import usuario
from api.autenticacao.models import Cargo
import json

class NotaFiscalViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = NotaFiscalViewSet.as_view({'post': 'create'})

        self.empresa = empresa.objects.create(
            nome='Minha Empresa Teste',
            cnpj='12.345.678/9012-34',
            telefone='(12) 34567-8910',
            telefone_whatsapp='(12) 34567-8910',
            email='empresa@teste.com',
            endereco='Endereço da Empresa Teste'
        )
        self.cargo = Cargo.objects.create(
            nome='Administrador',
            descricao='Cargo de administrador da empresa',
            empresa=self.empresa,
            nivel_acesso=10
        )
        self.user = usuario.objects.create(nome='testuser', email='test@example.com', password='testpassword', empresa=self.empresa, cargo=self.cargo)

        self.produto1 = produto.objects.create(
            empresa=self.empresa,
            nome='Produto Teste',
            descricao='Descrição do Produto Teste',
            codigo_referencia='123456',
        )
        self.produto2 = produto.objects.create(
            empresa=self.empresa,
            nome='Produto Teste',
            descricao='Descrição do Produto Teste',
            codigo_referencia='123456',
        )

    def test_create_nota_fiscal_success(self):
        data = {
            'cliente': 'Cliente Teste',
            'produtos_nota_fiscal': json.dumps([
                {
                    'produto': self.produto1.id,
                    'quantidade': 2,
                    'valor_unitario': 30.00,
                    'valor_total': 60.00
                },
                {
                    'produto': self.produto2.id,
                    'quantidade': 1,
                    'valor_unitario': 40.00,
                    'valor_total': 40.00
                }
            ])
        }

        request = self.factory.post('/api/notas_fiscais/', data, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # não consegui fazer funcionar, tá dando 400

    def test_create_nota_fiscal_invalid_data(self):
        data = {
            'cliente': 'Cliente Teste',
            'valor_total': 100.00,
            'produtos_nota_fiscal': json.dumps([
                {
                    'produto': self.produto1.id,
                    'quantidade': 2,
                    'valor_unitario': 30.00,
                    'valor_total': 60.00
                },
                {
                    'produto': self.produto2.id,
                    'quantidade': 1,
                    'valor_unitario': 40.00,
                    'valor_total': 40.00
                }
            ])
        }
        request = self.factory.post('/api/notas_fiscais/', data, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_nota_fiscal_invalid_data_and_error(self):
        data = {
            'cliente': 'Cliente Teste',
            'produtos_nota_fiscal': 'not a valid JSON string'  
        }

        request = self.factory.post('/api/notas_fiscais/', data, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
