
from django.contrib import admin

# Register your models here.
from profiles.models import Profile

app_name="profiles"
admin.site.register(Profile)