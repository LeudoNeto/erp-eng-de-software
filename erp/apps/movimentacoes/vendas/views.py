from erp.views import ErpTemplateView

from api.movimentacoes.models import transacao, produto_transacao
from api.produtos.models import produto
from api.produtos_estoque.models import produto_estoque
from api.usuarios.models import usuario

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class VendasView(ErpTemplateView):
    template_name = 'movimentacoes/vendas/vendas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Vendas'
        context['menu_atual'] = 'movimentacoes'
        context['link_atual'] = 'vendas'

        transacoes = transacao.objects.filter(tipo__in = ['v', 'p']).order_by('-id')
        for transaction in transacoes:            
            transaction.valor_total_recebido = locale.currency(transaction.valor_total_recebido, grouping=True, symbol=None)
            transaction.produtos_saida = sum(transaction.produto_transacao_set.filter(tipo='s').values_list("quantidade", flat=True))

        context['transacoes'] = transacoes

        context['produtos'] = produto.objects.filter(empresa=self.request.user.empresa)
        context['produtos_estoque'] = produto_estoque.objects.filter(empresa=self.request.user.empresa).values(
            "id", "produto_id", "produto__nome", "produto__foto", "quantidade", "valor_custo", "valor_venda", "localizacao"
        )

        context['vendedores'] = usuario.objects.filter(empresa=self.request.user.empresa)

        return context