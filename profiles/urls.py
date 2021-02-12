from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


app_name = 'profiles'
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url( r'^login/$', views.signin, name="login"),
    url( r'^logout/$', views.logout_view, name="logout"),
]