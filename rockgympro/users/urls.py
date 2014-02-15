from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^login/$', 'users.views.login', name='login'),
    url(r'^signup/$', 'users.views.signup', name='signup'),
    url(r'^$', 'users.views.home', name='home'),
)
