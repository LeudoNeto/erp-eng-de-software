from erp.views import ErpTemplateView

from api.produtos.models import produto

class ProdutosView(ErpTemplateView):
    template_name = 'produtos/produtos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Produtos'
        context['link_atual'] = 'produtos'

        context['produtos'] = produto.objects.all()

        return context