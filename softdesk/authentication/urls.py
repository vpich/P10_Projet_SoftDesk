from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from authentication.views import SignupView

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("signup/", SignupView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
