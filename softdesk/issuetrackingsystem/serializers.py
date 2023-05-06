from rest_framework.serializers import ModelSerializer, SerializerMethodField

from issuetrackingsystem.models import Project, Issue, Comment, Contributor
from authentication.models import User


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["description", "author_user_id", "issue_id"]
        read_only_fields = ("author_user_id",)


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            "description",
            "author_user_id",
            "issue_id",
            "created_time",
        ]
        read_only_fields = ("author_user_id",)

    def create(self, validated_data):
        validated_data["author_user_id"] = User.objects.get(id=self.context["request"].user.id)
        return Comment.objects.create(**validated_data)


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
        read_only_fields = ("author_user_id",)

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data

    def create(self, validated_data):
        validated_data["author_user_id"] = User.objects.get(id=self.context["request"].user.id)
        return Issue.objects.create(**validated_data)


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
        read_only_fields = ("author_user_id",)

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data

    # TODO: A retirer quand le modèle Project n'aura plus author_user_id
    def create(self, validated_data):
        validated_data["author_user_id"] = User.objects.get(id=self.context["request"].user.id)
        return Project.objects.create(**validated_data)


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ["user", "project"]


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = "__all__"
        read_only_fields = ("role", "permission",)
