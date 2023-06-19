from django.db import models
from django.conf import settings

from authentication.models import User


class Project(models.Model):

    class Type(models.TextChoices):
        BACK_END = "BACK-END"
        FRONT_END = "FRONT-END"
        IOS = "iOS"
        ANDROID = "ANDROID"

    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=128, choices=Type.choices)


class Issue(models.Model):

    class Tag(models.TextChoices):
        BUG = "BUG"
        TASK = "TASK"
        IMPROVEMENT = "IMPROVEMENT"

    class Priority(models.TextChoices):
        LOW = "LOW"
        MEDIUM = "MEDIUM"
        HIGH = "HIGH"

    class Status(models.TextChoices):
        TO_DO = "T"
        IN_PRODUCTION = "IP"
        DONE = "D"

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True, null=True)
    tag = models.CharField(max_length=128, choices=Tag.choices)
    priority = models.CharField(max_length=128, choices=Priority.choices)
    project_id = models.IntegerField()
    project_foreign_key = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    status = models.CharField(max_length=128, choices=Status.choices)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="issues",
        null=True,
    )
    assignee_user_id = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        related_name="issues_assigned",
        default=author_user_id,
    )

    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
    )
    issue_id = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):

    class Role(models.TextChoices):
        CREATOR = "CREATOR"
        CONTRIBUTOR = "CONTRIBUTOR"

    class Permission(models.TextChoices):
        CRUD = "CREATE_READ_UPDATE_DELETE"
        CR = "CREATE_READ"

    user_id = models.IntegerField()
    user_foreign_key = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributors",
        verbose_name="Utilisateurs",
    )

    permission = models.CharField(
        max_length=50,
        choices=Permission.choices,
        verbose_name="Permission",
        default=Permission.CR
    )
    role = models.CharField(
        max_length=128,
        choices=Role.choices,
        verbose_name="Rôle",
        default=Role.CONTRIBUTOR
    )

    project_id = models.IntegerField()
    project_foreign_key = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )

    class Meta:
        unique_together = ("user_id", "project_id")
