from rest_framework.permissions import BasePermission, SAFE_METHODS
from issuetrackingsystem.models import Contributor, Issue, Comment


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


def get_project(obj):
    if type(obj) == Issue:
        obj = obj.project_foreign_key
    elif type(obj) == Comment:
        obj = obj.issue_id.project_foreign_key
    elif type(obj) == Contributor:
        obj = obj.project_foreign_key
    return obj


def get_kwargs(view):
    try:
        return Issue.objects.get(id=view.kwargs["issue_pk"]).project_id
    except KeyError:
        return view.kwargs["project_pk"]


class IsUserContributor(BasePermission):

    def has_permission(self, request, view):
        try:
            Contributor.objects.get(project_id=get_kwargs(view), user_foreign_key=request.user)
        except Contributor.DoesNotExist:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        try:
            Contributor.objects.get(project_foreign_key=get_project(obj), user_foreign_key=request.user)
        except Contributor.DoesNotExist:
            return False
        return True


class HasContributorWritePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if type(obj) == Contributor:
            return obj.role == Contributor.Role.CREATOR


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user_id == request.user


class HasProjectWritePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        try:
            contributor = Contributor.objects.get(project_foreign_key=obj, user_foreign_key=request.user)
        except Contributor.DoesNotExist:
            return False
        return contributor.permission == Contributor.Permission.CRUD
