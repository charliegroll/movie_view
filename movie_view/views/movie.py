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
    tmdb.configure('36fb5f623484f4b2680f492005762f31') #store this key somewhere
    # something's going wrong here
    movie = tmdb.Movie(name)
    try:
        if None == movie:
            return None

        movie.get_id()
        movie.full_info(movie_id)

        return movie_id
    except:
        return None


