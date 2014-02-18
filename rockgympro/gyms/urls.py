from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'gyms.views.gym_page', name='gym_page'),
    url(r'^routes$', 'gyms.views.routes', name='gym_routes'),
    url(r'^route/(?P<route>\d+)/$', 'gyms.views.route', name='gym_route'),
)
