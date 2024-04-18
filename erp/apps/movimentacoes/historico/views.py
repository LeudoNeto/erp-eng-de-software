from erp.views import ErpTemplateView

from api.movimentacoes.models import transacao, produto_transacao
from api.produtos.models import produto

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class HistoricoView(ErpTemplateView):
    template_name = 'movimentacoes/historico/historico.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Histórico'
        context['menu_atual'] = 'movimentacoes'
        context['link_atual'] = 'historico_movimentacoes'

        transacoes = transacao.objects.filter(empresa=self.request.user.empresa)
        for transaction in transacoes:
            
            transaction.valor_total_recebido = locale.currency(transaction.valor_total_recebido, grouping=True, symbol=None)
            transaction.valor_total_pago = locale.currency(transaction.valor_total_pago, grouping=True, symbol=None)

            transaction.produtos_saida = transaction.produto_transacao_set.filter(tipo='s').count()
            transaction.produtos_entrada = transaction.produto_transacao_set.filter(tipo='e').count()

        context['transacoes'] = transacoes

        context['produtos'] = produto.objects.filter(empresa=self.request.user.empresa)

        return context