from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path
from django.urls import re_path
from .views import IndexView
from .apps.produtos.views import ProdutosView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^api/", include("api.urls")),
    path('', IndexView.as_view(), name="index"),
    path('produtos/', ProdutosView.as_view(), name="produtos")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)