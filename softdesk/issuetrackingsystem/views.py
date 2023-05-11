from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from issuetrackingsystem.models import Project, Issue, Comment, Contributor
from issuetrackingsystem.serializers import ProjectDetailSerializer, IssueDetailSerializer, \
    CommentDetailSerializer, ContributorDetailSerializer, \
    ProjectListSerializer, CommentListSerializer, IssueListSerializer, ContributorListSerializer
from issuetrackingsystem.permissions import IsAdminAuthenticated, IsUserContributor, \
    IsAuthor, HasContributorWritePermission, HasProjectWritePermission


def create_contributor(user, project):
    contributor = Contributor.objects.create(
        user_foreign_key=user,
        project_foreign_key=project,
        user_id=user.user_id,
        project_id=project.project_id
    )
    contributor.role = contributor.Role.CREATOR
    contributor.permission = Contributor.Permission.CRUD
    return contributor.save()


class CreateModelMixin:

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(project_id=self.request.data.get("project_id"))
        if Contributor.objects.filter(project_foreign_key=project, user_foreign_key=self.request.user):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        message = "Vous ne pouvez pas créer d'objet si vous n'êtes pas contributeur du projet"
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.detail_serializer_class is not None:
            if self.action == "retrieve":
                return self.detail_serializer_class
            elif self.action == "create":
                return self.detail_serializer_class
            elif self.action == "update":
                return self.detail_serializer_class
            elif self.action == "partial_update":
                return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectAdminViewset(ModelViewSet):

    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        project_save = serializer.save()
        project = Project.objects.get(project_id=project_save.pk)
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

    permission_classes = [IsAuthenticated, IsUserContributor, HasProjectWritePermission]

    def get_queryset(self):
        contributor = Contributor.objects.filter(user_id=self.request.user.user_id)
        return Project.objects.filter(contributors__in=contributor)

    def perform_create(self, serializer):
        project_save = serializer.save()
        project = Project.objects.get(project_id=project_save.project_id)
        user = self.request.user
        create_contributor(user, project)


class ContributorViewset(MultipleSerializerMixin, CreateModelMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    permission_classes = [IsAuthenticated, IsUserContributor, HasContributorWritePermission]

    def get_queryset(self):
        return Contributor.objects.filter(user_id=self.request.user.user_id)


class IssueViewset(MultipleSerializerMixin, CreateModelMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated, IsUserContributor, IsAuthor]

    def get_queryset(self):
        contributors = Contributor.objects.filter(user_id=self.request.user.user_id)
        return Issue.objects.filter(project_foreign_key__contributors__in=contributors)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    permission_classes = [IsAuthenticated, IsUserContributor, IsAuthor]

    def get_queryset(self):
        contributor = Contributor.objects.filter(user_id=self.request.user.user_id)
        return Comment.objects.filter(issue_id__project_foreign_key__contributors__in=contributor)

    def create(self, request, *args, **kwargs):
        project = Issue.objects.get(id=self.request.data.get("issue_id")).project_foreign_key
        if Contributor.objects.filter(project_foreign_key=project, user_foreign_key=self.request.user):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        message = "Vous ne pouvez pas créer d'objet si vous n'êtes pas contributeur du projet"
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
