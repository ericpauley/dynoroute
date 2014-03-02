from django.conf.urls import patterns, include, url
from gyms.views import *

urlpatterns = patterns('',
    url(r'^$', GymPage.as_view(), name='gym_page'),
    url(r'^routes/$', RoutesPage.as_view(), name='gym_routes'),
    url(r'^route/$', redirect, dict(to='gym_routes')),
    url(r'^routes/(?P<route>\w{5})/$', RoutePage.as_view(), name='gym_route'),
    url(r'^routes/(?P<route>\w{5})/(?P<action>send|unsend|favorite|unfavorite|rate)/$', RouteAJAX.as_view(), name='gym_route_ajax'),
    url(r'^admin/routes/(?P<route>\w{5})/$', AdminRouteEdit.as_view(), name='gym_route_edit'),
    url(r'^admin/$', GymDashboard.as_view(), name='gym_dashboard'),
    url(r'^admin/login/$', login, dict(template_name="login.html", authentication_form=GymAuthForm), name='gym_login'),
    url(r'^admin/stats.json$', GymStats.as_view(), name='gym_stats'),
    url(r'^admin/routes/add/$', AdminRouteAdd.as_view(), name='gym_route_add'),
    url(r'^admin/routes/$', AdminRoutesPage.as_view(), name="gym_routes_admin"),
    url(r'^admin/staff/$', AdminStaffPage.as_view(), name="gym_staff_admin"),
    url(r'^admin/staff/add/$', AdminEmployeeAdd.as_view(), name="gym_staff_add"),
    url(r'^admin/staff/(?P<user>[\w.@+-]+)/$', AdminEmployeeUpdate.as_view(), name="gym_staff_update"),
    url(r'^admin/staff/(?P<user>[\w.@+-]+)/delete/$', AdminEmployeeDelete.as_view(), name="gym_staff_delete"),
    url(r'^admin/settings/$', GymSettings.as_view(), name='gym_settings'),

)
