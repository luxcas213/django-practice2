from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateCompletaed = models.DateTimeField(null=True)
    important = models.BooleanField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " - "+ self.user.username

