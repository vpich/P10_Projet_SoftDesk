from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from issuetrackingsystem.models import Project, Issue, Comment, Contributor
from issuetrackingsystem.serializers import (
    ProjectDetailSerializer,
    IssueDetailSerializer,
    CommentDetailSerializer,
    ContributorDetailSerializer,
    ProjectListSerializer,
    CommentListSerializer,
    IssueListSerializer,
    ContributorListSerializer
    )
from issuetrackingsystem.permissions import (
    IsUserContributor,
    IsAuthor,
    ContributorIsNotCreator,
    HasProjectWritePermission
)


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


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated, HasProjectWritePermission]

    def get_queryset(self):
        return Project.objects.filter(
            contributors__user_id=self.request.user.user_id
        )

    def perform_create(self, serializer):
        project_save = serializer.save()
        project = Project.objects.get(project_id=project_save.project_id)
        user = self.request.user
        create_contributor(user, project)
        return serializer


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    permission_classes = [
        IsAuthenticated, IsUserContributor, ContributorIsNotCreator
    ]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = Project.objects.get(project_id=self.kwargs["project_pk"])
        try:
            serializer.save(
                user_id=serializer.validated_data["user_foreign_key"].user_id,
                project_id=self.kwargs["project_pk"],
                project_foreign_key=project,
            )
        except IntegrityError as e:
            raise ValidationError({"detail": e})
        return serializer

    def perform_update(self, serializer):
        try:
            serializer.save(
                user_id=serializer.validated_data["user_foreign_key"].user_id,
            )
        except IntegrityError as e:
            raise ValidationError({"detail": e})
        return serializer


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated, IsUserContributor, IsAuthor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        try:
            project = Project.objects.get(project_id=self.kwargs["project_pk"])
            Contributor.objects.get(
                user_foreign_key=serializer.validated_data["assignee_user_id"],
                project_foreign_key=project
            )
        except Exception as e:
            raise ValidationError({"detail": e})
        serializer.save(
            author_user_id=self.request.user,
            project_id=self.kwargs["project_pk"],
            project_foreign_key=project,
        )
        return serializer

    def perform_update(self, serializer):
        try:
            project = Project.objects.get(project_id=self.kwargs["project_pk"])
            Contributor.objects.get(
                user_foreign_key=serializer.validated_data["assignee_user_id"],
                project_foreign_key=project
            )
        except Exception as e:
            raise ValidationError({"detail": e})
        serializer.save(
            project_id=self.kwargs["project_pk"],
            project_foreign_key=project,
        )
        return serializer


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    permission_classes = [IsAuthenticated, IsUserContributor, IsAuthor]

    def get_queryset(self):
        try:
            Issue.objects.get(id=self.kwargs["issue_pk"])
        except Issue.DoesNotExist as e:
            raise ValidationError({"detail": e})
        return Comment.objects.filter(issue_id=self.kwargs["issue_pk"])

    def perform_create(self, serializer):
        try:
            issue = Issue.objects.get(id=self.kwargs["issue_pk"])
        except Issue.DoesNotExist as e:
            raise ValidationError({"detail": e})
        serializer.save(
            author_user_id=self.request.user,
            issue_id=issue,
        )
        return serializer
