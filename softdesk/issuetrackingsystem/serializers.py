from rest_framework.serializers import ModelSerializer, SerializerMethodField
from issuetrackingsystem.models import Project, Issue, Comment, Contributor
from authentication.models import User


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "description", "author_user_id", "issue_id"]
        read_only_fields = ("author_user_id",)


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("author_user_id",)

    def create(self, validated_data):
        validated_data["author_user_id"] = User.objects.get(id=self.context["request"].user.id)
        return Comment.objects.create(**validated_data)


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
        read_only_fields = ("author_user_id", "project_foreign_key")

    def get_comments(self, instance):
        try:
            queryset = instance.comments.all()
            serializer = CommentDetailSerializer(queryset, many=True)
            return serializer.data
        except AttributeError:
            return []

    def create(self, validated_data):
        validated_data["author_user_id"] = User.objects.get(email=self.context["request"].user)
        validated_data["project_foreign_key"] = Project.objects.get(project_id=validated_data["project_id"])
        return Issue.objects.create(**validated_data)


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
            serializer = IssueDetailSerializer(queryset, many=True)
            return serializer.data
        except AttributeError:
            return []

    def get_contributors(self, instance):
        try:
            queryset = instance.contributors.all()
            serializer = ContributorDetailSerializer(queryset, many=True)
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
        read_only_fields = ("user_foreign_key", "project_foreign_key", "role", "permission")

    def create(self, validated_data):
        validated_data["user_foreign_key"] = User.objects.get(user_id=validated_data["user_id"])
        validated_data["project_foreign_key"] = Project.objects.get(project_id=validated_data["project_id"])
        return Contributor.objects.create(**validated_data)
