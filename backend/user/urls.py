from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenObtainPairView, logout_view

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("logout/", logout_view, name="logout_view"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
