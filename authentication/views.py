from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as account_login
from django.contrib.auth import logout as account_logout
from django.shortcuts import redirect, render


def login(request):
    # if request.user.is_authenticated:
        # redirect to home page

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)

        if user is not None:
            # user is verified
            account_login(request, user)

            # redirect to home page
        else:
            # redirect to login page with error message
            return render(request, "authentication/login.html", {"error_message":"Authentication fails !!"})
            

        return redirect("/")
    
    return render(request, "authentication/login.html")

def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Creating a new user account
        User = get_user_model()
        user = User.objects.create_user(email=email, password=password)
        user.save()
        
        return redirect("/")

    return render(request, "authentication/signup.html")

def logout(request):
    account_logout(request)

    return render(request, "authentication/login.html")