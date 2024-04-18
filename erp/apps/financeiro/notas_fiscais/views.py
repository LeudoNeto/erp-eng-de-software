from erp.views import ErpTemplateView

from api.notas_fiscais.models import nota_fiscal, nota_fiscal_produtos
from api.produtos.models import produto

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

class NotaFiscalView(ErpTemplateView):
    template_name = 'financeiro/notas_fiscais/notas_fiscais.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Emitir Nota Fiscal'
        context['link_atual'] = 'notas_fiscais'

        context['notas_fiscais'] = nota_fiscal.objects.filter(empresa=self.request.user.empresa)
        context['produtos'] = produto.objects.filter(empresa=self.request.user.empresa)

        return context
    

class NotaFiscalDetailView(ErpTemplateView):
    template_name = 'financeiro/templates_notas/nota_fiscal_basica.html'

    def get(self, request, *args, **kwargs):
        # Renderiza o template para HTML
        html_string = render_to_string(self.template_name, self.get_context_data(**kwargs))
        
        # Converte o HTML para PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename=nota_fiscal.pdf'
        pisa.CreatePDF(html_string, dest=response)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['nota_fiscal'] = nota_fiscal.objects.get(id=kwargs['id'])
        context['nota_fiscal_produtos'] = nota_fiscal_produtos.objects.filter(nota_fiscal=kwargs['id']).values(
            "id", "produto__nome", "produto__codigo_referencia", "quantidade", "valor_unitario", "valor_total", "valor_icms", "produto__aliquota_icms"
            )

        return context
