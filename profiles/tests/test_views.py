from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.


class ProfileDetailView(TestCase):
    def test_profile_detail_works(self):
         pass

class SignUpView(TestCase):
    def test_successful_registration(self):
        pass

    def test_error_message_if_invalid_password(self):
        pass

    def test_error_message_if_empty_fields(self):
        pass
