from django.shortcuts import render

def home(request):
	return render(request, "dashboard.html")

def login(request):
	return render(request, "login.html")

def signup(request):
	return render(request, "signup.html")

def route(request):
	return render(request, "route.html")
