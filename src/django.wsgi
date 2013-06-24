import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# production virtualenv
sys.path.append('/opt/virtualenvs/openpaste/lib/python2.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp/openpaste/python-eggs'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()