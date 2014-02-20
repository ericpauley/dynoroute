from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages
from django.contrib import auth

def home(request):
    return render(request, "dashboard.html")

def signup(request):
    pass
