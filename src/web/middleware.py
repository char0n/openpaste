import settings
import logging
import uuid
from web.lib import utils

log = logging.getLogger(__name__)

class VisitorMiddleware(object):
    """Middleware for setting each visitor UUID into cookie."""

    def process_request(self, request):
        if ignore(request):
            return
        if settings.VISITOR_COOKIE_NAME not in request.COOKIES:
            request.VISITOR_UUID = uuid.uuid4()
        else:
            request.VISITOR_UUID = request.COOKIES[settings.VISITOR_COOKIE_NAME]

    def process_response(self, request, response):
        if ignore(request):
            return response

        if settings.VISITOR_COOKIE_NAME not in request.COOKIES:
            log.debug('Setting UUID to new visitor')
            visitor = utils.get_visitor(request.VISITOR_UUID)
            response.set_cookie(settings.VISITOR_COOKIE_NAME, visitor.uuid, max_age=365*24*60*60)
        else:
            log.debug('Extending visitors UUID cookie lifetime')
            visitor = utils.get_visitor(request.COOKIES[settings.VISITOR_COOKIE_NAME])
            response.set_cookie(settings.VISITOR_COOKIE_NAME, visitor.uuid, max_age=365*24*60*60)
        return response
    

def ignore(request):
    """
    Return true if:
     - request is to django admin interface
     - request is to static content/site-media (dev server)
    """
    #result = request.path.startswith(reverse('admin:index')) or request.path.startswith(settings.MEDIA_URL)
    return request.path.startswith(settings.MEDIA_URL)
