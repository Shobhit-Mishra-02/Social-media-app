from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .utils.upload_files import upload_file

from .forms import PostCreationForm
from .models import Post
# from .models import UploadImage

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        # redirecting to login page
        return redirect("/")
    
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post_title = form.cleaned_data["title"]
            post_content = form.cleaned_data["content"]
            post_image = form.cleaned_data["image"]
            post_image_caption = form.cleaned_data["caption"]

            print(post_title)
            print(post_content)
            print(post_image)
            print(post_image_caption)

            post = Post.objects.create(user=request.user, title=post_title, content=post_content, image=post_image, caption=post_image_caption)

            post.save()

            return render(request, "home/index.html", {"form":form})
    else:
        form = PostCreationForm()

    return render(request, "home/index.html", {"form":form})

def create_post(request):
    if request.method == "POST":
        post_text = request.POST["postContent"]
        print(post_text)
        print(type(request.FILES["media"]))
        # upload_file(request.FILES["media"])
        
        # form = CreatePostForm(request.POST, request.FILES)
        # if form.is_valid():
        #     # form is valid
        #     post_text = form.cleaned_data["postContent"]
        #     file = form.cleaned_data["media"]

        #     print(post_text)
        #     print(file)
        # else:
        #     print("Not a valid form")

    return redirect("/social/home")
