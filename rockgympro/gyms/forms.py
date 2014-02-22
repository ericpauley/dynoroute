from gyms.models import Route
from django.forms import ModelForm
from users.models import User
from django.utils import timezone
from django import forms

from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe

class RouteForm(ModelForm):

    def __init__(self, gym, user, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        self.fields['setter'].queryset = gym.staff.filter(level__gte=1000)
        self.fields['date_set'].initial = timezone.now()
        self.fields['status'].initial = 'complete'
        self.fields['type'].initial = 'bouldering'
        self.fields['difficulty'].label = "Grade"
        if user.gym == gym:
            self.fields['setter'].initial = user
        self.instance.gym = gym

    class Meta:
        fields = ['type', 'difficulty', 'location', 'date_set', 'setter', 'name', 'notes', 'status', 'color1', 'color2']
        model = Route
        widgets = {
          'notes': forms.Textarea(attrs={'rows':3, 'cols':10}),
          'color1': forms.Select(attrs=dict(id="route-color")),
          'color2': forms.Select(attrs=dict(id="route-color2")),
          'date_set': forms.DateInput(attrs=dict(id="route-date-set")),
          'type': forms.RadioSelect(),
        }

