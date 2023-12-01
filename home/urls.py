from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("home/", views.index, name="home"),
    path("createPost/", views.create_post, name="create_post"),
]