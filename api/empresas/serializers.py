from rest_framework import serializers
from .models import empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = empresa
        exclude = ["id"]