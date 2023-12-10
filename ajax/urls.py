from django.urls import path
from . import views

app_name = "ajax"
urlpatterns = [
    path("posts/", views.get_posts, name="posts")
]