import logging
from django.http import HttpResponse
from web import models
from datetime import datetime, timedelta
from django.db.models.query_utils import Q

log = logging.getLogger(__name__)

def collect_expired(request):
    """Pernamently deleting expired posts."""
    try :
        log.debug('Collecting and deleting expired posts')
        models.Post.objects.filter(expires__lte=datetime.now()).delete()
        return HttpResponse('Expired posts collected successfuly', mimetype='text/plain')
    except Exception:
        log.exception('Error while collecting and deleting expired posts')
        raise

def clean_visitors(request):
    """Pernamently deleting inactive visitors."""
    try:
        log.debug('Collecting and deleting inactive visitors')
        one_day_before   = datetime.now() - timedelta(days=1)
        half_year_before = datetime.now() - timedelta(days=183)

        # Deleting robots or with no activity for more than one year
        models.Visitor.objects.filter(
            (Q(body='{}') & Q(inserted__lte=one_day_before))
            |
            (~Q(body='{}') & Q(updated__lte=half_year_before))
        ).delete()
        return HttpResponse('Inactive visitors cleaned successfuly', mimetype='text/plain')
    except Exception:
        log.exception('Error while cleaning Visitor table')
        raise