import subprocess
import os, traceback, sys
from movie_view.settings import BEAMER_FLAG, PROJECT_ROOT
from movie_view.secret_settings import DEFAULT_MOVIE_DIR
from django.http import HttpResponse, Http404

DEFAULT_MOVIE_DIR = DEFAULT_MOVIE_DIR if os.path.exists(DEFAULT_MOVIE_DIR) else PROJECT_ROOT + '/demo'

def beam(request, moviefile):
	moviefile = moviefile.replace('~', ' ').replace(':', '_')

	beamer_cmdflag = ''
	if BEAMER_FLAG:
		beamer_cmdflag = '-a \'Beamer\''
	
	print DEFAULT_MOVIE_DIR

	if request.method == 'GET':
		for root, dirs, files in os.walk(DEFAULT_MOVIE_DIR):
			found = False
			for f in files:
				if moviefile in f:
					found = True
			print moviefile
			if found:
				print 'found'
				try:
					command = 'open ' + shellquote(DEFAULT_MOVIE_DIR + '/' + moviefile) + '.* ' + beamer_cmdflag

					print command
					# with open(DEFAULT_MOVIE_DIR + '/' + moviefile): pass
					os.system(command)

					return HttpResponse('opened!')
				except IOError:
					print 'IOError'
					traceback.print_exc(file=sys.stdout)
					raise Http404
			else:
				print 'not found'
				raise Http404
	else:
		print 'Not a GET'
		raise Http404

	raise Http404

def shellquote(s):
    return s.replace("'", "'\\''").replace(" ", "\\ ").replace("(", "\(").replace(")", "\)")