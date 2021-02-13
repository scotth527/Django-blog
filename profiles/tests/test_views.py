from django.test import TestCase, Client
from django.contrib.auth.models import User
# Create your tests here.
from django.urls import reverse
from profiles.tests.helpers.utils import login, create_user
import unittest

class ProfileDetailView(TestCase):
    def setUp(self):
                self.client = Client()

    @unittest.skip("test not done yet")
    def test_profile_detail_works(self):
        go_to_login = self.client.get("/profiles/login/")
        self.assertEqual(go_to_login.status_code, 200)
        login(self.client)
        profile_detail_response = self.client.get('/profiles/detail/')
        # f"Shepherd {shepherd} is {age} years old."
        assertContains(profile_detail_response, "john")
        pass

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
        print("Registration", signup_response)
        self.assertEqual(signup_response.status_code, 200)

    def test_error_message_if_invalid_password(self):
        pass

    def test_error_message_if_empty_fields(self):
        pass

class LoginView(TestCase):
    def setUp(self):
            self.client = Client()

    @unittest.skip("skip the test")
    def test_successful_login(self):
        response = self.client.get("/profiles/login/")
        self.assertEqual(response.status_code, 200)
        login_response = self.client.post(
                    "/profiles/login/", data={"username": "john", "password" :"johnpassword"}
                )
        self.assertRedirects(login_response, '/posts/index/', status_code=302, target_status_code=200)
        pass

    @unittest.skip("skip the test")
    def test_success_login_redirects_to_posts_index(self):
        login_response = self.client.post(
                                    "/profiles/login/", data={"username": "john", "password" :"johnpassword"}
                                )
        print("Login Response on line 42", login_response)
        self.assertRedirects(login_response, '/posts/index/', status_code=302, target_status_code=200)
        pass

    def test_incorrect_password_shows_errors(self):
        response = self.client.get("/profiles/login/")
        login_response = self.client.post(
                            "/profiles/login/", data={"username": "john", "password" :"fdsafdsafdsd"}, follow=True
                        )
        self.assertRedirects(login_response, '/profiles/login/')
        self.assertContains(login_response, "Username or password is incorrect.")


class LogoutView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_that_logout_is_successful(self):
        login_response = self.client.post(
                            "/profiles/login/", data={"username": "john", "password" :"johnpassword"}
                        )
        logout_response = self.client.get('/profiles/logout/', follow=True)
        print("Logout response", logout_response.status_code)
        self.assertRedirects(logout_response, '/profiles/login/', status_code=302, target_status_code=200, fetch_redirect_response=True)



