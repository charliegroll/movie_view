from tmdb3 import set_key, set_locale, searchMovie, Movie
from django.http import HttpResponse, Http404
from django import template
from django.template import Context
from django.template.loader import get_template
import string
import bisect
from filesystem import explore, fileset, MovieFile

moviesToDisplay = list()
movieids = list()

class DisplayMovie:
    def __init__(self, movie, poster, urlname):
        self.movie = movie
        self.poster = poster
        self.year = (movie.releasedate.year if movie.releasedate else 0)
        self.urlname = urlname

def show(request, name):
    name = parse_movie(name)

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
    movies = process_movies('~/Downloads/Movies')
    html = t.render(Context({'movies': moviesToDisplay,}))

    return HttpResponse(html)

def parse_movie(name):
    name = name.split('-')
    if name == '':
        return None
    else:
        return " ".join(name).title()

def unparse_movie(movie):
    if not movie.title:
        return ''

    result = ''
    last = False
    for x in movie.title:
        if x.isalnum():
            result += x
            last = False
        elif not last:
            result += '-'
            last = True

    if movie.releasedate:
        result += '-' + str(movie.releasedate.year)
    return result.rstrip('-')

def process_movies(dir):
    set_key('36fb5f623484f4b2680f492005762f31') #store this key somewhere
    set_locale()

    movies = list()
    explore(dir)

    for f in fileset:
        print f.fulltitle
        result = searchMovie(f.fulltitle)
        if len(result) == 0:
            print result
        movie = result[0] if len(result) > 0 else None
        movies.insert(0,movie)

    for m in movies:
        if not m or m.id in movieids:
            continue

        p = m.poster

        if p:
            d = DisplayMovie(m,  m.poster.geturl('w154'), unparse_movie(m))
        else:
            d = DisplayMovie(m, '', unparse_movie(m))

        pos = bisect.bisect(movieids, m.id)
        movieids.insert(pos, m.id)
        moviesToDisplay.append(d)
