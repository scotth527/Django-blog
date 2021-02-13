from posts.models import Post
from django.utils import timezone
import datetime

def create_post(body, title, author, days=0):
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.get_or_create(post_body=body, post_title=title, pub_date=time,author=author)[0]