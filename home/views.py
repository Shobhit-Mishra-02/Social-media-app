from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Sum

from authentication.models import AccountUser
from .forms import PostCreationForm, GeneralInformationForm, PersonalInformationForm
from .models import Post


"""

Home controller for the application which handles the post creations on the POST request.

"""


@login_required
def index(request):

    # if the request is POST
    if request.method == "POST":

        # create an instance of Post with the user who is making the request
        post = Post(user=request.user)

        # creating the Post form instance with requested POST content and empty Post instance(with the user)
        form = PostCreationForm(request.POST, request.FILES, instance=post)

        if form.is_valid():

            form.save()  # saving the data

            # rendering the index.html page with empty post form
            return render(request, "home/index.html", {"form": PostCreationForm()})
    else:
        form = PostCreationForm()

    # otherwise if received request is of GET method
    # then, just render index.html with empty form instance
    return render(request, "home/index.html", {"form": form})


"""

This is the profile controller which displays the user profile.

Here the id indicates the id of the user, whose profile needs to display.
"""


@login_required
def profile(request, id):

    # creating form instances of general information and personal information
    general_information_form = GeneralInformationForm()
    personal_information_form = PersonalInformationForm()

    # is_owner variable tells whether the requested user is the owner of the profile
    # if is_owner=True, means that User1 is viewing his own profile
    # if is_owner=False, means that User1 is viewing other user's profile
    is_owner = True if request.user.id == id else False

    return render(
        request,
        "home/profile.html",
        {
            "general_information_form": general_information_form,
            "personal_information_form": personal_information_form,
            "is_owner": is_owner,
            "id": id,
        })


@login_required
def get_user_posts(request):

    return render(request, "home/user_posts.html", {"form": PostCreationForm()})


@login_required
def view_post(request, id):

    filtered_post = Post.objects.filter(pk=id)
    did_user_like_post = True if filtered_post.first().userlikepost_set.filter(
        user_id=request.user.id).count() else False

    full_name = filtered_post.first().user.personalinformation.first_name + " " + \
        filtered_post.first().user.personalinformation.last_name

    if filtered_post.count() > 0:

        return render(request, "home/view_post.html", {"post": filtered_post[0], "did_user_like_post": did_user_like_post, "full_name": full_name})

    return render(request, "home/view_post.html", {"notFound": "Not Found"})


@login_required
def view_friends(request):

    return render(request, "home/friends.html")
