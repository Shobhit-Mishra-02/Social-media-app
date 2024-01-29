from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Count, Sum

from authentication.models import AccountUser
from .forms import PostCreationForm, GeneralInformationForm, PersonalInformationForm
from .models import Post, GeneralInformation, PersonalInformation
from .utils.upload_files import upload_file


@login_required
def index(request):

    if request.method == "POST":
        post = Post(user=request.user)
        form = PostCreationForm(request.POST, request.FILES, instance=post)
        if form.is_valid():

            form.save()

            return render(request, "home/index.html", {"form": PostCreationForm()})
    else:
        form = PostCreationForm()

    return render(request, "home/index.html", {"form": form})


@login_required
def profile(request, id):

    general_information_form = GeneralInformationForm()
    personal_information_form = PersonalInformationForm()
    is_owner = True if request.user.id == id else False

    user = AccountUser.objects.filter(pk=id).first()

    if user:
        top_user_posts = user.post_set.annotate(
            likes_count=Count("userlikepost")).order_by("-likes_count")[0:5]
        total_likes = user.post_set.annotate(likes_count=Count(
            'userlikepost')).aggregate(total_likes=Sum('likes_count', default=0))
    else:
        total_likes = {"total_likes": 0}
        top_user_posts = None

    return render(request, "home/profile.html", {
        "general_information_form": general_information_form,
        "personal_information_form": personal_information_form,
        "is_owner": is_owner,
        "id": id,
        "top_user_posts": top_user_posts,
        "total_likes": total_likes
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
