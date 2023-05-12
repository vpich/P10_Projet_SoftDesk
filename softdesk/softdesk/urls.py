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
from rest_framework_nested import routers

from issuetrackingsystem.views import ProjectAdminViewset, IssueAdminViewset, CommentAdminViewset, ContributorAdminViewset, \
    ProjectViewset, ContributorViewset, IssueViewset, CommentViewset
from authentication.views import UserAdminViewset, SignupView

router = routers.SimpleRouter()
router.register("projects", ProjectViewset, basename="projects")

projects_router = routers.NestedSimpleRouter(
    router,
    r"projects",
    lookup="project"
)
projects_router.register(r"issues", IssueViewset, basename="issues")
projects_router.register(r"users", ContributorViewset, basename="contributors")
issues_router = routers.NestedSimpleRouter(
    projects_router,
    r"issues",
    lookup="issue"
)
issues_router.register(r"comments", CommentViewset, basename="comments")


router_admin = routers.SimpleRouter()
router_admin.register("user", UserAdminViewset, basename="user")
router_admin.register("projects", ProjectAdminViewset, basename="projects")
router_admin.register("issues", IssueAdminViewset, basename="issues")
router_admin.register("comments", CommentAdminViewset, basename="comments")
router_admin.register("contributor", ContributorAdminViewset, basename="contributor")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("rest_framework.urls")),
    path("api/admin/", include(router_admin.urls)),
    path("api/", include(router.urls)),
    path("api/", include(projects_router.urls)),
    path("api/", include(issues_router.urls)),
    path("signup/", SignupView.as_view()),
]
