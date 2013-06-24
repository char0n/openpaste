from django.conf.urls.defaults import *
from django.contrib import admin
import settings

admin.autodiscover()

# frontend patterns
frontend_patterns = patterns('web.frontend',
    url(r'^$', 'new_post', name='new_post'),
    url(r'^my-posts/$', 'my_posts', name='my_posts'),
    url(r'^my-posts/(?P<syntax>.*)$', 'my_posts', name='my_posts'),
    url(r'^archive/$', 'archive', name='archive'),
    url(r'^archive/(?P<syntax>.*)$', 'archive', name='archive'),
    url(r'^raw/(?P<token>.+)$', 'raw', name='raw'),
    url(r'^download/(?P<token>.+)$', 'download', name='download'),
    url(r'^view/(?P<token>.+)$', 'view', name='view'),
    url(r'^(?P<token>.+)$', 'show_post', name='show_post')
)

# service patterns
services_patterns = patterns('web.services',
    url(r'^collect_expired$', 'collect_expired', name='collect_expired'),
    url(r'^clean_visitors$', 'clean_visitors', name='clean_visitor')
)

urlpatterns = patterns('',
    # private services
    (r'^services/', include(services_patterns)),
    # public frontend
    (r'^', include(frontend_patterns))
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes' : False}),
    ) + urlpatterns