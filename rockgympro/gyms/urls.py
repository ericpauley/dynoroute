from django.conf.urls import patterns, include, url
from gyms.views import *

urlpatterns = patterns('',
    url(r'^$', GymPage.as_view(), name='gym_page'),
    url(r'^routes$', RoutesPage.as_view(), name='gym_routes'),
    url(r'^route/(?P<route>\w{5})/$', RoutePage.as_view(), name='gym_route'),
)
