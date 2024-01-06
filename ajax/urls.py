from django.urls import path
from . import views

app_name = "ajax"
urlpatterns = [
    path("posts/<int:page>", views.get_posts, name="posts"),
    path("like/<int:id>", views.update_like_status, name="update_like_status"),
    path("addGeneralInformation/", views.add_general_information, name="genral_information")
]