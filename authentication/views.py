from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as account_login
from django.contrib.auth import logout as account_logout
from django.shortcuts import redirect, render


def login(request):
    # if the user session is already present, then redirect to the home page
    if request.user.is_authenticated:
        # redirect to home page
        return redirect("social/home/")

    # if the incomming request method is post which will trigger the actual login procedure
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)

        if user is not None:
            # user is verified
            account_login(request, user)

            # redirect to home page
            return redirect("social/home/")

        # redirect to login page with error message
        return render(request, "authentication/login.html", {"error_message": "Authentication fails !!"})

    # if a new user encounters then show the login page
    return render(request, "authentication/login.html")


def signup(request):
    # if the user session is already present then redirect to the home page
    if request.user.is_authenticated:
        # redirect to home page
        return redirect("social/home/")

    # if the incomming request method is post which will trigger the actual signup procedure
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Creating a new user account
        User = get_user_model()
        User.objects.create_user(email=email, password=password)

        # redirecting to the login page
        return redirect("/")

    # if a new user encounters then show the signup page
    return render(request, "authentication/signup.html")


def logout(request):
    account_logout(request)  # logout the user

    # then, redirecting the user to the login page
    return render(request, "authentication/login.html")
