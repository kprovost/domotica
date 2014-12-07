from django.conf.urls import patterns, include, url
from django.conf import settings
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'domotica.views.front', name='front'),
    url(r'^lightgroups$', 'domotica.views.lightgroups', name='lightgroups'),
    url(r'^login$', 'domotica.views.do_login', name='login'),
    url(r'^lightgroup/(?P<groupName>.*)', 'domotica.views.lightgroup', name='lightgroup'),
    url(r'^lightswitch/(?P<action>.*)', 'domotica.views.lightswitch', name='lightswitch'),
    url(r'^light/settings/(?P<id>\d+)$', 'domotica.views.lightsettings', name='lightsettings'),
    url(r'^alarm$', 'domotica.views.alarm_index', name='alarm'),
    url(r'^alarm_action/(?P<action>.*)$', 'domotica.views.alarm_action', name='alarm_action'),
    url(r'^power$', 'domotica.views.powerplug', name='power'),
    url(r'^powerplug/(?P<action>.*)/(?P<ID>.*)', 'domotica.views.powerswitch', name='powerswitch'),
    url(r'^heating$', 'domotica.views.heating', name='heating'),
    url(r'^heating/toggle/(?P<ID>.*)', 'domotica.views.heatingtoggle', name='heatingtoggle'),
    url(r'^heating/history$', 'domotica.views.heatinghistory', name='heatinghistory'),
    url(r'^heating/graph/(?P<period>.*)$', 'domotica.views.heatinggraph', name='heating_graph'),

    # Examples:
    # url(r'^$', 'domotica.views.home', name='home'),
    # url(r'^domotica/', include('domotica.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve')
)
