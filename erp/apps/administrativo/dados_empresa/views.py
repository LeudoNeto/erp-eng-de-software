from erp.views import ErpTemplateView

from api.empresas.models import empresa

class DadosEmpresaView(ErpTemplateView):
    template_name = 'administrativo/dados_empresa/dados_empresa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Dados da Empresa'
        context['menu_atual'] = 'administrativo'
        context['link_atual'] = 'dados_empresa'

        context['empresa'] = self.request.user.empresa

        return context