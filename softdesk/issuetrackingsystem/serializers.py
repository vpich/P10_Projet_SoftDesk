from rest_framework.serializers import ModelSerializer, SerializerMethodField

from issuetrackingsystem.models import Project, Issue, Comment, Contributor


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


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ["title", "project", "comments"]


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

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
            "comments",
        ]

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["title", "description"]


class ProjectDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "type",
            "author_user_id",
            "issues",
        ]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


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
