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
    re_path(r'^login$', domotica.views.do_login, name='login'),
    re_path(r'^lightswitch/(?P<action>.*)', domotica.views.lightswitch, name='lightswitch'),
    re_path(r'^lights', domotica.views.lights, name='lights'),
    re_path(r'^alarm_action/(?P<action>.*)$', domotica.views.alarm_action, name='alarm_action'),
    re_path(r'^alarm$', domotica.views.alarm_index, name='alarm'),

    # Examples:
    # re_path(r'^$', domotica.views.home, name='home'),
    # re_path(r'^domotica/', include('domotica.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # re_path(r'^admin/', include(admin.site.urls)),

    re_path(r'^static/(?P<path>.*)$', serve)
]
