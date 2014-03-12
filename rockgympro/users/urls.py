from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from gyms.forms import GymAuthForm
from users.forms import RegistrationForm

urlpatterns = patterns('',

    url(r'^login/$', 'django.contrib.auth.views.login', dict(template_name="login.html", authentication_form=GymAuthForm), name='login'),
    url(r'^signup/$', 'django.contrib.auth.views.login', dict(template_name="signup.html", authentication_form=GymAuthForm), name='signup'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
)
