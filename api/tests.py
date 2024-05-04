from erp.tests import ErpTestCase
from rest_framework.test import APIRequestFactory
from .views import DashboardViewSet
from api.usuarios.models import usuario
from api.empresas.models import empresa
from api.autenticacao.models import Cargo

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
