"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from issuetrackingsystem.views import ProjectAdminViewset, IssueAdminViewset, CommentAdminViewset, ContributorAdminViewset, \
    ProjectViewset, ContributorViewset, IssueViewset, CommentViewset
from authentication.views import UserAdminViewset

router = routers.SimpleRouter()
router.register("project", ProjectViewset, basename="project")
router.register("contributor", ContributorViewset, basename="contributor")
router.register("issue", IssueViewset, basename="issue")
router.register("comment", CommentViewset, basename="comment")

router_admin = routers.SimpleRouter()
router_admin.register("user", UserAdminViewset, basename="user")
router_admin.register("project", ProjectAdminViewset, basename="project")
router_admin.register("issue", IssueAdminViewset, basename="issue")
router_admin.register("comment", CommentAdminViewset, basename="comment")
router_admin.register("contributor", ContributorAdminViewset, basename="contributor")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/admin/", include(router_admin.urls)),
    path("api/", include(router.urls)),
]
