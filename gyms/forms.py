from gyms.models import Route, Gym
from django.forms import ModelForm
from users.models import User
from django.utils import timezone
from django import forms

from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class ReadOnlyMixin(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReadOnlyMixin, self).__init__(*args, **kwargs)
        for name in self.get_readonly_fields():
            self.fields[name].widget.attrs['readonly'] = True
            self.fields[name].widget.attrs['disabled'] = True

    def clean(self):
        print "egg"
        for name in self.get_readonly_fields():
            print name
            self.cleaned_data[name] = getattr(self.instance, name)
        return self.cleaned_data

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
        self.fields['setter'].initial = user

    class Meta:
        fields = ['type', 'image', 'grade', 'location', 'date_set', 'setter', 'name', 'notes', 'status', 'color1', 'color2']
        model = Route
        widgets = {
        'notes': forms.Textarea(attrs={'rows':3, 'cols':10}),
        'color1': forms.Select(attrs=dict(id="route-color")),
        'color2': forms.Select(attrs=dict(id="route-color2")),
        'image': forms.FileInput(),
        'date_set': forms.DateInput(attrs={'id':"route-date-set", 'data-date-autoclose':"true", "data-auto-close":'true'}, format="%m/%d/%Y"),
        'type': forms.RadioSelect(),
        }

class GymSettingsForm(ModelForm):

    class Meta:
        fields = ['name', 'named_routes', 'location_options']
        model=Gym

class GymAuthForm(AuthenticationForm):

    def __init__(self, request, gym=None, *args, **kwargs):
        self.gym = gym or None
        super(GymAuthForm, self).__init__(request, *args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password, gym=self.gym)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class EmployeeCreationForm(UserCreationForm):

    name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'level', 'email')

    def __init__(self, gym, *args, **kwargs):
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
        self.instance.gym = gym
        self.fields['level'].choices = self.fields['level'].choices[2:]

    def get_readonly_fields(self):
        return []

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username, gym=self.instance.gym or None)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

class EmployeeUpdateForm(EmployeeCreationForm):

    password = None
    username = None

    name = forms.CharField(required=True)

    password1 = forms.CharField(label="New Password",
        widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.", required=False)

    class Meta:
        model = User
        fields = ('name', 'level', 'email')

    def __init__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        if self.instance.level == 10000:
            del self.fields['level']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
