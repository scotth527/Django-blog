from django.contrib import admin

# Register your models here.
from posts.models import Post, Comment
from profiles.models import Profile, Friendship

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friendship)
admin.site.register(Profile)
