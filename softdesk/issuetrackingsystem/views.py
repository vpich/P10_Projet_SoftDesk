import http

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from issuetrackingsystem.models import Project, Issue, Comment, Contributor
from issuetrackingsystem.serializers import ProjectDetailSerializer, IssueDetailSerializer, \
    CommentDetailSerializer, ContributorDetailSerializer, \
    ProjectListSerializer, CommentListSerializer, IssueListSerializer, ContributorListSerializer
from issuetrackingsystem.permissions import IsAdminAuthenticated, IsOwnerOrReadOnly, IsUserContributor

# def get_contributor_permission(self, instance):
#     contributor = Contributor.objects.get(project=instance, user=self.request.user)
#     if contributor.role == contributor.Role.CREATOR:
#         return


# def check_owner(instance, user):
#     if type(instance) == Project:
#         contributor = Contributor.objects.get(project=instance, user=user)
#         if contributor.role == contributor.Role.CREATOR:
#             return True
#         return False
#     if type(instance) == Contributor:
#         if instance.role == Contributor.Role.CREATOR:
#             return True
#         return False
#     else:
#         if instance.author_user_id == user:
#             return True
#         return False


# def check_user_in_contrib(project, user):
#     contributor = Contributor.objects.filter(project=project, user=user)
#     if contributor:
#         return True
#     else:
#         return False


# def get_project(self):
#     obj = self.get_object()
#     if type(obj) == Issue:
#         obj = obj.project
#     elif type(obj) == Comment:
#         obj = obj.issue_id.project
#     elif type(obj) == Contributor:
#         obj = obj.project
#     return obj


class CustomViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsUserContributor]

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.request.data.get("project"))
        if Contributor.objects.filter(project=project, user=self.request.user):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        message = "Vous ne pouvez pas créer d'objet si vous n'êtes pas contributeur du projet"
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     project = Project.objects.get(id=self.request.data.get("project"))
    #     if Contributor.objects.filter(project=project, user=self.request.user):
    #         return serializer.save()
    #     # else:
    #     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         raise ValueError("Vous ne pouvez pas créer d'objet si vous n'êtes pas contributeur du projet")
#
#     def perform_update(self, serializer):
#         if check_user_in_contrib(project=get_project(self), user=self.request.user):
#                 # and check_owner(instance=self.get_object(), user=self.request.user):
#             return serializer.save()
#         else:
#             raise ValueError("Vous ne pouvez pas modifier un élement dont vous n'êtes pas le créateur")
#
#     def perform_destroy(self, instance):
#         if check_user_in_contrib(project=get_project(self), user=self.request.user):
#                 # and check_owner(instance=self.get_object(), user=self.request.user):
#             return self.perform_destroy(instance)
#         else:
#             raise ValueError("Vous ne pouvez pas supprimer un élément dont vous n'êtes pas le créateur")


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


class ProjectViewset(MultipleSerializerMixin, CustomViewset):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        contributor = Contributor.objects.filter(user=self.request.user)
        return Project.objects.filter(contributors__in=contributor)

    def perform_create(self, serializer):
        project_save = serializer.save()
        project = Project.objects.get(id=project_save.id)
        user = self.request.user
        create_contributor(user, project)


# TODO: mettre en readonly pour les détails ?
class ContributorViewset(MultipleSerializerMixin, CustomViewset):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        # TODO: attention: page d'erreur si l'utilisateur est anonyme
        return Contributor.objects.filter(user=self.request.user)


class IssueViewset(MultipleSerializerMixin, CustomViewset):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        contributors = Contributor.objects.filter(user=self.request.user)
        return Issue.objects.filter(project__contributors__in=contributors)
        # projects = [element.project for element in contributors]
        # print(projects)
        # return Issue.objects.filter(project__in=projects)


class CommentViewset(MultipleSerializerMixin, CustomViewset):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        contributor = Contributor.objects.filter(user=self.request.user)
        return Comment.objects.filter(issue_id__project__contributors__in=contributor)
        # issues = Issue.objects.filter(
        #     Q(author_user_id=self.request.user) |
        #     Q(assignee_user=self.request.user)
        # )
        # return Comment.objects.filter(
        #     Q(author_user_id=self.request.user) |
        #     Q(issue_id__in=issues)
        # )

    def create(self, request, *args, **kwargs):
        project = Issue.objects.get(id=self.request.data.get("issue_id")).project
        if Contributor.objects.filter(project=project, user=self.request.user):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        message = "Vous ne pouvez pas créer d'objet si vous n'êtes pas contributeur du projet"
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     project = Issue.objects.get(id=self.request.data.get("issue_id")).project
    #     if Contributor.objects.filter(project=project, user=self.request.user):
    #         return serializer.save()
    #     # else:
    #     #     raise ValueError("Vous ne pouvez pas créer d'objet si vous n'êtes pas contributeur du projet")
    #     return serializer.errors
