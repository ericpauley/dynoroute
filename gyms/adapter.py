from allauth.account.adapter import DefaultAccountAdapter

from allauth.account import app_settings
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _

class GymAccountAdapter(DefaultAccountAdapter):

    def clean_username(self, username):
        """
        Validates the username. You can hook into this if you want to
        (dynamically) restrict what usernames can be chosen.
        """
        from django.contrib.auth.forms import UserCreationForm
        USERNAME_REGEX = UserCreationForm().fields['username'].regex
        if not USERNAME_REGEX.match(username):
            raise forms.ValidationError(_("Usernames can only contain "
                                          "letters, digits and @/./+/-/_."))

        # TODO: Add regexp support to USERNAME_BLACKLIST
        if username in app_settings.USERNAME_BLACKLIST:
            raise forms.ValidationError(_("Username can not be used. "
                                          "Please use other username."))
        username_field = app_settings.USER_MODEL_USERNAME_FIELD
        assert username_field
        user_model = get_user_model()
        try:
            query = {username_field + '__iexact': username, 'gym':None}
            user_model.objects.get(**query)
        except user_model.DoesNotExist:
            return username
        raise forms.ValidationError(_("This username is already taken. Please "
                                      "choose another."))

    def login(self, request, user):
        from django.contrib.auth import login
        # HACK: This is not nice. The proper Django way is to use an
        # authentication backend
        if not hasattr(user, 'backend'):
            user.backend \
                = 'rockgympro.backends.CaseInsensitiveModelBackend'
        login(request, user)
