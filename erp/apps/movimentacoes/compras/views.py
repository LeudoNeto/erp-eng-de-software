from erp.views import ErpTemplateView

from api.movimentacoes.models import transacao, produto_transacao
from api.produtos.models import produto
from api.produtos_estoque.models import produto_estoque

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class ComprasView(ErpTemplateView):
    template_name = 'movimentacoes/compras/compras.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Compras'
        context['menu_atual'] = 'movimentacoes'
        context['link_atual'] = 'compras'

        transacoes = transacao.objects.filter(tipo__in = ['c', 'r']).order_by('-id')
        for transaction in transacoes:            
            transaction.valor_total_pago = locale.currency(transaction.valor_total_pago, grouping=True, symbol=None)
            transaction.produtos_entrada = sum(transaction.produto_transacao_set.filter(tipo='e').values_list("quantidade", flat=True))

        context['transacoes'] = transacoes

        context['produtos'] = produto.objects.filter(empresa=self.request.user.empresa)
        context['produtos_estoque'] = produto_estoque.objects.filter(empresa=self.request.user.empresa).values(
            "id", "produto_id", "produto__nome", "produto__foto", "quantidade", "valor_custo", "valor_venda", "localizacao"
        )

        return context