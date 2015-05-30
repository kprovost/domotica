import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'domotica.settings'
sys.path.append('/home/kp/libs7comm-python/')

path = '/home/kp/domotica'
if path not in sys.path:
    sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
