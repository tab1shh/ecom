from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "home.html", {"products": products})


def about(request):
    return render(request, "about.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect("home")
        else:
            messages.success(request, ("There was an error, please try again..."))
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out..."))
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You Have Registered Successfully"))
            return redirect("home")
        else:
            messages.success(
                request, ("There was a problem Registering, please try again")
            )
            return redirect("register")
    else:
        return render(request, "register.html", {"form": form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {"product": product})


def category(request, foo):
    foo = foo.replace("-", " ")
    # grab the category from the url
    try:
        # look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(
            request, "category.html", {"products": products, "category": category}
        )
    except:
        messages.success(request, ("Category Not Found"))
        return redirect("home")


def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})
