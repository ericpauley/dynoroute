from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages
from django.contrib import auth
from django.views.generic import DetailView

def home(request):
    if request.user.is_authenticated():
        return render(request, "home.html")
    else:
        return render(request, "launch.html")

def signup(request):
    pass
