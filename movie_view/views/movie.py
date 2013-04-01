from tmdb3 import set_key, set_locale, searchMovie, Movie
from django.http import HttpResponse, Http404
from movie_view.secret_settings import API_KEY, DEFAULT_MOVIE_DIR, DEFAULT_DATA_FILE
from django import template
from django.template import Context
from django.template.loader import get_template
import string
import bisect
import operator
from os.path import expanduser as expand

try:
    import cPickle as pickle
except:
    import pickle

from filesystem import explore, fileset, MovieFile

movieids = list()
moviesToDisplay = list()
notfound = list()

datafile = DEFAULT_DATA_FILE

def showall(request):
    t = get_template('home.html')

    # get movie list
    movies = process_movies(DEFAULT_MOVIE_DIR)
    html = t.render(Context({'movies': movies,'notfound': notfound,}))

    return HttpResponse(html)

def process_movies(dir):
    set_key(API_KEY) #store this key somewhere
    set_locale()

    dir = expand(dir)

    movies = list()
    moviesToDisplay = loadfromfile(dir)

    if not moviesToDisplay:
        moviesToDisplay = list()

    titles = list()

    for m in moviesToDisplay:
        titles.append(m.title)

    explore(dir)

    for f in fileset:
        if f.fulltitle in titles:
            continue

        result = searchMovie(f.fulltitle)

        if len(result) == 0:
            if f.filename not in notfound:
                notfound.append(f.filename)
            print "Couldn't find results for: " + f.fulltitle + " result = " + str(result)
            continue

        # print "**** Found results for: " + f.fulltitle + " result = " + str(result[0])

        movie = result[0] if len(result) > 0 else None
        movies.append(movie)

    for m in movies:
        if not m:
            continue

        if m.id in movieids:
            continue

        p = m.poster

        if p:
            d = DisplayMovie(m,  p.geturl('w154'),)
        else:
            d = DisplayMovie(m, '',)

        if m.id in movieids:
            continue

        pos = bisect.bisect(movieids, m.id)
        movieids.insert(pos, m.id)

        moviesToDisplay.append(d)

    writetofile(dir, moviesToDisplay)
    return sorted(moviesToDisplay, key=lambda x: x.movie.title)

def loadfromfile(dir):
    f = None
    try:
        f = open(dir + datafile, 'r')
        mtds = pickle.load(f)

        for mtd in mtds:
            pos = bisect.bisect(movieids, mtd.movie.id)
            movieids.insert(pos, mtd.movie.id)

        f.close()

        return mtds
    except:
        try:
            file = open(dir + datafile, 'w')
            file.write('')
            file.close()
            return None
        except:
            raise Http404

def writetofile(dir, mtd):
    try:
        f = open(dir + datafile, 'w')
        pickle.dump(mtd, f, -1)
        f.close()
    except:
        raise Http404

class DisplayMovie:
    def __init__(self, movie, poster):
        self.movie = movie
        self.title = movie.title
        self.poster = poster
        # self.apple_trailer = movie.apple_trailer.geturl()
        # self.youtube_trailer = movie.youtube_trailer.geturl()
        self.year = (movie.releasedate.year if movie.releasedate else 0)
    def __str__(self):
        return repr(self.movie.title + ' (' + str(self.year) + ')')
