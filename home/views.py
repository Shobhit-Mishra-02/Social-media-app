from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .utils.upload_files import upload_file

from .forms import ImageUploadForm
from .models import UploadImage

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        # redirecting to login page
        return redirect("/")
    
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            img_obj = form.instance

            return render(request, "home/index.html", {"form":form, "img_obj":img_obj})
    else:
        form = ImageUploadForm()

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
