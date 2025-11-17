from django.db import models
from django.conf import settings

class Project(models.Model):
    NAME_MAX_LEN = 100

    name = models.CharField(max_length=NAME_MAX_LEN)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_projects",
    )
    users = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        blank=True,
        related_name="joined_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Task(models.Model):
    NAME_MAX_LEN = 200
    STATUS_TODO = 1
    STATUS_TODO_LABEL = "To Do"
    STATUS_IN_PROGRESS = 2
    STATUS_IN_PROGRESS_LABEL = "In Progress"
    STATUS_DONE = 3
    STATUS_DONE_LABEL = "Done"

    STATUS_CHOICES = [
        (STATUS_TODO, STATUS_TODO_LABEL),
        (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS_LABEL),
        (STATUS_DONE, STATUS_DONE_LABEL),
    ]

    name = models.CharField(max_length=NAME_MAX_LEN, db_index=True)
    description = models.TextField(blank=True, default="")
    status = models.IntegerField(default=STATUS_TODO, choices=STATUS_CHOICES)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through="UserTask",
        through_fields=("task", "user"),
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class UserTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["task", "user"], name="unique_task_user"),
        ]
