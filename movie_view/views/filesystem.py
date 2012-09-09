import os
import string

dirlist = list()
filelist = {}
exts = ['.avi', '.mkv', '.m4v', '.mp4']

# returns a list of MovieFiles
def explore(dir):
    if dir not in dirlist:
        dirlist.append(os.path.abspath(dir))

    for root, dirs, files in os.walk(dir):
        # we ignore all hidden files and dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        # we only want video files
        for ext in exts:
            files[:] = [f for f in files if not f.endswith(ext)]

        for f in files:
            y = f[f.rfind("(")+1:f.rfind(")")] # have to check if there's no year
            t = f[0:f.rfind("(")]
            d = root
            m = MovieFile(title=t, year=y, dir=d, filename=f)
            filelist.setdefault(str(m), []).append(m)

        print root,
        print dirs,
        print files

# when trying to add an extension with add_extension,
# they may submit an invalid format
class ExtensionException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# add your own file extensions to search
# valid formats include strings with one leading- or no '.'
def add_extension(ext):
    if string.rfind(ext, '.') > 0:
        raise ExtensionException(ext)

    if ext not in exts and '.' + ext not in exts:
        exts.append('.' + ext if not ext.startswith('.') else ext)
        return True
    else:
        return False

# store all of the metadata about the files
class MovieFile():
    def __init__(self, title, dir, filename, year=0):
        self.title = title
        self.year = year
        self.fulltitle = title if year == 0 else title + ' (' + year + ')'
        self.dir = dir
        self.filename = filename
    def __str__(self):
        return repr(self.title + ' (' + self.year + ')')
