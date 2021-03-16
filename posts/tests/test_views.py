from django.test import TestCase, Client, RequestFactory
from posts.models import Post, Reaction
from profiles.models import Profile
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from profiles.tests.helpers.utils import login, create_user
from posts.tests.helpers.utils import create_post
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
import unittest
import pdb

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
        self.index_url = reverse('posts:index')

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
        go_to_index = self.client.get(self.index_url)
        self.assertContains(go_to_index, title)
        reaction_url = f'/posts/{post.id}/post/reaction/'
        add_reaction = self.client.post(reaction_url, {"reaction":"U+1F44D"})
        # pdb.set_trace()
        self.assertRedirects(add_reaction, self.index_url)
        self.assertEqual(post.reactions.filter(user=self.user).count(), 1)

    def test_that_if_post_has_a_reaction_by_the_user_already_that_it_will_be_removed(self):
        login(self.client)
        post = create_post(body_sample, title, self.user, -4)
        go_to_index = self.client.get(self.index_url)
        self.assertContains(go_to_index, title)
        User.objects.create_user('Dwayne', 'dj@wwe.com', 'peoplepassword')
        second_user = User.objects.get(email='dj@wwe.com')
        reaction1 = Reaction.objects.create(user=self.user, reaction="U+1F44D", object_id=post.id, content_object=post)
        reaction2 = Reaction.objects.create(user=second_user ,reaction="U+1F44D", object_id=post.id, content_object=post)
        reaction_url = f'/posts/{post.id}/post/reaction/'
        remove_reaction = self.client.post(reaction_url, {"reaction":"U+1F44D"})
        self.assertEqual(post.reactions.filter(user=self.user).count(), 0)
        self.assertEqual(post.reactions.all().count(), 1)

    def test_that_if_user_is_not_logged_in_and_tries_detail_gets_redirected(self):
        post = create_post(body_sample, title, self.user, 4)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class PostsIndexView(TestCase):
    def setUp(self):
            create_user()
            self.client = Client()
            self.user = User.objects.get(email="youcantseeme@wwe.com")
            self.index_url = reverse('posts:index')


    def test_only_friends_and_your_own_posts_show_up_on_feed(self):
        login(self.client)
        past_post = create_post("You never know what you are going to get", "Life is a box of chocolates.", self.user,
                                -3)
        index_response = self.client.get(self.index_url)
        self.assertContains(index_response, "Life is a box of chocolates.")

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

class PostsDeleteView(TestCase):

    def setUp(self):
            create_user()
            self.client = Client()
            self.user = User.objects.get(email="youcantseeme@wwe.com")
            self.post = create_post("You never know what you are going to get", "Life is a box of chocolates.", self.user, -3)
            self.index_url = reverse('posts:index')

    def test_a_post_is_successfully_deleted_if_it_user_is_author(self):
        login(self.client)
        delete_url = f'/posts/{self.post.id}/delete/'
        delete_response = self.client.post(delete_url, {}, follow=True)
        self.assertRedirects(delete_response, 'posts/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_a_delete_is_unsuccessful_if_user_is_not_author(self):
        # login(self.client)
        User.objects.create_user('joe', 'bigdog@wwe.com', 'joepassword')
        self.client.login(username='joe', password='joepassword')
        delete_url = f'/posts/{self.post.id}/delete/'
        delete_response = self.client.post(delete_url)
        self.assertEqual(delete_response.status_code, 403)

class PostsUpdateView(TestCase):
    def setUp(self):
            create_user()
            self.client = Client()
            self.user = User.objects.get(email="youcantseeme@wwe.com")
            self.post = create_post("You never know what you are going to get", "Life is a box of chocolates.", self.user, -3)
            self.index_url = reverse('posts:index')


    def test_user_successfully_updates_post_if_user_is_author(self):
        login(self.client)
        edit_url = reverse('posts:update-post', kwargs={'pk': self.post.id})
        edit_response = self.client.post(edit_url, {"post_body": "YOU CANNOT SEE ME" }, follow=True)
        self.assertEqual(edit_response.status_code, 200)
        self.assertContains(edit_response, "YOU CANNOT SEE ME")

    def test_user_gets_403_if_user_is_not_author_of_post(self):
        User.objects.create_user('joe', 'bigdog@wwe.com', 'joepassword')
        self.client.login(username='joe', password='joepassword')
        edit_url = reverse('posts:update-post', kwargs={'pk': self.post.id})
        edit_response = self.client.post(edit_url, {"post_body": "YOU CANNOT SEE ME"}, follow=True)
        self.assertEqual(edit_response.status_code, 403)

