from rest_framework.serializers import ModelSerializer, SerializerMethodField
from issuetrackingsystem.models import Project, Issue, Comment, Contributor


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["comment_id", "description", "author_user_id", "issue_id"]
        read_only_fields = ("author_user_id",)


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("author_user_id", "issue_id")


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ["id", "title", "project_id", "comments"]
        read_only_fields = ("comments",)


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ("author_user_id", "project_foreign_key", "project_id")

    def get_comments(self, instance):
        try:
            queryset = instance.comments.all()
            serializer = CommentListSerializer(queryset, many=True)
            return serializer.data
        except AttributeError:
            return []


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["project_id", "title", "description"]


class ProjectDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()
    contributors = SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("author_user_id", "project_id")

    def get_issues(self, instance):
        try:
            queryset = instance.issues.all()
            serializer = IssueListSerializer(queryset, many=True)
            return serializer.data
        except AttributeError:
            return []

    def get_contributors(self, instance):
        try:
            queryset = instance.contributors.all()
            serializer = ContributorListSerializer(queryset, many=True)
            return serializer.data
        except AttributeError:
            return []


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ["id", "user_id", "project_id"]


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = "__all__"
        read_only_fields = ("user_id", "project_foreign_key", "role", "permission", "project_id")
