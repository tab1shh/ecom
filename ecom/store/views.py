from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q


def home(request):
    # fetch all products from the DB
    products = Product.objects.all()
    categories = Category.objects.all()
    # render with list of products
    return render(request, "home.html", {"products": products})


def about(request):
    return render(request, "about.html", {})


def login_user(request):
    # if the request method if POST
    if request.method == "POST":
        # get the user and pass from the submitted form data
        username = request.POST["username"]
        password = request.POST["password"]
        # authenticate the user with the provided credentials
        user = authenticate(request, username=username, password=password)
        # if user exists and credentials are valid
        if user is not None:
            # log the user in and displat a success message
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect("home")
        else:
            # diplay if authentication fails
            messages.success(request, ("There was an error, please try again..."))
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user(request):
    # log the user out
    logout(request)
    messages.success(request, ("You Have Been Logged Out..."))
    return redirect("home")


def register_user(request):
    # create an empty instance
    form = SignUpForm()
    # check if the request method is POST
    if request.method == "POST":
        # create a form instance populated with the submitted data
        form = SignUpForm(request.POST)
        # validate form data
        if form.is_valid():
            # save the valif form data to DB (creates a new user)
            form.save()
            # extract username and password
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # authenticater user with the provided username and password
            user = authenticate(username=username, password=password)
            # log the user (creates a session)
            login(request, user)
            messages.success(
                request,
                ("Username Created - Please Fill Out Your Billing Info Below..."),
            )
            return redirect("update_info")
        else:
            messages.success(
                request, ("There was a problem Registering, please try again")
            )
            return redirect("register")
    else:
        return render(request, "register.html", {"form": form})


def product(request, pk):
    # fetch the product with the give pk from the DB
    product = Product.objects.get(id=pk)
    # render the html page with product details
    return render(request, "product.html", {"product": product})


# click on a category name and it'll take you there
def category(request, foo):
    foo = foo.replace("-", " ")
    # grab the category from the url
    try:
        # look up the category by name
        category = Category.objects.get(name=foo)
        # fetch the products belonging to the category
        products = Product.objects.filter(category=category)
        # render the html with products and category
        return render(
            request, "category.html", {"products": products, "category": category}
        )
    except:
        messages.success(request, ("Category Not Found"))
        return redirect("home")


def category_list(request):
    # fetch all categories from the DB
    categories = Category.objects.all()
    # return the html with the list of categories
    return render(request, "category_list.html", {"categories": categories})


def update_user(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        # fetch the curernt users's data
        current_user = User.objects.get(id=request.user.id)
        # create a form pre-filled with the user data
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        # if form is valid (submitted). update the user data, and log them in
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!")
            return redirect("home")
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.success(request, "You Must Be In Logged In To Access Page")
        return redirect("home")


def update_password(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        # get the current user
        current_user = request.user

        # check if request is 'POST'
        if request.method == "POST":
            # create a password change form
            form = ChangePasswordForm(current_user, request.POST)

            # if form is valid, save the password, log in the user, and redirect them
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated...")
                login(request, current_user)
                return redirect("update_user")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect("update_password")
        else:
            # if request method is 'GET' display the password change form
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form": form})

    else:
        messages.success(request, "You Must Be In Logged In To Access Page")
        return redirect("home")


def update_info(request):
    # check if the user authenticated
    if request.user.is_authenticated:
        # get the current user profile
        current_user = Profile.objects.get(user__id=request.user.id)
        # create a form pre filled with the user profile data
        form = UserInfoForm(request.POST or None, instance=current_user)
        # if form valid- save profile data, display msg, redirect to home page
        if form.is_valid():
            form.save()

            messages.success(request, "Your Info Has Been Updated!")
            return redirect("home")
        # render the html with profile form
        return render(request, "update_info.html", {"form": form})
    else:
        messages.success(request, "You Must Be In Logged In To Access Page")
        return redirect("home")


def search(request):
    # check if request is 'POST'
    if request.method == "POST":
        # get the search term from the submitted data
        searched = request.POST["searched"]

        # query the Products DB Model for products matching the search term
        searched = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched)
        )

        # test for null
        # if no product found- display error, and render html with no results
        if not searched:
            messages.success(request, "That Product Does Not Exist...")
            return render(request, "search.html", {})

        else:
            # render html with results
            return render(request, "search.html", {"searched": searched})
    else:
        # if the request is 'GET' display the search form
        return render(request, "search.html", {})
