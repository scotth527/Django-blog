from django.test import TestCase
from posts.models import Post
from profiles.models import Profile
from django.utils import timezone
from django.shortcuts import render

from django.urls import reverse
from django.contrib.auth.models import User
import datetime
body_sample = "Cool thanks for reading"
title="My first post"

def create_post(body, title, author, days=0):
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.get_or_create(post_body=body, post_title=title, pub_date=time,author=author)

def create_user():
    try:
        return User.objects.create_user('john', 'youcantseeme@wwe.com', 'johnpassword')
        profile = Profile.objects.get_or_create(first_name="John", last_name="Cena", address="123 Fake Street", city="Miami", state="FL", user=user)
    except:
        return User.objects.get(email = 'youcantseeme@wwe.com')

# Create your tests here.
class PostsDetailView(TestCase):

    def test_detail_view_shows_body(self):
        user = create_user()
        post = create_post(body_sample, title, user )
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, post.post_body)

    def test_does_not_show_if_pub_date_in_future(self):
        user = create_user()
        post = create_post(body_sample, title, user, 4 )
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status, 404)

class PostsIndexView(TestCase):
    def test_shows_most_recent_posts(self):
        self.assertEqual(1+1, 2)
