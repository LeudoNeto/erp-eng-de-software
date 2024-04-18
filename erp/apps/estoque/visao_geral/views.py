from erp.views import ErpTemplateView

from api.produtos_estoque.models import (
    produto_estoque,
    produto_estoque_transacao
)
from api.produtos.models import produto


class EstoqueVisaoGeralView(ErpTemplateView):
    template_name = 'estoque/visao_geral/visao_geral.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Visão Geral'
        context['link_atual'] = 'estoque_visao_geral'

        context['produtos_estoque'] = produto_estoque.objects.filter(empresa=self.request.user.empresa).values(
            "id", "produto__nome", "produto__foto", "descricao",
            "quantidade", "valor_custo", "valor_venda", "localizacao"
        )
        context['produtos'] = produto.objects.filter(empresa=self.request.user.empresa).values("id", "nome")


        return context