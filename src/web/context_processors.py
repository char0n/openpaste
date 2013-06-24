import logging
import settings
from web import models

log = logging.getLogger(__name__)

def common_data(request):
    # current active link in main menu
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'VIEWABLE' : settings.VIEWABLE_SYNTAXES,
        'VISITOR'  : models.Visitor.objects.get(uuid=request.VISITOR_UUID)
    }
