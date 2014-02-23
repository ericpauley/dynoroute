from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rockgympro.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('users.urls')),
    url(r'^(?P<gym>\w{3,32})/', include('gyms.urls')),
)
