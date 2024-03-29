from django.db import models
from django.db.models import Q
from Images import *
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin
from base.utils.ChoiceFields import *
from rest_framework.authtoken.models import Token
from base.utils.document_upload import task_document_path, validate_file_size, validate_extension


class MainUser(AbstractUser):
    projects = models.ManyToManyField('Project', through='ProjectMember', related_name='participants')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_login}'

    @property
    def my_projects(self):
        return self.projects

    @property
    def tasks_count(self):
        return self.assigned_tasks.count()

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, default='none')
    address = models.CharField(max_length=300, default='none')
    web_site = models.CharField(max_length=300, default='none')
    avatar = models.FileField(default='Images/Default.png')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description? You can add one!")
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="created_projects")

    @property
    def block_count(self):
        return self.blocks.count()

    @property
    def members_count(self):
        return self.participants.count()

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="membership")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="membership")

    class Meta:
        unique_together = ('user', 'project',)


class BlockStatusManager(models.Manager):
    def todo_tasks(self):
        return super().get_queryset().filter(type=STATUS_TODO)

    def in_progress_tasks(self):
        return super().get_queryset().filter(type=STATUS_IN_PROGRESS)

    def done_tasks(self):
        return super().get_queryset().filter(type=STATUS_DONE)

    def new_tasks(self):
        return super().get_queryset().filter(type=STATUS_NEW)


class BlockFilledManager(models.Manager):
    def not_empty(self):
        return super().get_queryset().exclude(Q(tasks_count__lte=0))


class Block(models.Model):
    name = models.CharField(max_length=300)
    type = models.IntegerField(choices=STATUS_CHOICES, default=4)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="blocks")
    objects = models.Manager()
    status_sort = BlockStatusManager()
    not_empty = BlockFilledManager()

    @property
    def tasks_count(self):
        return self.tasks.count()

    def __str__(self):
        return self.name + " " + str(self.project)


class TaskDispatchedManager(models.Manager):
    def dispatched(self):
        return super().get_queryset().exclude(Q(executors_count__lte=0))


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="created_tasks")
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="assigned_tasks")
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="tasks")
    priority = models.IntegerField()
    dispatched = TaskDispatchedManager()

    @property
    def documents_count(self):
        return self.documents.count()

    def __str__(self):
        return self.name + " With priority of " + str(self.priority)


class DateManager(models.Manager):
    def ordered(self):
        return super().get_queryset().order_by('created_at')

    def rev_ordered(self):
        return super().get_queryset().order_by('-created_at')


class TaskSubmission(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    timeOrder = DateManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.text}: {self.created_at}'


class TaskDocument(TaskSubmission):
    document = models.FileField(upload_to=task_document_path, validators=[validate_file_size, validate_extension])
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="documents")
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="documents")

    def __str__(self):
        return self.document.name + " added by " + str(self.creator.full_name)


class TaskComment(TaskSubmission):
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.creator.full_name + " posted at  " + str(self.created_at)
