from erp.tests import ErpTestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import VendaViewSet
from .models import transacao, produto_transacao
from api.produtos.models import produto
from api.empresas.models import empresa
from api.autenticacao.models import Cargo
from api.usuarios.models import usuario
import json

class VendaViewSetTestCase(ErpTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = VendaViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update'})

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

    def test_retrieve_existing_venda(self):
        venda_obj = transacao.objects.create(
            empresa=self.empresa,
            cliente='Cliente Teste',
            valor_total_recebido=100.00,
            valor_total_pago=90.00,
            valor_de_custo_dos_produtos=70.00,
            valor_de_venda_dos_produtos=110.00,
            lucro=20.00,
            tipo='v'
        )
        request = self.factory.get('/api/vendas/{}/'.format(venda_obj.pk))
        response = self.view(request, pk=venda_obj.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_venda(self):
        request = self.factory.get('/api/vendas/9999/')
        response = self.view(request, pk=9999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_venda_success(self):
        produto.objects.create(
            empresa=self.empresa,
            nome='Produto Teste',
            descricao='Descrição do Produto Teste',
            codigo_referencia='123456',
        )
        data = {
            'transacao': json.dumps({
                'cliente': 'Cliente Novo',
                'valor_total_recebido': 150.00,
                'valor_total_pago': 140.00,
                'valor_de_custo_dos_produtos': 90.00,
                'valor_de_venda_dos_produtos': 180.00,
                'lucro': 50.00,
                'tipo': 'v',
                'remover_estoque': False,
            }),
            'produtos_transacao': json.dumps([
                {
                    'produto': 1,  # ID do produto
                    'quantidade': 3,
                    'valor_custo': 30.00,
                    'valor_venda': 60.00,
                    'tipo': 's'
                }
            ]),
            'produtos_estoque': json.dumps([]),
            'remover_estoque': False
        }
        request = self.factory.post('/api/vendas/', data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_venda_invalid_data(self):
        # Test missing required fields
        data = {
            'transacao': json.dumps({}),
            'produtos_transacao': json.dumps([]),
            'produtos_estoque': json.dumps([]),
            'remover_estoque': False
        }
        request = self.factory.post('/api/vendas/', data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_existing_venda(self):
        produto.objects.create(
            empresa=self.empresa,
            nome='Produto Teste',
            descricao='Descrição do Produto Teste',
            codigo_referencia='123456',
        )
        venda_obj = transacao.objects.create(
            empresa=self.empresa,
            cliente='Cliente Teste',
            valor_total_recebido=100.00,
            valor_total_pago=90.00,
            valor_de_custo_dos_produtos=70.00,
            valor_de_venda_dos_produtos=110.00,
            lucro=20.00,
            tipo='v'
        )
        data = {
            'transacao': json.dumps({
                'cliente': 'Cliente Modificado',
                'valor_total_recebido': 150.00,
                'valor_total_pago': 140.00,
                'valor_de_custo_dos_produtos': 90.00,
                'valor_de_venda_dos_produtos': 180.00,
                'lucro': 50.00,
                'tipo': 'v'
            }),
            'produtos_transacao': json.dumps([
                {
                    'produto': 1,  # ID do produto
                    'quantidade': 3,
                    'valor_custo': 30.00,
                    'valor_venda': 60.00,
                    'tipo': 's'
                }
            ])
        }
        request = self.factory.put('/api/vendas/{}/'.format(venda_obj.pk), data)
        request.user = self.user
        response = self.view(request, pk=venda_obj.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_nonexistent_venda(self):
        produto.objects.create(
            empresa=self.empresa,
            nome='Produto Teste',
            descricao='Descrição do Produto Teste',
            codigo_referencia='123456',
        )
        data = {
            'transacao': json.dumps({
                'cliente': 'Cliente Modificado',
                'valor_total_recebido': 150.00,
                'valor_total_pago': 140.00,
                'valor_de_custo_dos_produtos': 90.00,
                'valor_de_venda_dos_produtos': 180.00,
                'lucro': 50.00,
                'tipo': 'v'
            }),
            'produtos_transacao': json.dumps([
                {
                    'produto': 1,  # ID do produto
                    'quantidade': 3,
                    'valor_custo': 30.00,
                    'valor_venda': 60.00,
                    'tipo': 's'
                }
            ])
        }
        request = self.factory.put('/api/vendas/9999/', data)
        request.user = self.user
        response = self.view(request, pk=9999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
