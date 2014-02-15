from django.shortcuts import render, get_object_or_404
from gyms.models import Gym

def gym_finder(func):
	def result(*args, **kwargs):
		if 'gym' in kwargs:
			kwargs['gym'] = get_object_or_404(Gym, slug=kwargs['gym_name'])
		return func(*args, **kwargs)
	return result

@gym_finder
def home(request, gym):
	return render(request, "content.html")