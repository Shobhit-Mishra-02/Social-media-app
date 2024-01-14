from django.urls import path
from . import views

app_name = "ajax"
urlpatterns = [
    path("posts/<int:page>", views.get_posts, name="posts"),
    path("like/<int:id>", views.update_like_status, name="update_like_status"),
    path("addGeneralInformation/", views.add_general_information, name="general_information"),
    path("generalInformation/", views.get_general_information, name="get_general_information"),
    path("getPersonalInformation/", views.get_personal_information, name="get_personal_information"),
    path("addPersonalInformation/", views.add_personal_information, name="add_personal_information")
]