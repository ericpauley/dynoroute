from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User
from gyms.models import Gym

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

class UserChangeForm(UserChangeForm):
    class Meta:
        model=User

class MyUserAdmin(UserAdmin):
   add_form = UserCreationForm
   form = UserChangeForm
   fieldsets = UserAdmin.fieldsets + (("Gym Info", {'fields': ('gym', 'level')}),)

# Now register the new UserAdmin...
admin.site.register(User, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
