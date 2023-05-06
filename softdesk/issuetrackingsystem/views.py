from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.db.models import Q

from issuetrackingsystem.models import Project, Issue, Comment, Contributor
from issuetrackingsystem.serializers import ProjectDetailSerializer, IssueDetailSerializer, \
    CommentDetailSerializer, ContributorDetailSerializer, ProjectListSerializer
from issuetrackingsystem.permissions import IsAdminAuthenticated


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return  self.detail_serializer_class
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
    contributor.role = "CREATOR"
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


class ProjectViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()
