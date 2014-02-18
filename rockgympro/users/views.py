from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import auth

def home(request):
    return render(request, "dashboard.html")

def login(request):
    if request.user.is_authenticated():
        return redirect('home')
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        auth.login(request, form.get_user())
        return redirect("home")
    return render(request, "login.html", dict(form=form))

def signup(request):
    pass
