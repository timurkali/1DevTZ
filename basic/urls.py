from django.urls import path, include
from rest_framework.routers import DefaultRouter

from basic import views

router = DefaultRouter()
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'order-line', views.OrderLineViewSet, basename='order_line')
router.register(r'order', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
