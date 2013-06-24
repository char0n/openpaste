from django.utils.encoding import smart_unicode
import re
from htmlentitydefs import name2codepoint
import unicodedata
from uuid import uuid4
from random import choice
import string
import math
from web import models
import logging

log = logging.getLogger(__name__)

def slugify(s, entities=True, decimal=True, hexadecimal=True,
   instance=None, slug_field='slug', filter_dict=None):
    s = smart_unicode(s)

    #character entity reference
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

    #decimal character reference
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass

    #hexadecimal character reference
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass

    #translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

    #replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())

    #remove redundant -
    s = re.sub('-{2,}', '-', s).strip('-')

    slug = s
    if instance:
        def get_query():
            query = instance.__class__.objects.filter(**{slug_field: slug})
            if filter_dict:
                query = query.filter(**filter_dict)
            if instance.pk:
                query = query.exclude(pk=instance.pk)
            return query
        counter = 1
        while get_query():
            slug = "%s-%s" % (s, counter)
            counter += 1
    return slug


def generate_token():
    token = ''
    for c in str(uuid4())[:8]:
        if c.isalpha() and choice([True, False]):
            c = c.upper()
        token += c
    if choice([True, False]):
        return token[::-1]
    else:
        return token

def int2base(integer, base):
        if not integer: return '0'
        sign = 1 if integer > 0 else -1
        alphanum = string.digits + string.ascii_lowercase
        nums = alphanum[:base]
        res = ''
        integer *= sign
        while integer:
                integer, mod = divmod(integer, base)
                res += nums[mod]
        return ('' if sign == 1 else '-') + res[::-1]

def get_string_size(string):
    if len(string) <= 1024:
        return str(len(string) * 8) + ' b'
    else:
        return str(round(len(string) / 1024 * 8, 2)) + ' kb'

def get_age(seconds):
    minute = 60
    hour   = 60 * minute
    day    = 24 * hour
    year   = 365 * day

    age = ''
    if seconds == 1:
        age = '1 second'
    elif seconds < minute:
        age = str(int(seconds)) + ' seconds'
    elif seconds >= minute and seconds < hour and seconds < minute * 2:
        age = '1 minute'
    elif seconds >= minute and seconds < hour:
        age = str(int(math.ceil(seconds / minute))) + ' minutes'
    elif seconds >= hour and seconds < day and seconds < hour * 2:
        age = '1 hour'
    elif seconds >= hour and seconds < day:
        age = str(int(math.ceil(seconds / hour))) + ' hours'
    elif seconds >= day and seconds < year and seconds < day * 2:
        age = '1 day'
    elif seconds >= day and seconds < year:
        age = str(int(math.ceil(seconds / day))) + ' days'
    elif seconds >= year and seconds < year * 2:
        age = '1 year'
    elif seconds >= year:
        age = str(int(math.ceil(seconds / year))) + ' years'
    return age

def get_visitor(uuid):
    """Getting visitor by uuid."""
    log.debug('Getting visitor by uuid(%s)', uuid)
    try:
        visitor = models.Visitor.objects.get(uuid=uuid)
    except Exception:
        visitor      = models.Visitor()
        visitor.uuid = uuid
        visitor.save()
    return visitor
