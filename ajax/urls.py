from django.urls import path
from . import views

app_name = "ajax"
urlpatterns = [
    path("posts/<int:page>", views.get_posts, name="posts"),
    path("like/<int:id>", views.increment_likes, name="increment_likes")
]