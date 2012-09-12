from tmdb3 import set_key, set_locale, searchMovie, Movie
from django.http import HttpResponse, Http404
from django import template
from django.template import Context
from django.template.loader import get_template
import string
import bisect
import operator

from filesystem import explore, fileset, MovieFile

movieids = list()
moviesToDisplay = list()

def showall(request):
    t = get_template('home.html')

    # get movie list
    movies = process_movies('~/Downloads/Movies')
    html = t.render(Context({'movies': movies,}))

    return HttpResponse(html)

def process_movies(dir):
    set_key('36fb5f623484f4b2680f492005762f31') #store this key somewhere
    set_locale()

    movies = list()
    explore(dir)

    for f in fileset:
        result = searchMovie(f.fulltitle)
        if len(result) == 0:
            print "Couldn't find results for: " + str(result)
        movie = result[0] if len(result) > 0 else None
        movies.append(movie)

    for m in movies:
        if not m:
            continue

        p = m.poster

        if p:
            d = DisplayMovie(m,  m.poster.geturl('w154'))
        else:
            d = DisplayMovie(m, '')

        if m.id in movieids:
            continue

        pos = bisect.bisect(movieids, m.id)
        movieids.insert(pos, m.id)

        moviesToDisplay.append(d)

    return sorted(moviesToDisplay, key=lambda x: x.movie.title)

class DisplayMovie:
    def __init__(self, movie, poster):
        self.movie = movie
        self.title = movie.title
        self.poster = poster
        self.year = (movie.releasedate.year if movie.releasedate else 0)
    def __str__(self):
        return repr(self.movie.title + ' (' + self.year + ')')
