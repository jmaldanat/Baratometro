from rest_framework import serializers
from perfil.models import SavedProduct

class SavedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedProduct
        fields = ['id', 'user', 'product', 'created_at']