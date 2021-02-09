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
    return Post.objects.get_or_create(post_body=body, post_title=title, pub_date=time,author=author)[0]

def create_user():
    try:
        return User.objects.create_user('john', 'youcantseeme@wwe.com', 'johnpassword')
        profile = Profile.objects.get_or_create(first_name="John", last_name="Cena", address="123 Fake Street", city="Miami", state="FL", user=user)
    except:
        return User.objects.get(email = 'youcantseeme@wwe.com')

# Create your tests here.
class PostsDetailView(TestCase):
    def setUp(self):
        user = create_user()

    def test_detail_view_shows_body(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        post = create_post(body_sample, title, user)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, body_sample)

    def test_does_not_show_if_pub_date_in_future(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        post = create_post(body_sample, title, user, 4)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_that_like_button_works(self):
        pass

class PostsIndexView(TestCase):
    def setUp(self):
            user = create_user()

    def test_future_posts_are_not_included(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        future_post = create_post(body_sample, title, user, 4)
        past_post = create_post("You never know what you are going to get", "Life is a box of chocolates.", user, -3)
        response = self.client.get(reverse('posts:index'))
        self.assertQuerysetEqual(
                    response.context['latest_post_list'],
                    ['<Post: Life is a box of chocolates.>']
                )

    def test_if_no_posts_display_message(self):
        response = self.client.get(reverse('posts:index'))
        self.assertContains(response, "No posts are available.")

    def test_past_posts_included(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        post = create_post("You never know what you are going to get", "Life is a box of chocolates.", user, -3)
        response = self.client.get(reverse('posts:index'))
        self.assertContains(response, "Life is a box of chocolates.")

    def test_only_shows_posts_from_people_you_follow(self):
        pass

