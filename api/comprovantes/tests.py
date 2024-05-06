from erp.tests import ErpTestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import ComprovanteViewSet
from .models import comprovante, comprovante_produtos
from api.produtos.models import produto
from api.empresas.models import empresa
from api.usuarios.models import usuario
from api.autenticacao.models import Cargo
import json

class ComprovanteViewSetTestCase(ErpTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ComprovanteViewSet.as_view({'post': 'create', 'delete': 'destroy'})
        
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

    def test_create_comprovante_success(self):
        data = {
            'empresa': self.empresa.id,
            'cliente': 'Cliente Teste',
            'vendedor': self.user.id,
            'metodo_pagamento': 'd',
            'subtotal': 30.00,
            'taxas': 5.00,
            'desconto': 2.00,
            'total': 33.00,
            'produtos_comprovante': json.dumps([
                {
                    'produto': self.produto1.id,
                    'quantidade': 2,
                    'valor_unitario': 10.00,
                    'valor_total': 20.00
                },
                {
                    'produto': self.produto2.id,
                    'quantidade': 1,
                    'valor_unitario': 20.00,
                    'valor_total': 20.00
                }
            ])
        }
        request = self.factory.post('/api/comprovantes/', data, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comprovante_success(self):
        comprovante_obj = comprovante.objects.create(
            empresa=self.empresa,
            cliente='Cliente Teste',
            vendedor=self.user,
            metodo_pagamento='d',
            subtotal=30.00,
            taxas=5.00,
            desconto=2.00,
            total=33.00
        )

        comprovante_produtos.objects.create(
            comprovante=comprovante_obj,
            produto=self.produto1,
            quantidade=2,
            valor_unitario=10.00,
            valor_total=20.00
        )
        comprovante_produtos.objects.create(
            comprovante=comprovante_obj,
            produto=self.produto2,
            quantidade=1,
            valor_unitario=20.00,
            valor_total=20.00
        )

        request = self.factory.delete(f'/api/comprovantes/{comprovante_obj.id}/')
        request.user = self.user
        response = self.view(request, pk=comprovante_obj.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_nonexistent_comprovante(self):
        request = self.factory.delete('/api/comprovantes/9999/')  # ID que não existe
        request.user = self.user
        response = self.view(request, pk=9999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)