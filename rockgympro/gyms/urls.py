from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'gyms.views.gym_page', name='hgym_page'),
    url(r'^route/(?P<route>\d+)/$', 'gyms.views.route', name='route')
)
