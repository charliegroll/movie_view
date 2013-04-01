import subprocess
import os
from movie_view.secret_settings import DEFAULT_MOVIE_DIR
from django.http import HttpResponse, Http404

DEFAULT_MOVIE_DIR = DEFAULT_MOVIE_DIR if exists(DEFAULT_MOVIE_DIR) else PROJECT_ROOT + 'demo'

def beam(request, moviefile):
	moviefile = moviefile.replace('~', ' ')
	
	if request.method == 'GET':
		for root, dirs, files in os.walk(DEFAULT_MOVIE_DIR):
			print moviefile
			print files
			if moviefile in files:
				print 'found'
				try:
					command = 'open -a \'Beamer\' ' + '\'' + DEFAULT_MOVIE_DIR + '/' + moviefile + '\''

					print command
					with open(DEFAULT_MOVIE_DIR + '/' + moviefile): pass
					os.system(command)

					return HttpResponse('opened!')
				except IOError:
					print 'IOError'
					raise Http404
			else:
				raise Http404
	else:
		raise Http404

	raise Http404