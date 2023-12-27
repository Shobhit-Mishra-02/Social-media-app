from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import PostCreationForm
from .models import Post
from .utils.upload_files import upload_file


@login_required
def index(request):
    
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post_title = form.cleaned_data["title"]
            post_content = form.cleaned_data["content"]
            post_image = form.cleaned_data["image"]
            post_image_caption = form.cleaned_data["caption"]

            Post.objects.create(user=request.user, title=post_title, content=post_content, image=post_image, caption=post_image_caption)

            return render(request, "home/index.html", {"form":form})
    else:
        form = PostCreationForm()

    return render(request, "home/index.html", {"form":form})

@login_required
def profile(request):
    return render(request, "home/profile.html")
