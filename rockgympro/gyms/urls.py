from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'gyms.views.home', name='home'),
    url(r'^route/$', 'routes.views.route', name='route')
)
