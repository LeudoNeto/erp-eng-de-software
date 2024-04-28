from django.urls import path, include
from rest_framework import routers

from .autenticacao.views import LoginViewSet, CargoViewSet
from .usuarios.views import UsuarioViewSet
from .empresas.views import EmpresaViewSet
from .produtos.views import ProdutoViewSet
from .movimentacoes.views import TransacaoViewSet, VendaViewSet, CompraViewSet, TrocaViewSet
from .produtos_estoque.views import ProdutoEstoqueViewSet
from .comprovantes.views import ComprovanteViewSet
from .notas_fiscais.views import NotaFiscalViewSet

router = routers.DefaultRouter()
router.register(r"login", LoginViewSet, basename="login")
router.register(r"usuarios", UsuarioViewSet, basename="usuarios")
router.register(r"empresas", EmpresaViewSet, basename="empresas")
router.register(r"cargos", CargoViewSet, basename="cargos")
router.register(r"produtos", ProdutoViewSet, basename="produtos")
router.register(r"movimentacoes", TransacaoViewSet, basename="movimentacoes")
router.register(r"vendas", VendaViewSet, basename="vendas")
router.register(r"compras", CompraViewSet, basename="compras")
router.register(r"trocas", TrocaViewSet, basename="trocas")
router.register(r"produtos_estoque", ProdutoEstoqueViewSet, basename="produtos_estoque")
router.register(r"comprovantes", ComprovanteViewSet, basename="comprovantes")
router.register(r"notas_fiscais", NotaFiscalViewSet, basename="notas_fiscais")

urlpatterns = [path("", include(router.urls))]