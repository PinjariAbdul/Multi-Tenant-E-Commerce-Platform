from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, CustomerOrderViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')
router.register('my-orders', CustomerOrderViewSet, basename='customer-order')

urlpatterns = [
    path('', include(router.urls)),
]
