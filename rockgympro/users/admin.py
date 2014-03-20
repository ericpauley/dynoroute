from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _

from users.models import User
from gyms.models import Gym

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'gym', 'level')

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username, gym=self.data['gym'] or None)
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
   fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ("Gym Info", {'fields': ('gym', 'level')}),
    )
   list_display = ('gym', 'username', 'email', 'name', 'is_staff')
   search_fields = ('gym__name', 'gym__slug', 'username', 'name', 'email')
   add_fieldsets = UserAdmin.add_fieldsets + (("Gym Info", {'fields': ('gym', 'level')}),)

# Now register the new UserAdmin...
admin.site.register(User, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
