from django.shortcuts import render, redirect

def home(request):
	return render(request, "dashboard.html")

def login(request):
	if request.user.is_authenticated():
		return redirect('home')
	return render(request, "login.html")

def signup(request):
	if request.user.is_authenticated():
		return redirect('home')
	return render(request, "signup.html")
