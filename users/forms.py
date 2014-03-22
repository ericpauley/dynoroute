from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class RegistrationForm(UserCreationForm):
  def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username, gym=None)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

class CustomSignupForm(forms.Form):
    name = forms.CharField()

    def signup(self, request, user):
        user.save()
