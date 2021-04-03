from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostsIndexView.as_view(), name='index'),
    path('<int:pk>/', views.PostsDetailView.as_view(), name='detail'),
    path('create/',views.create_post, name='create-post'),
    path('<int:post_id>/comment/',views.create_comment, name='create-comment'),
    path('<int:object_id>/<str:object_type>/reaction/', views.toggle_reaction, name='toggle-reaction'),
    path('<int:pk>/delete/', views.PostsDeleteView.as_view(), name='delete-post'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='update-post'),
]