import os
import string

dirlist = list()
fileset = set()
exts = ['.avi', '.mkv', '.m4v', '.mp4'] # todo: make this a set()

# returns a list of MovieFiles
def explore(dir):
    dir = os.path.expanduser(dir)

    try:
        os.chdir(dir)
    except:
        raise FileNameException('Invalid dir ' + dir)

    if dir not in dirlist:
        dirlist.append(dir)

    for root, dirs, files in os.walk(dir):
        # we ignore all hidden files and dirs
        dirs = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # we only want video files
        # TODO: keep list of invalid files (if the year isn't a number, maybe at least 1900)
        for f in list(files):
            ext = f[f.rfind("."):]

            if ext not in exts:
                files.remove(f)

            froot = f[:f.rfind(".")]
            y = froot[froot.rfind("(")+1:froot.rfind(")")] # have to check if there's no year
            t = froot[:froot.rfind("(")].strip().replace("_", ":") # some filesystems replace ':' with '_'
            f = f.replace("_", ":")
            d = root

            m = MovieFile(title=t, year=y, dir=d, filename=f)
            fileset.add(m)

        #print root,
        #print dirs,
        #print files

# add your own file extensions to search
# valid formats include strings with one leading- or no '.'
def add_extension(ext):
    if string.rfind(ext, '.') > 0:
        raise FileNameException(ext)

    if ext not in exts and '.' + ext not in exts:
        exts.append('.' + ext if not ext.startswith('.') else ext)
        return True
    else:
        return False

# when trying to add an extension with add_extension,
# they may submit an invalid format
class FileNameException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# store all of the metadata about the files
class MovieFile():
    def __init__(self, title, dir, filename, year=0):
        self.title = title
        self.year = year
        self.fulltitle = title if year == 0 else title + ' (' + year + ')'
        self.dir = dir
        self.filename = filename
    def __str__(self):
        return repr(self.title + ' (' + self.year + ') at ' + self.dir)
