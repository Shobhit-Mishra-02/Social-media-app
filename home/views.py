from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

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
            
            return render(request, "home/index.html", {"form":PostCreationForm()})
    else:
        form = PostCreationForm()

    return render(request, "home/index.html", {"form":form})

@login_required
def profile(request, id):

    general_information_form = GeneralInformationForm()
    personal_information_form = PersonalInformationForm()
    is_owner = True if request.user.id == id else False


    return render(request, "home/profile.html", {
        "general_information_form":general_information_form,  
        "personal_information_form":personal_information_form,
        "is_owner": is_owner,
        "id": id
        })

@login_required
def get_user_posts(request):
    
    return render(request, "home/user_posts.html")

@login_required
def view_post(request, id):

    return render(request, "home/view_post.html")



