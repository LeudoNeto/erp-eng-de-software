from erp.views import ErpTemplateView

from api.autenticacao.models import Cargo

class CargoView(ErpTemplateView):
    template_name = 'administrativo/gerenciar_cargos/gerenciar_cargos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Gerenciar Cargos'
        context['menu_atual'] = 'administrativo'
        context['link_atual'] = 'gerenciar_cargos'

        context['cargos'] = Cargo.objects.filter(empresa=self.request.user.empresa)

        return context