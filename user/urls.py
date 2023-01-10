from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()
router.register(r'signup', views.SignUpViewSet, basename='signup')
router.register(r'signin', views.SignInViewSet, basename='signin')

urlpatterns = [
    path('', include(router.urls)),
]
