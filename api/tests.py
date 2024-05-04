from erp.tests import ErpTestCase
from erp.views import IndexView
from rest_framework.test import APIRequestFactory
from .views import DashboardViewSet
from .produtos.views import ProdutoViewSet
from api.usuarios.models import usuario
from api.empresas.models import empresa
from api.autenticacao.models import Cargo

from django.utils import timezone
from django.contrib.auth.models import AnonymousUser

from concurrent.futures import ThreadPoolExecutor

class DashboardViewSetTestCase(ErpTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DashboardViewSet.as_view({'get': 'list'})
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

    def test_dashboard_get(self):
        request = self.factory.get('/api/dashboard/')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

class RequisitosNaoFuncionais(ErpTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

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

    # O tempo de resposta das requisições ao servidor deve ser inferior a 1 segundo
    def test_nao_funcional_desempenho(self):
        view = DashboardViewSet.as_view({'get': 'list'})
        start_time = timezone.now()
        request = self.factory.get('/')
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        end_time = timezone.now()
        elapsed_time = (end_time - start_time).total_seconds()
        self.assertLess(elapsed_time, 1)

        view = ProdutoViewSet.as_view({'post': 'create'})
        data = {
            'nome': 'Novo Produto',
            'descricao': 'Descrição do Novo Produto',
            'codigo_referencia': 'REF456',
            'valor_custo_padrao': 15.00,
            'valor_venda_padrao': 25.00,
            'aliquota_icms': 12.5
        }
        start_time = timezone.now()
        request = self.factory.post('/api/produtos/', data)
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 201)
        end_time = timezone.now()
        elapsed_time = (end_time - start_time).total_seconds()
        self.assertLess(elapsed_time, 1)

    # Deve verificar se o usuário está autenticado em todas as páginas,
    #redirecionando para a página de login caso não esteja.
    def test_nao_funcional_seguranca(self):
        view = IndexView.as_view()
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

        request = self.factory.get('/')
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)

    # Deve comportar 10 usuários simultâneos sem comprometer o tempo de resposta
    def test_nao_funcional_escalabilidade(self):
        view = IndexView.as_view()
        start_time = timezone.now()

        # Definir a função para realizar a solicitação GET
        def make_request():
            request = self.factory.get('/')
            request.user = self.user
            response = view(request)

        # Executar 10 solicitações em threads separados
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(make_request) for _ in range(10)]

            # Aguardar até que todas as solicitações sejam concluídas
            for future in futures:
                future.result()

        end_time = timezone.now()
        elapsed_time = (end_time - start_time).total_seconds()
        self.assertLess(elapsed_time, 1)
