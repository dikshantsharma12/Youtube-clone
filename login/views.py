from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from profile_page.models import UserDetails
from django.contrib import messages, auth
from django.contrib.auth import authenticate


def signup(request):

    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST["email"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()
        user_id = user.id
        user = User.objects.get(id=user_id)
        user_details = UserDetails.objects.create(
            user_id=user,
            first_name=first_name,
            last_name=last_name,
        )
        user_details.save()
        return redirect('/login')
    else:
        return render(request, 'signup.html')


def login(request):

    if request.method == "POST":
        username = request.POST['emails']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Couldn't found your google account")
            return redirect("/login")
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect("/")


def password_page(request):

    return render(request, 'password_page.html')
