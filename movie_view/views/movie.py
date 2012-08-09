# import tmdb # make sure to install pip and install requests
from tmdb3 import set_key, set_locale, searchMovie
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
import string

def show(request, name):
    name = parse_movie(name)

    ua = request.META.get('HTTP_USER_AGENT', 'unknown')

    if name == '':
        raise Http404()
    else:
        t = get_template('movie.html')
        movie_id = process_movie(name)
        html = t.render(Context({'movie': name, 'id': movie_id}))
        return HttpResponse(html)

def parse_movie(name):
    name = name.split('-')
    if name == '':
        return None
    else:
        return " ".join(name).title()

def process_movie(name):
    set_key('36fb5f623484f4b2680f492005762f31') #store this key somewhere
    set_locale()
    try:
        movie = searchMovie(name)
        if None == movie:
            return None

        return movie[0]
    except:
        return None


