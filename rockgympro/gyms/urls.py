from django.conf.urls import patterns, include, url
from gyms.views import *

urlpatterns = patterns('',
    url(r'^$', GymPage.as_view(), name='gym_page'),
    url(r'^routes/$', RoutesPage.as_view(), name='gym_routes'),
    url(r'^route/$', redirect, dict(to='gym_routes')),
    url(r'^routes/(?P<route>\w{5})/$', RoutePage.as_view(), name='gym_route'),
    url(r'^admin/routes/(?P<route>\w{5})/$', GymAdminRouteEdit.as_view(), name='gym_route_edit'),
    url(r'^admin/$', GymDashboard.as_view(), name='gym_dashboard'),
    url(r'^admin/routes/add/$', GymAdminRouteAdd.as_view(), name='gym_route_add'),
    url(r'^admin/settings/$', GymSettings.as_view(), name='gym_settings')

)
