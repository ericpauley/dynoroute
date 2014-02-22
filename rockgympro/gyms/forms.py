from gyms.models import Route
from django.forms import ModelForm

class RouteForm(ModelForm):
	class Meta:
		fields = ['difficulty', 'location', 'date_set']
		model = Route
