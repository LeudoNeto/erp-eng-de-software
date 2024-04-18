from django.views.generic import TemplateView
from django.shortcuts import redirect

from api.usuarios.models import usuario

class LoginView(TemplateView):
    template_name = 'login/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Login'

        return context