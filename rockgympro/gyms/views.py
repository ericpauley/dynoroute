from django.shortcuts import render, get_object_or_404
from gyms.models import Gym

def resolve_gym(func):
	def result(*args, **kwargs):
		if 'gym' in kwargs:
			kwargs['gym'] = get_object_or_404(Gym, slug=kwargs['gym'])
		return func(*args, **kwargs)
	return result

@resolve_gym
def gym_page(request, gym):
	return render(request, "home.html", {'gym':gym})

@resolve_gym
def route(request, gym, route):
	return render(request, "route.html")