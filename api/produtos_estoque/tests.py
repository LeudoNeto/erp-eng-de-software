from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import ProdutoEstoqueViewSet
from .models import produto_estoque
from api.produtos.models import produto
from api.empresas.models import empresa
from api.usuarios.models import usuario
from api.autenticacao.models import Cargo

class ProdutoEstoqueViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProdutoEstoqueViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'put', 'delete': 'destroy'})
        
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

        self.produto = produto.objects.create(
            empresa=self.empresa,
            nome='Produto Teste',
            descricao='Descrição do Produto Teste',
            codigo_referencia='123456',
        )

        self.produto_estoque_data = {
            'empresa': self.empresa.id,
            'produto': self.produto.id,
            'quantidade': 10,
            'valor_custo': 10.00,
            'valor_venda': 20.00,
            'localizacao': 'Localização do Produto'
        }

    def test_create_produto_estoque(self):
        request = self.factory.post('/api/produtos_estoque/', self.produto_estoque_data, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sucesso', response.data)

    def test_retrieve_produto_estoque(self):
        self.produto_estoque_data['empresa'] = self.empresa
        self.produto_estoque_data['produto'] = self.produto
        
        produto_estoque_obj = produto_estoque.objects.create(**self.produto_estoque_data)
        request = self.factory.get('/api/produtos_estoque/', {'pk': produto_estoque_obj.id})


        response = self.view(request, pk=produto_estoque_obj.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_produto_estoque(self):  
        self.produto_estoque_data['empresa'] = self.empresa
        self.produto_estoque_data['produto'] = self.produto
        
        produto_estoque_obj = produto_estoque.objects.create(**self.produto_estoque_data)
        
        updated_data = {
            'empresa': self.empresa.id,  # Atualizando a empresa
            'produto': self.produto.id,  # Atualizando o produto
            'quantidade': 20,  # Alterando a quantidade para 20
            'valor_custo': 15.00,  # Alterando o valor de custo para 15.00
            'valor_venda': 25.00,  # Alterando o valor de venda para 25.00
            'localizacao': 'Nova Localização do Produto'  # Alterando a localização
        }
        
        request = self.factory.put('/api/produtos_estoque/', updated_data, format='json')
        request.user = self.user
        response = self.view(request, pk=produto_estoque_obj.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sucesso', response.data)
        
        # Verifica se os dados foram atualizados no objeto
        produto_estoque_obj.refresh_from_db()
        self.assertEqual(produto_estoque_obj.empresa.id, updated_data['empresa'])
        self.assertEqual(produto_estoque_obj.produto.id, updated_data['produto'])
        self.assertEqual(produto_estoque_obj.quantidade, updated_data['quantidade'])
        self.assertEqual(produto_estoque_obj.valor_custo, updated_data['valor_custo'])
        self.assertEqual(produto_estoque_obj.valor_venda, updated_data['valor_venda'])
        self.assertEqual(produto_estoque_obj.localizacao, updated_data['localizacao'])
        
    def test_delete_produto_estoque(self):
        self.produto_estoque_data['empresa'] = self.empresa
        self.produto_estoque_data['produto'] = self.produto
        
        produto_estoque_obj = produto_estoque.objects.create(**self.produto_estoque_data)
        request = self.factory.delete('/api/produtos_estoque/', {'pk': produto_estoque_obj.id})
        request.user = self.user

        response = self.view(request, pk=produto_estoque_obj.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sucesso', response.data)

        # Verifica se o objeto foi removido do banco de dados
        with self.assertRaises(produto_estoque.DoesNotExist):
            produto_estoque.objects.get(pk=produto_estoque_obj.id)
