#!/usr/bin/python

from distutils.core import setup
from DistUtilsExtra.command import *

setup(name='gphotoframe',
      version='0.1.1',
      description='Gnome Photo Frame',
      author='Yoshizumi Endo',
      author_email='y-endo@ceres.dti.ne.jp',
      url='http://code.google.com/p/gphotoframe/',
      package_dir = {'gphotoframe' : 'lib'},
      packages=['gphotoframe', 'gphotoframe.plugins'],
      scripts=['gphotoframe'],
      data_files=[('share/gphotoframe', ['gphotoframe.glade'])],
      cmdclass = { "build" : build_extra.build_extra,
                   "build_i18n" : build_i18n.build_i18n,
                   "build_help" : build_help.build_help,
                   "build_icons" : build_icons.build_icons }
      )
