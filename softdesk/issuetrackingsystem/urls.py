from django.urls import path, include
from rest_framework_nested import routers

from issuetrackingsystem.views import (
    ProjectViewset,
    ContributorViewset,
    IssueViewset,
    CommentViewset,
    ProjectAdminViewset,
    IssueAdminViewset,
    CommentAdminViewset,
    ContributorAdminViewset
)

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
router_admin.register("projects",
                      ProjectAdminViewset,
                      basename="admin-projects")
router_admin.register("issues",
                      IssueAdminViewset,
                      basename="admin-issues")
router_admin.register("comments",
                      CommentAdminViewset,
                      basename="admin-comments")
router_admin.register("contributors",
                      ContributorAdminViewset,
                      basename="admin-contributors")

urlpatterns = [
    path("admin/", include(router_admin.urls)),
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
]
