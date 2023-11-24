from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, "authentication/login.html")

def signup(request):
    return render(request, "authentication/signup.html")