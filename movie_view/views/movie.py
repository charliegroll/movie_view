import tmdb # make sure to install pip and install requests
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
import string

def show(request, offset):
    name = parse_movie(offset)

    ua = request.META.get('HTTP_USER_AGENT', 'unknown')

    if name == '':
        raise Http404()
    else:
        t = get_template('movie.html')
        html = t.render(Context({'movie': name}))
        return HttpResponse(html)

def parse_movie(name):
    name = name.split('-')
    if name == '':
        return null
    else:
        return " ".join(name).title()
