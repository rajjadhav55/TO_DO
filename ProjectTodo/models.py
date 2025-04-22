# ProjectTodo/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
   
    contact_no = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username


from django.conf import settings

class Task(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
