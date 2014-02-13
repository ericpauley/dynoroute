from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'routes.views.home', name='home'),
    url(r'^login/$', 'routes.views.login', name='login'),
    url(r'^signup/$', 'routes.views.signup', name='signup'),
)
