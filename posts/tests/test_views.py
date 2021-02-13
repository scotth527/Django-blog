from django.test import TestCase, Client
from posts.models import Post
from profiles.models import Profile
from django.utils import timezone
from django.shortcuts import render
from profiles.tests.helpers.utils import login, create_user
from posts.tests.helpers.utils import create_post
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

body_sample = "Cool thanks for reading"
title="My first post"

# Create your tests here.
class PostsDetailView(TestCase):
    def setUp(self):
        user = create_user()
        self.client = Client()

    def test_detail_view_shows_body(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        post = create_post(body_sample, title, user)
        login(self.client)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, body_sample)

    def test_does_not_show_if_pub_date_in_future(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        post = create_post(body_sample, title, user, 4)
        login(self.client)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_that_like_button_works(self):
        pass

    def test_that_if_user_is_not_logged_in_gets_redirected(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        post = create_post(body_sample, title, user, 4)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class PostsIndexView(TestCase):
    def setUp(self):
            user = create_user()
            self.client = Client()

    def test_that_you_need_to_be_logged_in_to_see_index(self):
        url = reverse('posts:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_future_posts_are_not_included(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        future_post = create_post(body_sample, title, user, 4)
        past_post = create_post("You never know what you are going to get", "Life is a box of chocolates.", user, -3)
        login(self.client)
        response = self.client.get(reverse('posts:index'))
        self.assertQuerysetEqual(
                    response.context['latest_post_list'],
                    ['<Post: Life is a box of chocolates.>']
                )

    def test_if_no_posts_display_message(self):
        login(self.client)
        response = self.client.get(reverse('posts:index'))
        self.assertContains(response, "No posts are available.")

    def test_past_posts_included(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        post = create_post("You never know what you are going to get", "Life is a box of chocolates.", user, -3)
        login(self.client)
        response = self.client.get(reverse('posts:index'))
        self.assertContains(response, "Life is a box of chocolates.")

    def test_only_shows_posts_from_people_you_follow(self):
        pass



