from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        # redirecting to login page
        return redirect("/")
    
    return render(request, "home/index.html")
