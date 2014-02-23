from gyms.models import Route, Gym
from django.forms import ModelForm
from users.models import User
from django.utils import timezone
from django import forms

from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe

class RouteForm(ModelForm):

    location = forms.ChoiceField()

    def __init__(self, gym, user, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        self.fields['setter'].queryset = gym.staff.filter(level__gte=1000)
        self.fields['date_set'].initial = timezone.now()
        self.fields['status'].initial = 'complete'
        self.fields['type'].initial = 'bouldering'
        self.fields['location'].choices = tuple([(x.strip(),x.strip()) for x in gym.location_options.split('\n')])
        self.instance.gym = gym
        if user.gym == gym:
            self.fields['setter'].initial = user

    class Meta:
        fields = ['type', 'image', 'grade', 'location', 'date_set', 'setter', 'name', 'notes', 'status', 'color1', 'color2']
        model = Route
        widgets = {
        'notes': forms.Textarea(attrs={'rows':3, 'cols':10}),
        'color1': forms.Select(attrs=dict(id="route-color")),
        'color2': forms.Select(attrs=dict(id="route-color2")),
        'image': forms.FileInput(),
        'date_set': forms.DateInput(attrs=dict(id="route-date-set"), format="%m/%d/%Y"),
        'type': forms.RadioSelect(),
        }

class GymSettingsForm(ModelForm):

    class Meta:
        fields = ['name', 'named_routes', 'location_options']
        model=Gym
