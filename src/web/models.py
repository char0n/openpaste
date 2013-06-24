from django.db import models
from mptt.models import MPTTModel
import json

class TimestampAware(models.Model):
    """
    Ancestor for models with timestamable behaviour
    """
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Api(object):
    WEB = 1

    CHOICES = (
        (WEB, u'Submission via web forms'),
    )
    
class Syntax(models.Model):
    name      = models.CharField(max_length=50, blank=False, db_index=True)
    aliases   = models.CharField(max_length=255, blank=True)
    filetypes = models.CharField(max_length=255, blank=True)
    mimetypes = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'syntaxes'

class Subdomain(TimestampAware):
    name = models.CharField(max_length=20, blank=False, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'subdomains'


class Post(MPTTModel, TimestampAware):

    EXPOSURE_PUBLIC  = 1
    EXPOSURE_PRIVATE = 2

    EXPOSURE_CHOICES = (
        (EXPOSURE_PUBLIC , u'Public post exposure'),
        (EXPOSURE_PRIVATE, u'Private post exposure')
    )

    author         = models.CharField(max_length=20, blank=True)
    syntax         = models.ForeignKey('web.Syntax', null=True, db_index=True)
    body           = models.TextField(blank=False, null=False)
    parent         = models.ForeignKey('self', null=True, blank=True, related_name='children')
    expires        = models.DateTimeField(blank=True, null=True, db_index=True)
    exposure       = models.PositiveSmallIntegerField(choices=EXPOSURE_CHOICES, default=EXPOSURE_PUBLIC)
    email          = models.CharField(max_length=75, blank=True, db_index=True)
    api            = models.PositiveSmallIntegerField(choices=Api.CHOICES, default=Api.WEB)
    token          = models.CharField(max_length=8, null=False, blank=False, db_index=True)
    description    = models.TextField(blank=True)
    subdomain      = models.ForeignKey('web.Subdomain', null=True, db_index=True)
    wrapping       = models.BooleanField(default=True)
    diff           = models.TextField(blank=True)
    views          = models.PositiveIntegerField(default=1)
    visitor_uuid   = models.CharField(max_length=36, blank=True)
    meta           = models.TextField(blank=False, default='{}')

    @property
    def metadata(self):
        return json.loads(self.meta)

    @metadata.setter
    def metadata(self, value):
        self.meta = json.dumps(value)

    @metadata.deleter
    def metadata(self):
        self.meta = '{}'

    def __unicode__(self):
        return self.token

    class Meta:
        db_table = 'posts'

class Visitor(TimestampAware):
    uuid = models.CharField(max_length=36, blank=False, null=False, unique=True)
    body = models.TextField(blank=False, default='{}')

    @property
    def attributes(self):
        return json.loads(self.body)

    @attributes.setter
    def attributes(self, value):
        self.body = json.dumps(value)

    @attributes.deleter
    def attributes(self):
        self.body = '{}'

    def __unicode__(self):
        return self.uuid

    class Meta:
        db_table = 'visitors'