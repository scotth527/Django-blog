from django.test import TestCase, Client, RequestFactory
from posts.models import Post
from profiles.models import Profile
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from profiles.tests.helpers.utils import login, create_user
from posts.tests.helpers.utils import create_post
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

body_sample = "Cool thanks for reading"
title="My first post"

# Create your tests here.
class PostCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        create_user()
        self.user = User.objects.get(email="youcantseeme@wwe.com")
        self.index_route = reverse('posts:index')
        self.create_post_route = reverse('posts:create-post')
        self.post_data = {  "post_body":"Hello Darkness",
                                                   "post_title":"You cannot see me" ,
                                                   "author": f"{self.user.id}",
                                                   "pub_date_month": '1',
                                                   "pub_date_day": '1',
                                                   'pub_date_year':'2021' }

    def test_successful_creation_of_new_post_from_index(self):
        login(self.client)
        go_to_index = self.client.get(self.index_route)
        self.assertEqual(go_to_index.status_code, 200)
        post_response = self.client.post(self.create_post_route, self.post_data , follow=True )
        self.assertRedirects(post_response, '/posts/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertContains(post_response, "Hello Darkness" )

    def test_post_detail_works_after_creation(self):
        login(self.client)
        post_response = self.client.post(self.create_post_route, self.post_data , follow=True )
        self.assertEqual(post_response.status_code, 200)
        post = Post.objects.get(post_title="You cannot see me")
        url = reverse('posts:detail', args=(post.id,))
        detail_route = self.client.get(url)
        self.assertEqual(detail_route.status_code, 200)

class PostsDetailView(TestCase):
    def setUp(self):
        user = create_user()
        self.client = Client()
        self.user = User.objects.get(email="youcantseeme@wwe.com")

    def test_detail_view_shows_body(self):
        post = create_post(body_sample, title, self.user)
        login(self.client)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, body_sample)

    def test_does_not_show_if_pub_date_in_future(self):
        post = create_post(body_sample, title, self.user, 4)
        login(self.client)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # @unittest.skip("skip the test")
    def test_a_reaction_is_added_if_not_yet_reacted(self):
        login(self.client)
        post = create_post(body_sample, title, self.user, -4)
        url = reverse('posts:index')
        go_to_index = self.client.get(url)
        print("Post that was created", go_to_index.content)
        self.assertContains(go_to_index, title)

    def test_that_if_post_has_a_reaction_by_the_user_that_it_it_will_be_removed(self):
        pass

    def test_that_if_user_is_not_logged_in_gets_redirected(self):
        post = create_post(body_sample, title, self.user, 4)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class PostsIndexView(TestCase):
    def setUp(self):
            create_user()
            self.client = Client()
            self.user = User.objects.get(email="youcantseeme@wwe.com")

    def test_only_friends_and_your_own_posts_show_up_on_feed(self):
        pass

    def test_that_you_need_to_be_logged_in_to_see_index(self):
        url = reverse('posts:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_future_posts_are_not_included(self):
        future_post = create_post(body_sample, title, self.user, 4)
        past_post = create_post("You never know what you are going to get", "Life is a box of chocolates.", self.user, -3)
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



