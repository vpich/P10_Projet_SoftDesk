from django.db import models
from django.conf import settings

from authentication.models import User


class Project(models.Model):

    PROJECT = "PROJECT"
    PRODUCT = "PRODUCT"
    APPLICATION = "APPLICATION"

    TYPE_CHOICES = (
        (PROJECT, "Projet"),
        (PRODUCT, "Production"),
        (APPLICATION, "Application"),
    )

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.CharField(max_length=2048, blank=True, null=True)
    type = models.CharField(max_length=128, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="projects",
        verbose_name="Créateur",
        null=True,
    )


class Issue(models.Model):

    class Tag(models.TextChoices):
        BUG = "BUG"
        TASK = "TASK"
        IMPROVEMENT = "IMPROVEMENT"

    class Priority(models.TextChoices):
        LOW = "L"
        MEDIUM = "M"
        HIGH = "H"

    class Status(models.TextChoices):
        TODO = "T"
        IN_PRODUCTION = "IP"
        DONE = "D"

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True, null=True)
    tag = models.CharField(max_length=128, choices=Tag.choices)
    priority = models.CharField(max_length=128, choices=Priority.choices)
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    # project_id = project.objects.pk
    status = models.CharField(max_length=128, choices=Status.choices)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="issues",
        null=True,
    )
    assignee_user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="issues_assigned",
        blank=True,
        null=True,
    )
    # assignee_user_id =

    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
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
    # Possède les attributs user_id et project_id
    # peut avoir plusieurs users et plusieurs projects ?

    class Role(models.TextChoices):
        CREATOR = "CREATOR"
        ASSIGNEE = "ASSIGNEE"

    class Permission(models.TextChoices):
        CREATE = "CREATE"
        READ = "READ"
        UPDATE = "UPDATE"
        DELETE = "DELETE"

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="participants",
    )

    permission = models.CharField(max_length=50, choices=Permission.choices, verbose_name="Permission")
    role = models.CharField(max_length=128, choices=Role.choices, verbose_name="Rôle")

    # def permission(self):
    #     if self.role == self.Role.CREATOR:
    #         return self.Permission.CREATE
    #     elif self.role == self.Role.ASSIGNEE:
    #         return self.Permission.READ

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="project",
    )

    class Meta:
        unique_together = ("user", "project")
