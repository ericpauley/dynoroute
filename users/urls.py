from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from gyms.forms import GymAuthForm
from users.forms import RegistrationForm
from users.views import *

urlpatterns = patterns('',

    url(r'^dashboard/$', 'users.views.dashboard', name='dashboard'),
    url(r'^favorites/$', 'users.views.favorites', name='favorites'),
    url(r'^sends/$', 'users.views.sends', name='sends'),
    url(r'^profile/edit/$', ProfileEditView.as_view(), name="edit_profile"),
)
