from django.urls import path, include
from rest_framework_nested import routers

from issuetrackingsystem.views import (
    ProjectViewset,
    ContributorViewset,
    IssueViewset,
    CommentViewset,
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

urlpatterns = [
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
]
