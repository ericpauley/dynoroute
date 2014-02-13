from django.shortcuts import render

def home(request):
	return render(request, "content.html")

def login(request):
	return render(request, "login.html")

def signup(request):
	return render(request, "signup.html")