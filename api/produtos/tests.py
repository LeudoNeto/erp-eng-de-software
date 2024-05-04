from erp.tests import ErpTestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import ProdutoViewSet
from .models import produto
from api.empresas.models import empresa
from api.autenticacao.models import Cargo
from api.usuarios.models import usuario

class ProdutoViewSetTestCase(ErpTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProdutoViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'put', 'delete': 'destroy'})

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

    def test_retrieve_existing_produto(self):
        produto_obj = produto.objects.create(
            empresa=self.empresa,
            nome='Produto Teste',
            descricao='Descrição do Produto Teste',
            codigo_referencia='REF123',
            valor_custo_padrao=10.00,
            valor_venda_padrao=20.00,
            aliquota_icms=18.5
        )
        request = self.factory.get('/api/produto/{}/'.format(produto_obj.pk))
        response = self.view(request, pk=produto_obj.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_produto(self):
        request = self.factory.get('/api/produto/9999/')
        response = self.view(request, pk=9999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_produto_success(self):
        data = {
            'nome': 'Novo Produto',
            'descricao': 'Descrição do Novo Produto',
            'codigo_referencia': 'REF456',
            'valor_custo_padrao': 15.00,
            'valor_venda_padrao': 25.00,
            'aliquota_icms': 12.5
        }
        request = self.factory.post('/api/produto/', data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_produto_missing_fields(self):
        # Test missing required fields
        data = {
            'nome': 'Novo Produto',
            'codigo_referencia': 'REF789',
        }
        for key in data.keys():
            data_missing = data.copy()
            del data_missing[key]
            request = self.factory.post('/api/produto/', data_missing)
            request.user = self.user
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_existing_produto(self):
        produto_obj = produto.objects.create(
            empresa=self.empresa,
            nome='Produto Existente',
            descricao='Descrição do Produto Existente',
            codigo_referencia='REF999',
            valor_custo_padrao=5.00,
            valor_venda_padrao=15.00,
            aliquota_icms=10.0
        )
        data = {
            'nome': 'Produto Modificado',
            'descricao': 'Descrição do Produto Modificado',
            'codigo_referencia': 'REF999',
            'valor_custo_padrao': 7.00,
            'valor_venda_padrao': 18.00,
            'aliquota_icms': 11.0
        }
        request = self.factory.put('/api/produto/{}/'.format(produto_obj.pk), data)
        request.user = self.user
        response = self.view(request, pk=produto_obj.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_nonexistent_produto(self):
        data = {
            'nome': 'Produto Modificado',
            'descricao': 'Descrição do Produto Modificado',
            'codigo_referencia': 'REF999',
            'valor_custo_padrao': 7.00,
            'valor_venda_padrao': 18.00,
            'aliquota_icms': 11.0
        }
        request = self.factory.put('/api/produto/9999/', data)
        request.user = self.user
        response = self.view(request, pk=9999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing_produto(self):
        produto_obj = produto.objects.create(
            empresa=self.empresa,
            nome='Produto Existente',
            descricao='Descrição do Produto Existente',
            codigo_referencia='REF999',
            valor_custo_padrao=5.00,
            valor_venda_padrao=15.00,
            aliquota_icms=10.0
        )
        request = self.factory.delete('/api/produto/{}/'.format(produto_obj.pk))
        request.user = self.user
        response = self.view(request, pk=produto_obj.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_nonexistent_produto(self):
        request = self.factory.delete('/api/produto/9999/')
        request.user = self.user
        response = self.view(request, pk=9999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
