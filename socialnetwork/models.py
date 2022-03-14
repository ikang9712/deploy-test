from asyncio import create_subprocess_exec
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    creation_time = models.DateTimeField()

class Comment(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    creation_time = models.DateTimeField()
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    bio = models.CharField(max_length=200)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    following = models.ManyToManyField(User, related_name="following")
