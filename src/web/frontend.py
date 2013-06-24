from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from web.lib import service
from web import models
import settings
from web.lib import utils

@csrf_protect
def new_post(request):
    """Adding new post."""
    syntaxes = models.Syntax.objects.all().order_by('name')
    visitor  = utils.get_visitor(request.VISITOR_UUID)
    c = RequestContext(request, {
        'syntaxes' : syntaxes,
        'visitor'  : visitor
    })

    if request.method == 'POST':
        input     = request.POST['input']

        # No input specified
        if (input.strip() == '' and not request.FILES) or request.POST.get('skey') != settings.ANTISPAM_KEY:
            return HttpResponseRedirect(reverse('new_post'))

        # Uploaded file too large
        if request.FILES and request.FILES['file'].size > 1048576:
            return HttpResponseRedirect(reverse('new_post'))

        # Post preview
        if request.POST['submiter'] == 'Preview':
            # File upload
            if request.FILES:
                input = request.FILES['file'].read()
                if request.POST['syntax'] == '':
                    # Guess lexer by filename
                    lexer = service.get_lexer(input=input, filename=request.FILES['file'].name)
                else:
                    # Apply selected syntax on uploaded file
                    lexer = service.get_lexer(input=input, syntax_aliases=request.POST['syntax'])
            # Pasted text
            else:
                lexer = service.get_lexer(input=input, syntax_aliases=request.POST['syntax'])
            formatter, input = service.get_formatter(input, bool(int(request.POST['wrapping'])))

            # Format the message
            finput = service.highlight(input, lexer, formatter)

            data = request.POST.copy()
            data.update({
                'syntax'       : ','.join(lexer.aliases),
                'visitor_uuid' : request.COOKIES.get(settings.VISITOR_COOKIE_NAME),
                'input'        : input
            })
            c.update({
                'finput'       : finput,
                'finput_styles': formatter.get_style_defs('.highlight'),
                'finput_info'  : service.get_meta(input),
                'data'         : data,
            })
        # Post submission
        if request.POST['submiter'] == 'Paste':
            data = dict(request.POST.items())
            data.update({
                'visitor_uuid' : request.COOKIES.get(settings.VISITOR_COOKIE_NAME),
                'ip'           : request.META.get('REMOTE_ADDR'),
                'user_agent'   : request.META.get('HTTP_USER_AGENT')
            })

            # File upload
            if request.FILES:
                input = request.FILES['file'].read()
                data.update({
                    'input'        : input,
                    'filename'     : request.FILES['file'].name,
                    'filesize'     : request.FILES['file'].size,
                    'file_mimetype': request.FILES['file'].content_type
                })

            post   = service.persist_post(**data)

            # Setting visitor post options
            visitor_attrs = visitor.attributes
            posts  = visitor_attrs.get('posts', [])
            posts += [post.id]
            visitor_attrs['posts']   = posts
            visitor_attrs['options'] = {
                'syntax'     : data['syntax'],
                'expiration' : data['expiration'],
                'exposure'   : data['exposure'],
                'wrapping'   : data['wrapping'],
                'name'       : data['name'],
                'email'      : data['email']
            }
            visitor.attributes = visitor_attrs
            visitor.save()
            return HttpResponseRedirect(reverse('show_post', kwargs={'token': post.token}))
    return render_to_response('frontend/new_post.html', context_instance=c)


def show_post(request, token):
    """Showing highlighted post."""
    try:
        post = models.Post.objects.select_related('syntax').get(token=token)
    except Exception:
        return HttpResponseNotFound()

    lexer            = service.get_lexer(syntax_aliases=post.syntax.aliases)
    formatter, input = service.get_formatter(post.body, post.wrapping)
    finput           = service.highlight(input, lexer, formatter)

    return render_to_response('frontend/post.html', context_instance=RequestContext(request, {
        'post'         : post,
        'finput'       : finput,
        'finput_styles': formatter.get_style_defs('.highlight')
    }))


def my_posts(request, syntax=None):
    """Showing list of posts associated with current visitor."""
    visitor       = models.Visitor.objects.get(uuid=request.VISITOR_UUID)
    visitor_attrs = visitor.attributes
    posts_ids     = filter(lambda x: not isinstance(x, basestring), visitor_attrs.get('posts', []))
    posts         = models.Post.objects.filter(id__in=posts_ids).select_related('syntax')\
                     .order_by('-inserted')\
                     .defer('body')
    if syntax is not None:
        posts = posts.filter(syntax__aliases__exact=syntax)
    posts = posts[:200]
    visitor_attrs['posts'] = posts_ids
    visitor.attributes = visitor_attrs
    visitor.save()
    return render_to_response('frontend/my_posts.html', context_instance=RequestContext(request, {
        'posts': posts
    }))


def archive(request, syntax=None):
    """Viewing archived public posts."""
    if syntax is not None:
        posts = models.Post.objects.filter(exposure=models.Post.EXPOSURE_PUBLIC)\
                .filter(syntax__aliases__exact=syntax)
    else:
        posts = models.Post.objects.filter(exposure=models.Post.EXPOSURE_PUBLIC)
    posts = posts.defer('body').order_by('-inserted').select_related('syntax')[:100]

    return render_to_response('frontend/archive.html', context_instance=RequestContext(request, {
        'posts': posts  
    }))


def raw(request, token):
    """Showing post in raw form; no syntax highlighting applied."""
    try:
        post = models.Post.objects.get(token=token)
    except Exception:
        return HttpResponseNotFound()
    return HttpResponse(post.body, mimetype='text/plain; charset=utf-8')

def download(request, token):
    """Showing download dialog."""
    try:
        post = models.Post.objects.select_related('syntax').get(token=token)
    except Exception:
        return HttpResponseNotFound()
    ext = post.syntax.filetypes.split(',')[0].replace('*', '')
    if ext == '':
        ext = '.txt'
    mimetype = post.syntax.mimetypes.split(',')[0]
    if mimetype == '':
        mimetype = 'text/plain'
    response = HttpResponse(post.body, mimetype=mimetype)
    response['Content-Disposition'] = 'attachment; filename='+post.token+ext
    return response

def view(request, token):
    """Handler for running various codes in browser, like html or js."""
    try:
        post = models.Post.objects.select_related('syntax').get(token=token)
    except Exception:
        return HttpResponseNotFound()

    # Disable viewing of unsupported syntaxes
    if post.syntax.name not in settings.VIEWABLE_SYNTAXES:
        raise Http404

    # Viewing html code
    if post.syntax.name == 'HTML':
        # Code is XHTML compliant
        if post.body.find('"-//W3C//DTD XHTML') != -1:
            return HttpResponse(post.body, mimetype='application/xhtml+xml; charset=utf-8')
        # Code is HTML compliant
        else:
            return HttpResponse(post.body, mimetype='text/html; charset=utf-8')

    # Other viewable syntaxes
    if post.syntax.name in settings.VIEWABLE_SYNTAXES:
        return HttpResponse(post.body, mimetype=post.syntax.mimetypes.split(',')[0]+'; charset=utf-8')