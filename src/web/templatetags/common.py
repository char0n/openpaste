from django import template
from web.lib.utils import get_age as util_get_age
from datetime import datetime
import time
import settings

register = template.Library()

@register.simple_tag
def get_age(date_time):
    unow       = time.mktime(datetime.now().timetuple())
    udate_time = time.mktime(date_time.timetuple())
    return util_get_age(unow - udate_time)

@register.simple_tag
def get_future(date_time):
    unow       = time.mktime(datetime.now().timetuple())
    udate_time = time.mktime(date_time.timetuple())
    future     = util_get_age(udate_time - unow)
    if future.startswith('-'):
        return '0 seconds'
    else:
        return future
