from rest_framework.serializers import ModelSerializer

from issuetrackingsystem.models import Project, Issue, Comment, Contributor


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["title", "author_user_id"]


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "type",
            "author_user_id",
        ]


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ["title", "project"]


class IssueDetailSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "project",
            "author_user_id",
            "assignee_user",
            "created_time",
        ]


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["description", "author_user_id"]


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            "description",
            "author_user_id",
            "issue_id",
            "created_time",
        ]


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ["user", "project"]


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = [
            "user",
            "project",
            "permission",
            "role",
        ]
