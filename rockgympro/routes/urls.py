from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'routes.views.home', name='home'),

)
