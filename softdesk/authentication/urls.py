from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import SignupView, UserAdminViewset

router_admin = routers.SimpleRouter()
router_admin.register("users", UserAdminViewset, basename="admin-users")

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("admin/", include(router_admin.urls)),
    path("signup/", SignupView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
