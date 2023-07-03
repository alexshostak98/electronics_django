from rest_framework.viewsets import ModelViewSet
from api.product.serializers import ProductSerializer
from product.models import Product


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
