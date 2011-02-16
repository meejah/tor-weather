import os
import sys

sys.path.append('/home/weather/opt/current')
sys.path.append('/home/weather/opt/current/weather')
#sys.path.append('/home/weather/opt/current/weather/weatherapp')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
