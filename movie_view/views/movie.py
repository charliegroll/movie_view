from tmdb3 import set_key, set_locale, searchMovie, Movie
from django.http import HttpResponse, Http404
from django import template
from django.template import Context
from django.template.loader import get_template
import string

moviesToDisplay = list()

class DisplayMovie:
    def __init__(self, movie, poster):
        self.movie = movie
        self.poster = poster

def show(request, name):
    name = parse_movie(name)

    #ua = request.META.get('HTTP_USER_AGENT', 'unknown')

    if name == '':
        raise Http404()
    else:
        t = get_template('movie.html')
        process_movies(name)

        if None == moviesToDisplay:
            html = t.render(Context({'movie': name,}))
        else:
            l = len(moviesToDisplay)
            if l == 1:
                html = t.render(Context({'movie': name, 'id': mo}))
            else:
                #handle multiple responses
                #names = ''
                #for x in movies:
                #    names = names + x.title + '  '
                movie = movies[0]
                html = t.render(Context({'movie': name, 'id': movie}))

        return HttpResponse(html)

def showall(request):
    t = get_template('home.html')

    # get movie list
    movies = process_movies('Batman')
    html = t.render(Context({'movies': moviesToDisplay,}))

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

    movies = searchMovie(name)

    for m in movies:
        p = m.poster

        if  p:
            d = DisplayMovie(m,  m.poster.geturl('w154'))
        else:
            d = DisplayMovie(m, '')

        moviesToDisplay.append(d)

    moviesToDisplay.sort(key=lambda x: (x.movie.releasedate.year if x.movie.releasedate else 0), reverse=True)
