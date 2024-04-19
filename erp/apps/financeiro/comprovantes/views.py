from erp.views import ErpTemplateView

from api.comprovantes.models import comprovante, comprovante_produtos
from api.produtos.models import produto
from api.usuarios.models import usuario

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

class ComprovanteView(ErpTemplateView):
    template_name = 'financeiro/comprovantes/comprovantes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Emitir Comprovante'
        context['link_atual'] = 'comprovante'

        context['comprovantes'] = comprovante.objects.filter(empresa=self.request.user.empresa)
        context['produtos'] = produto.objects.filter(empresa=self.request.user.empresa)
        context['vendedores'] = usuario.objects.filter(empresa=self.request.user.empresa)

        return context
    

class ComprovanteDetailView(ErpTemplateView):
    template_name = 'financeiro/templates_notas/comprovante_basico.html'

    def get(self, request, *args, **kwargs):
        # Renderiza o template para HTML
        html_string = render_to_string(self.template_name, self.get_context_data(**kwargs))
        
        # Converte o HTML para PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename=comprovante.pdf'
        pisa.CreatePDF(html_string, dest=response)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['comprovante'] = comprovante.objects.select_related('vendedor', 'empresa').get(id=kwargs['id'])
        context['produtos_comprovante'] = comprovante_produtos.objects.filter(comprovante=kwargs['id']).values(
            "produto__nome", "quantidade", "valor_unitario", "valor_total"
            )

        return context
