from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from base.ChoiceFields import STATUS_CHOICES
from django.utils import timezone
from rest_framework.authtoken.models import Token


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    address = models.CharField(max_length=300)
    web_site = models.CharField(max_length=300)
    # avatar = models.FileField()

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class Project_member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Block(models.Model):
    name = models.CharField(max_length=300)
    type = models.IntegerField(choices=STATUS_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdtasks")
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignedtasks")
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    order = models.IntegerField()


class Task_document(models.Model):
    document = models.FileField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Task_comment(models.Model):
    body = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
