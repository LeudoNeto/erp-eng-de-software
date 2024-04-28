from erp.views import ErpTemplateView

from api.usuarios.models import usuario
from api.autenticacao.models import Cargo

class FuncionariosView(ErpTemplateView):
    template_name = 'administrativo/gerenciar_funcionarios/gerenciar_usuarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Histórico'
        context['menu_atual'] = 'administrativo'
        context['link_atual'] = 'gerenciar_funcionarios'

        context['usuarios'] = usuario.objects.filter(empresa=self.request.user.empresa).values(
            'id', 'nome', 'email', 'foto', 'cargo__nome', 'telefone'
        )
        context['cargos'] = Cargo.objects.filter(empresa=self.request.user.empresa).values(
            'id', 'nome'
        )

        return context