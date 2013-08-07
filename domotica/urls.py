from django.conf.urls import patterns, include, url
from django.conf import settings
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'domotica.views.index', name='index'),
    url(r'^login$', 'domotica.views.do_login', name='login'),
    url(r'^lightgroup/(?P<groupName>.*)', 'domotica.views.lightgroup', name='lightgroup'),
    url(r'^lightswitch/(?P<action>.*)', 'domotica.views.lightswitch', name='lightswitch'),
    url(r'^light/settings/(?P<id>\d+)$', 'domotica.views.lightsettings', name='lightsettings'),
    url(r'^alarm$', 'domotica.views.alarm', name='alarm'),
    url(r'^power$', 'domotica.views.power', name='power'),
    url(r'^heating$', 'domotica.views.heating', name='heating'),

    # Examples:
    # url(r'^$', 'domotica.views.home', name='home'),
    # url(r'^domotica/', include('domotica.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve')
)
