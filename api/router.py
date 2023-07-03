from rest_framework import routers
from api.company.views import CompanyViewSet
from api.product.views import ProductViewSet

api_router = routers.DefaultRouter()

api_router.register('company', CompanyViewSet)
api_router.register('product', ProductViewSet)
