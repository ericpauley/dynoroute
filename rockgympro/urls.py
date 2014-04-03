from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rockgympro.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('allauth.urls')),
    url(r'^', include('users.urls')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^gyms/', 'gyms.views.gym_list', name='gym_list'),
    url(r'^about/', 'gyms.views.about', name='about'),
    url(r'^home/$', 'users.views.home', name='home'),
    url(r'^(?P<gym>\w{3,32})/', include('gyms.urls')),
    url(r'^$', 'users.views.landing', name='landing'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
