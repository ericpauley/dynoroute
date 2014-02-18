from django.shortcuts import render, get_object_or_404
from gyms.models import Gym, Route
from django.utils.timezone import now
from django.http import Http404

def resolve_gym(func):
	def result(*args, **kwargs):
		if 'gym' in kwargs:
			kwargs['gym'] = get_object_or_404(Gym, slug=kwargs['gym'])
		return func(*args, **kwargs)
	return result

@resolve_gym
def gym_page(request, gym):
	return render(request, "gym_page.html", {'gym':gym, 'pg':'gym_page'})

@resolve_gym
def routes(request, gym):
	routes = gym.routes.filter(date_torn__isnull=True, date_torn__lte=now())
	return render(request, "gym_routes.html", {'gym':gym, 'pg':'gym_routes', 'routes':routes})

@resolve_gym
def route(request, gym, route):
	try:
		route = gym.routes.get(slug=route)
	except Route.DoesNotExist:
		raise Http404
	return render(request, "route.html", {'gym':gym})
