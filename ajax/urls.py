from django.urls import path
from . import views

app_name = "ajax"
urlpatterns = [
    path("posts/<int:page>/<int:own_user>", views.get_posts, name="posts"),
    path("like/<int:id>", views.update_like_status, name="update_like_status"),
    path("addGeneralInformation/", views.add_general_information, name="general_information"),
    path("generalInformation/<int:id>/", views.get_general_information, name="get_general_information"),
    path("getPersonalInformation/<int:id>/", views.get_personal_information, name="get_personal_information"),
    path("addPersonalInformation/", views.add_personal_information, name="add_personal_information"),
    path("getUserDetails/<int:id>/", views.get_user_details, name="get_user_details"),
    path("getTrendingPosts/", views.get_trending_posts, name="get_trending_posts")
]