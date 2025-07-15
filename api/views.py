from django.shortcuts import render
from rest_framework import viewsets, permissions
from perfil.models import SavedProduct
from .serializers import SavedProductSerializer
from .authentication import ApiKeyAuthentication
from product.models import Product
from django.contrib.auth import get_user_model
from rest_framework.response import Response

class SavedProductViewSet(viewsets.ModelViewSet):
    queryset = SavedProduct.objects.all()
    serializer_class = SavedProductSerializer
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        try:
            User = get_user_model()
            user = User.objects.get(pk=user_id)
            product = Product.objects.get(pk=product_id)
        except (User.DoesNotExist, Product.DoesNotExist):
            return Response({'error': 'Usuario o producto no existe.'}, status=400)
        obj, created = SavedProduct.objects.get_or_create(user=user, product=product)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=201 if created else 200)

# Create your views here.
