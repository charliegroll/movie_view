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
        movies = process_movies(name)

        if None == movies:
            html = t.render(Context({'movie': name, 'id': '<null>'}))
        else:
            l = len(movies)
            if l == 1:
                html = t.render(Context({'movie': name, 'id': movies[0].title}))
            else:
                #handle multiple responses
                #names = ''
                #for x in movies:
                #    names = names + x.title + '  '
                names = movies[0].title
                html = t.render(Context({'movie':name, 'id': names}))

        return HttpResponse(html)

def parse_movie(name):
    name = name.split('-')
    if name == '':
        return None
    else:
        return " ".join(name).title()

def process_movies(name):
    set_key('36fb5f623484f4b2680f492005762f31') #store this key somewhere
    set_locale()

    try:
        movies = searchMovie(name)
        if None == movies:
            return None
        return movies
    except:
        return None


