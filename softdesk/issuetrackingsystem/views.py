from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issuetrackingsystem.models import Project, Issue, Comment, Contributor
from issuetrackingsystem.serializers import ProjectDetailSerializer, IssueDetailSerializer, \
    CommentDetailSerializer, ContributorDetailSerializer, \
    ProjectListSerializer, CommentListSerializer, IssueListSerializer, ContributorListSerializer
from issuetrackingsystem.permissions import IsAdminAuthenticated


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


def create_contributor(user, project):
    # if Contributor.objects.filter(
    #     project=project,
    #     user=user,
    # ):
    #     return
    # if Contributor.objects.filter(project=project):
    #     contributor = Contributor.objects.create(user=user, project=project)
    #     contributor.role = "ASSIGNEE"
    #     return contributor.save()
    # else:
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

    def perform_update(self, serializer):
        instance = self.get_object()
        contributor = Contributor.objects.get(project=instance, user=self.request.user)
        if contributor.role == contributor.Role.CREATOR:
            serializer.save()
        else:
            raise ValueError("Vous ne pouvez pas modifier un élément dont vous n'êtes pas le créateur")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            contributor = Contributor.objects.get(project=instance, user=self.request.user)
            if contributor.role == contributor.Role.CREATOR:
                self.perform_destroy(instance)
        except Exception as e:
            raise e
        return Response


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        return Contributor.objects.filter(user=self.request.user)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

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
