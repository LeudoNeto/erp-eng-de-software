from django.views.generic import TemplateView
from .settings import MEDIA_URL

class ErpTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["MEDIA_URL"] = MEDIA_URL
        
        return context


class IndexView(ErpTemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Página Inicial'
        context['link_atual'] = 'index'

        return context