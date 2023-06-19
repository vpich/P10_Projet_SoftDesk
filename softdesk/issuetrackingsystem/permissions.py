from rest_framework.permissions import BasePermission, SAFE_METHODS
from issuetrackingsystem.models import Contributor, Issue, Comment, Project
from rest_framework.exceptions import NotFound


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
        Project.objects.get(project_id=view.kwargs["project_pk"])
        return view.kwargs["project_pk"]
    except Project.DoesNotExist:
        raise NotFound


class IsUserContributor(BasePermission):

    def has_permission(self, request, view):
        try:
            Contributor.objects.get(
                project_id=get_kwargs(view),
                user_foreign_key=request.user
            )
        except Contributor.DoesNotExist:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        try:
            Contributor.objects.get(
                project_foreign_key=get_project(obj),
                user_foreign_key=request.user
            )
        except Contributor.DoesNotExist:
            return False
        return True


class ContributorIsNotCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.role != Contributor.Role.CREATOR


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
            contributor = Contributor.objects.get(
                project_foreign_key=obj,
                user_foreign_key=request.user
            )
        except Contributor.DoesNotExist:
            return False
        return contributor.permission == Contributor.Permission.CRUD
