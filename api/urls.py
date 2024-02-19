from django.urls import path, include
from rest_framework import routers

from .produtos.views import ProdutoViewSet

router = routers.DefaultRouter()
router.register(r"produtos", ProdutoViewSet, basename="produtos")

urlpatterns = [path("", include(router.urls))]