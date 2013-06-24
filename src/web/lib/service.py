from pygments.lexers import  get_lexer_by_name, guess_lexer, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
import web.lib.utils
import pygments
import re
import logging
from web import models
from datetime import datetime, timedelta

log = logging.getLogger(__name__)

def get_lexer(input=None, syntax=None, syntax_aliases=None, filename=None):
    """Getting appropriate lexer."""
    log.debug('Getting lexer for code highlighting')
    try:
        if input is None and syntax is None and syntax_aliases is None and filename is None:
            return get_lexer_by_name('text')
        if syntax:
            return get_lexer_by_name(syntax.aliases.split(',')[0])
        elif syntax_aliases:
            return get_lexer_by_name(syntax_aliases.split(',')[0])
        elif filename:
            return get_lexer_for_filename(filename, input)
        elif input:
            return guess_lexer(input)
    except Exception:
        log.exception('Something went wrong while getting lexer')
        return get_lexer_by_name('text')


def get_hl_lines(code):
    """Getting number of tobe highlighted lines."""
    log.debug('Getting number of tobe highlighted lines')
    i = 1
    lines = []
    for line in code.split('\n'):
        if line.startswith('@h@'):
            lines.append(i)
        i += 1
    return lines


def remove_hl_lines(code):
    """Removing markers from highlighted lines."""
    log.debug('Removing markers from highlighted lines.')
    hl_regex  = re.compile(r'^@h@', re.MULTILINE)
    return re.sub(hl_regex, '', code)

def clean(code):
    """Cleaning input data from unwanted content."""
    log.debug('Cleaning input data from unwanted content')
    return remove_hl_lines(code.rstrip())

def get_formatter(input, wrapping=False):
    log.debug('Getting formatter for code highlighting')
    hl_lines = get_hl_lines(input)
    if hl_lines:
        input = remove_hl_lines(input)
    if wrapping is False:
        return (HtmlFormatter(
            linenos=True, style='trac', encoding='utf-8', nowrap=False, hl_lines=hl_lines,
            lineanchors='line', anchorlinenos=True
        ), input.rstrip())
    else:
        return (HtmlFormatter(
            linenos=False, style='trac', encoding='utf-8', nowrap=True, hl_lines=hl_lines
        ), input.rstrip())


def highlight(input, lexer, formatter):
    """Highlighting code using appropriate lexer and formatter."""
    log.debug('Highlighting code using appropriate lexer and formatter')
    return pygments.highlight(input, lexer, formatter)


def get_meta(input):
    """Getting code metadata."""
    log.debug('Getting code metadata')
    clean_input = clean(input)
    return {
        'chars': len(clean_input),
        'lines': len(clean_input.split('\n')),
        'size' : web.lib.utils.get_string_size(clean_input)
    }


def persist_post(**kwargs):
    """Persistence of new post."""
    try:
        log.debug('Persiting new post')
        p              = models.Post()
        p.author       = kwargs['name'].strip()
        if kwargs['syntax'] != '':
            p.syntax   = models.Syntax.objects.get(aliases=kwargs['syntax'])
        else:
            lexer      = get_lexer(input=kwargs['input'], filename=kwargs.get('filename'))
            p.syntax   = models.Syntax.objects.get(aliases=','.join(lexer.aliases))
        p.body         = clean(kwargs['input'])
        if kwargs['expiration'] != '0':
            p.expires  = datetime.now() + timedelta(seconds=int(kwargs['expiration']))
        else:
            p.expires  = None
        p.exposure     = kwargs['exposure']
        p.email        = kwargs['email'].strip()
        p.api          = models.Api.WEB
        p.token        = web.lib.utils.generate_token()
        p.description  = kwargs['description']
        p.wrapping     = bool(int(kwargs['wrapping']))
        meta = get_meta(p.body)
        if 'ip' in kwargs and 'user_agent' in kwargs:
            meta.update({'ip': kwargs['ip'], 'user_agent': kwargs['user_agent']})
        if 'filename' in kwargs:
            meta.update({
                'filename': kwargs['filename'], 'filesize': kwargs.get('filesize'), 'file_mimetype': kwargs.get('file_mimetype')
            })
        p.metadata     = meta
        p.visitor_uuid = kwargs.get('visitor_uuid', '')
        p.save()

        if kwargs.get('visitor_uuid') is not None:
            log.debug('Assigning new post to visitor')
            try:
                visitor            = models.Visitor.objects.get(uuid=kwargs.get('visitor_uuid'))
                attrs              = visitor.attributes
                if 'posts' not in attrs:
                    attrs['posts'] = []
                attrs['posts'].append(p.token)
                visitor.attributes = attrs
                visitor.save()
            except Exception:
                log.exception('Error while assigning new post to visitor')

        return p
    except Exception:
        log.exception('Error while persisting new post')
        raise