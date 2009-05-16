import os
from os.path import join, abspath,  dirname

VERSION = '0.2'

SHARED_DATA_DIR = abspath(join(dirname(__file__), '..'))
if not os.access(SHARED_DATA_DIR + '/gphotoframe.glade', os.R_OK):
    SHARED_DATA_DIR = '/usr/share/gphotoframe'

GLADE_FILE = SHARED_DATA_DIR + '/gphotoframe.glade'

CACHE_DIR = '/tmp/gphotoframe-' + os.environ['USER'] + '/'
if not os.access(CACHE_DIR, os.W_OK):
    os.makedirs(CACHE_DIR)
