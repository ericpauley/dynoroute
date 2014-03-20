from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from gyms.forms import GymAuthForm
from users.forms import RegistrationForm

urlpatterns = patterns('',

    url(r'^dashboard/$', 'users.views.dashboard', name='dashboard')
)
