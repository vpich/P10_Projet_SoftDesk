from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issuetrackingsystem.models import Project, Issue, Comment, Contributor
from issuetrackingsystem.serializers import ProjectDetailSerializer, IssueDetailSerializer, \
    CommentDetailSerializer, ContributorDetailSerializer, \
    ProjectListSerializer, CommentListSerializer, IssueListSerializer, ContributorListSerializer
from issuetrackingsystem.permissions import IsAdminAuthenticated

# def get_contributor_permission(self, instance):
#     contributor = Contributor.objects.get(project=instance, user=self.request.user)
#     if contributor.role == contributor.Role.CREATOR:
#         return


def check_owner(instance, user):
    if type(instance) == Project:
        contributor = Contributor.objects.get(project=instance, user=user)
        if contributor.role == contributor.Role.CREATOR:
            return True
        return False
    else:
        if instance.objects.filter(author_user_id=user):
            return True
        return False


def check_user_in_contrib(instance, user):
    contributor = Contributor.objects.filter(project=instance, user=user)
    if contributor:
        return True
    else:
        return False


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CustomViewset(ModelViewSet):

    def perform_create(self, serializer):
        instance = self.get_object()
        if type(instance) != Project:
            instance = instance.project
        user = self.request.user
        if check_user_in_contrib(instance, user):
            serializer.save()
        else:
            raise ValueError("Vous ne pouvez pas créer d'objet si vous n'êtes pas contributeur du projet")

    def perform_update(self, serializer):
        instance = self.get_object()
        if type(instance) != Project:
            instance = instance.project
        user = self.request.user
        if check_user_in_contrib(instance, user) and check_owner(instance, user):
            return serializer.save()
        else:
            raise ValueError("Vous ne pouvez pas modifier un élement dont vous n'êtes pas le créateur")

    def perform_destroy(self, instance):
        instance = self.get_object()
        if type(instance) != Project:
            instance = instance.project
        user = self.request.user
        if check_user_in_contrib(instance, user) and check_owner(instance, user):
            return self.perform_destroy(instance)
        else:
            raise ValueError("Vous ne pouvez pas supprimer un élément dont vous n'êtes pas le créateur")


def create_contributor(user, project):
    contributor = Contributor.objects.create(user=user, project=project)
    contributor.role = contributor.Role.CREATOR
    return contributor.save()


class ProjectAdminViewset(ModelViewSet):

    serializer_class = ProjectDetailSerializer

    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        project_save = serializer.save()
        project = Project.objects.get(id=project_save.id)
        user = self.request.user
        create_contributor(user, project)


class IssueAdminViewset(ModelViewSet):

    serializer_class = IssueDetailSerializer

    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Issue.objects.all()


class CommentAdminViewset(ModelViewSet):

    serializer_class = CommentDetailSerializer

    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()


class ContributorAdminViewset(ModelViewSet):

    serializer_class = ContributorDetailSerializer

    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Contributor.objects.all()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        contributor = Contributor.objects.filter(user=self.request.user)
        return Project.objects.filter(contributors__in=contributor)

    def perform_create(self, serializer):
        project_save = serializer.save()
        project = Project.objects.get(id=project_save.id)
        user = self.request.user
        create_contributor(user, project)


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        # TODO: attention: page d'erreur si l'utilisateur est anonyme
        return Contributor.objects.filter(user=self.request.user)


class IssueViewset(MultipleSerializerMixin, CustomViewset):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        contributor = Contributor.objects.filter(user=self.request.user)
        return Issue.objects.filter(project__contributors__in=contributor)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        contributor = Contributor.objects.filter(user=self.request.user)
        return Comment.objects.filter(issue_id__project__contributors__in=contributor)
