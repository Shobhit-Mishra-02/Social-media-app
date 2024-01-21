from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("home/", views.index, name="home"),
    path("profile/<int:id>/", views.profile, name="profile"),
    path("getUserPosts/", views.get_user_posts, name="get_user_posts"),
    path("viewPost/<int:id>/", views.view_post, name="view_post"),
]