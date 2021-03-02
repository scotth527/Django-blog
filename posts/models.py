from django.db import models
from django.shortcuts import render, get_object_or_404
# Create your models here.
import datetime
# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, default="U+1F44D")
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.reaction

class Post(models.Model):
    post_body = models.CharField(max_length=200)
    post_title = models.CharField(max_length=120)
    pub_date = models.DateTimeField('date published', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reactions = GenericRelation(Reaction)

    def __str__(self):
        return self.post_title

    def was_published_recently(self):
       now = timezone.now()
       return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Comment(models.Model):
    comment_body = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    created_date = models.DateTimeField('date created', null=True, auto_now_add=True,blank=True )
    reactions = GenericRelation(Reaction)

    def __str__(self):
        return self.comment_body

