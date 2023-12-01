from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .utils.upload_files import upload_file

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        # redirecting to login page
        return redirect("/")
    
    return render(request, "home/index.html")

def create_post(request):
    if request.method == "POST":
        post_text = request.POST["postContent"]
        print(post_text)
        upload_file(request.FILES["media"])

    return redirect("/social/home")
