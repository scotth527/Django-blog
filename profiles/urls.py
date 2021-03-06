from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'profiles'
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url( r'^login/$', views.signin, name="login"),
    url( r'^logout/$', views.logout_view, name="logout"),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:requestee_id>/friend-request', views.request_friendship, name='friend-request'),
    path('<int:pk>/friend-request-update', views.FriendshipUpdateView.as_view(), name='friend-request-update'),
    path('<int:pk>/friend-list', views.FriendshipIndexView.as_view(), name='friend-list'),
    path('<int:pk>/friendship-delete/', views.FriendshipDeleteView.as_view(), name='delete-friendship'),
]