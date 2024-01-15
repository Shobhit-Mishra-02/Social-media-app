from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("home/", views.index, name="home"),
    path("profile/<int:id>/", views.profile, name="profile"),
]