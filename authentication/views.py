from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)

        if user is not None:
            # user is verified
            print(f"The user is {user.email}")
        else:
            # user is not verified
            print("authentication fails")
            

        return redirect("/")
    
    return render(request, "authentication/login.html")

def signup(request):
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        User = get_user_model()
        user = User.objects.create_user(email=email, password=password)
        user.save()
        
        return redirect("/")

    return render(request, "authentication/signup.html")