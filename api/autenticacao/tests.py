from erp.tests import ErpTestCase
from rest_framework.test import APIRequestFactory
from .views import LoginViewSet
from api.usuarios.models import usuario
from api.empresas.models import empresa
from api.autenticacao.models import Cargo

class LoginViewSetTestCase(ErpTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LoginViewSet.as_view({'post': 'create', 'get': 'logout'})
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

    def test_authentication_success(self):
        data = {'email': 'test@example.com', 'senha': 'testpassword'}
        response = self.client.post('/api/login/', data)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_missing_email_or_password(self):
        data = {'email': 'test@example.com'}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, 400)

        data = {'senha': 'testpassword'}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, 400)

    def test_incorrect_email_or_password(self):
        data = {'email': 'wrong@example.com', 'senha': 'wrongpassword'}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        response = self.client.get('/api/login/logout/')
        self.assertEqual(response.status_code, 200)
