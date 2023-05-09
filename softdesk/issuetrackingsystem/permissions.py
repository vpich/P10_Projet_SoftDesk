from rest_framework.permissions import BasePermission, SAFE_METHODS
from issuetrackingsystem.models import Project, Contributor, Issue, Comment


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


def get_project(obj):
    if type(obj) == Issue:
        obj = obj.project
    elif type(obj) == Comment:
        obj = obj.issue_id.project
    elif type(obj) == Contributor:
        obj = obj.project
    return obj


class IsUserContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        contributor = Contributor.objects.filter(project=get_project(obj), user=request.user)
        if contributor:
            return True
        else:
            return False


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if type(obj) == Project:
            contributor = Contributor.objects.get(project=obj, user=request.user)
            return contributor.role == contributor.Role.CREATOR
        elif type(obj) == Contributor:
            return obj.role == Contributor.Role.CREATOR
        else:
            return obj.author_user_id == request.user
