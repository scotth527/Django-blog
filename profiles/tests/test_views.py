from django.test import TestCase, Client
from django.contrib.auth.models import User
# Create your tests here.
from django.urls import reverse
from profiles.models import Friendship
from profiles.tests.helpers.utils import login, create_user
import unittest

class ProfileDetailView(TestCase):
    def setUp(self):
                self.client = Client()
                create_user()

    def test_profile_detail_works(self):
        go_to_login = self.client.get("/profiles/login/")
        self.assertEqual(go_to_login.status_code, 200)
        login(self.client)
        user = User.objects.get(email="youcantseeme@wwe.com")
        profile_detail_response = self.client.get(f'/profiles/{user.id}')
        self.assertContains(profile_detail_response, "john")

    def test_profile_detail_for_redirect_if_no_authentication(self):
        user = User.objects.get(email="youcantseeme@wwe.com")
        profile_detail_response = self.client.get(f'/profiles/{user.id}', follow=True)
        self.assertRedirects(profile_detail_response, f'/profiles/login/?next=/profiles/{user.id}', status_code=302, target_status_code=200)

class SignUpView(TestCase):
    def setUp(self):
            self.client = Client()

    def test_successful_registration(self):
        response = self.client.get("/profiles/signup/")
        self.assertEqual(response.status_code, 200)
        signup_response = self.client.post(
                                              "/profiles/signup/",
                                              data={"username": "billy",
                                                    "password" :"billypassword",
                                                    "first_name" : "Bill",
                                                    "last_name" : "Billson",
                                                    "address" : "123 Fake Street",
                                                    "city" : "Miami",
                                                    "state" : "Fl"
                                                    }, follow = True
                                           )
        self.assertEqual(signup_response.status_code, 200)

    def test_error_message_if_invalid_password(self):
        pass

    def test_error_message_if_empty_fields(self):
        pass

class LoginView(TestCase):
    def setUp(self):
            self.client = Client()
            create_user()

    def test_successful_login(self):
        response = self.client.get("/profiles/login/")
        self.assertEqual(response.status_code, 200)
        login_response = self.client.post("/profiles/login/",  {"username": "john", "password" :"johnpassword"}, follow=True, secure=True)
        self.assertEqual(login_response.status_code, 200)

    # @unittest.skip("skip the test")
    def test_success_login_redirects_to_posts_index(self):
        login_response = self.client.post(
                                    "/profiles/login/", data={"username": "john", "password" :"johnpassword"}, follow=True, secure=True
                                )
        # print("Login Response on line 42", login_response.content)
        self.assertRedirects(login_response, '/', status_code=302, fetch_redirect_response=True)


    def test_incorrect_password_shows_errors(self):
        response = self.client.get("/profiles/login/")
        login_response = self.client.post(
                            "/profiles/login/", data={"username": "john", "password" :"fdsafdsafdsd"}, follow=True
                        )
        self.assertRedirects(login_response, '/profiles/login/',status_code=302, fetch_redirect_response=True)
        self.assertContains(login_response, "Username or password not correct.")


class LogoutView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_that_logout_is_successful(self):
        login(self.client)
        logout_response = self.client.get('/profiles/logout/', follow=True)
        self.assertRedirects(logout_response, '/profiles/login/', status_code=302, target_status_code=200, fetch_redirect_response=True)

class FriendshipRequestView(TestCase):
    def setUp(self):
        self.client = Client()
        create_user()
        self.user = User.objects.get(email="youcantseeme@wwe.com")
        self.user2 = User.objects.create_user('billy', 'billy@wwe.com', 'billypassword')

    def test_that_friendship_request_is_successful_if_logged_in(self):
        login(self.client)
        friendship_url = reverse('profiles:friend-request', kwargs={'requestee_id': self.user2.id})
        friendrequest_response = self.client.post(friendship_url, {"status":"Accept"}, follow=True)
        self.assertEquals(friendrequest_response.status_code, 200)


class FriendshipUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        create_user()
        self.user = User.objects.get(email="youcantseeme@wwe.com")
        self.user2 = User.objects.create_user('billy', 'billy@wwe.com', 'billypassword')

    def test_that_friendship_request_can_be_updated_if_user_is_requestee(self):
        login(self.client)
        friendship_request_url = reverse('profiles:friend-request', kwargs={'requestee_id': self.user2.id})
        friendrequest_response = self.client.post(friendship_request_url, {"status": "Pending"}, follow=True)
        self.client.logout()

        friendrequest = Friendship.objects.get(requestee=self.user2, requester=self.user)
        self.client.login(username='billy', password='billypassword')
        friendship_update_request_url = reverse('profiles:friend-request-update', kwargs={'pk': friendrequest.id})
        print("Friendship update", friendship_update_request_url)
        friendship_update = self.client.post(friendship_update_request_url, {"status":"Accept"}, follow=True)
        self.assertEquals(friendship_update.status_code, 200)
