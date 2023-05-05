from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

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


class ProjectAdminViewset(ModelViewSet):

    serializer_class = ProjectDetailSerializer

    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Project.objects.all()


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
