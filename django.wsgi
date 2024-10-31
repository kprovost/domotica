import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'domotica.settings'
sys.path.append('/home/kp/libs7comm-python/')

path = '/home/kp/domotica'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
