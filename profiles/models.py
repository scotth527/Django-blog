from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50, default="Miami")
    state = models.CharField(max_length=50, default="FL")
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
            return self.first_name + " " + self.last_name
