from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'profiles'
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signup'),
]