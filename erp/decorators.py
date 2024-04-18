from django.shortcuts import redirect
from functools import wraps

def permissao_required(permissao):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.cargo.filter(permissoes__codename=permissao).exists():
                    return view_func(request, *args, **kwargs)
            return redirect('/login/')
        return _wrapped_view
    return decorator