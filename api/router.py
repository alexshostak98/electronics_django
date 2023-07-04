from rest_framework import routers
from api.company.views import CompanyViewSet
from api.product.views import ProductViewSet
from api.employee.views import EmployeeViewSet

api_router = routers.DefaultRouter()

api_router.register('company', CompanyViewSet)
api_router.register('product', ProductViewSet)
api_router.register('employee', EmployeeViewSet)
