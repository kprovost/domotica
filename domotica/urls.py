from django.urls import include, re_path
from django.conf import settings
from django.views.static import serve
import django
import domotica
import domotica.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    re_path(r'^$', domotica.views.front, name='front'),
    re_path(r'^lightgroups$', domotica.views.lightgroups, name='lightgroups'),
    re_path(r'^login$', domotica.views.do_login, name='login'),
    re_path(r'^lightgroup/(?P<groupName>.*)', domotica.views.lightgroup, name='lightgroup'),
    re_path(r'^lightswitch/(?P<action>.*)', domotica.views.lightswitch, name='lightswitch'),
    re_path(r'^light/settings/(?P<id>\d+)$', domotica.views.lightsettings, name='lightsettings'),
    re_path(r'^alarm$', domotica.views.alarm_index, name='alarm'),
    re_path(r'^alarm_action/(?P<action>.*)$', domotica.views.alarm_action, name='alarm_action'),
    re_path(r'^power$', domotica.views.powerplug, name='power'),
    re_path(r'^powerplug/(?P<action>.*)/(?P<ID>.*)', domotica.views.powerswitch, name='powerswitch'),
    re_path(r'^heating$', domotica.views.heating, name='heating'),
    re_path(r'^heating/toggle/(?P<ID>.*)', domotica.views.heatingtoggle, name='heatingtoggle'),
    re_path(r'^heating/history$', domotica.views.heatinghistory, name='heatinghistory'),
    re_path(r'^heating/graph/(?P<period>.*)$', domotica.views.heatinggraph, name='heating_graph'),

    # Examples:
    # re_path(r'^$', domotica.views.home, name='home'),
    # re_path(r'^domotica/', include('domotica.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # re_path(r'^admin/', include(admin.site.urls)),

    re_path(r'^static/(?P<path>.*)$', serve)
]
