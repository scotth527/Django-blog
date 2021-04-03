from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from haystack.views import basic_search
from . import views


app_name = 'profiles'
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url( r'^login/$', views.signin, name="login"),
    url( r'^logout/$', views.logout_view, name="logout"),
    url(r'search/$', login_required(basic_search), name='basic_search'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<str:keyword>/search', views.SearchUserIndexView.as_view(), name='user-search'),
    path('<int:requestee_id>/friend-request', views.request_friendship, name='friend-request'),
    path('<int:pk>/friend-request-update', views.FriendshipUpdateView.as_view(), name='friend-request-update'),
    path('<int:pk>/friend-list', views.FriendshipIndexView.as_view(), name='friend-list'),
    path('<int:pk>/friend-suggestion', views.FriendshipSuggestionIndexView.as_view(), name='friend-suggestion'),
    path('<int:pk>/friendship-delete/', views.FriendshipDeleteView.as_view(), name='delete-friendship'),
]