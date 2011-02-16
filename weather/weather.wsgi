import os
import sys

sys.path.append('/home/weather/opt/weather2')
sys.path.append('/home/weather/opt/weather2/weather')
#sys.path.append('/home/weather/opt/weather2/weather/weatherapp')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
