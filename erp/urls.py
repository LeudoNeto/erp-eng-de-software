from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path
from django.urls import re_path
from .apps.login.views import LoginView
from .views import IndexView
from .apps.produtos.views import ProdutosView
from .apps.movimentacoes.historico.views import HistoricoView
from .apps.movimentacoes.vendas.views import VendasView
from .apps.movimentacoes.compras.views import ComprasView
from .apps.estoque.visao_geral.views import EstoqueVisaoGeralView
from .apps.financeiro.comprovantes.views import ComprovanteView, ComprovanteDetailView
from .apps.financeiro.notas_fiscais.views import NotaFiscalView, NotaFiscalDetailView
from .apps.administrativo.gerenciar_funcionarios.views import FuncionariosView
from .apps.administrativo.gerenciar_cargos.views import CargoView
from .apps.administrativo.dados_empresa.views import DadosEmpresaView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^api/", include("api.urls")),
    path('login/', LoginView.as_view(), name="login"),
    path('', IndexView.as_view(), name="index"),
    path('produtos/', ProdutosView.as_view(), name="produtos"),
    path('movimentacoes/', HistoricoView.as_view(), name="historico_movimentacoes"),
    path('vendas/', VendasView.as_view(), name="vendas"),
    path('compras/', ComprasView.as_view(), name="compras"),
    path('estoque/', EstoqueVisaoGeralView.as_view(), name="estoque_visao_geral"),
    path('funcionarios/', FuncionariosView.as_view(), name="funcionarios"),
    path('cargos/', CargoView.as_view(), name="cargos"),
    path('dados_empresa/', DadosEmpresaView.as_view(), name="dados_empresa"),
    path('financeiro/comprovantes/', ComprovanteView.as_view(), name="financeiro_comprovantes"),
    path('financeiro/comprovantes/<int:id>', ComprovanteDetailView.as_view(), name="comprovante_detail"),
    path('financeiro/notas_fiscais/', NotaFiscalView.as_view(), name="financeiro_notas_fiscais"),
    path('financeiro/notas_fiscais/<int:id>', NotaFiscalDetailView.as_view(), name="nota_fiscal_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATICFILES_DIRS[0], document_root=settings.STATICFILES_DIRS[0])
