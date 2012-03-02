#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
    setup(
        name = 'nmsg',
        ext_modules = [ Extension('_nmsg', ['_nmsg.pyx'], libraries = ['nmsg']) ],
        cmdclass = {'build_ext': build_ext},
        py_modules = ['nmsg'],
    )
except ImportError:
    setup(
        name = 'nmsg',
        ext_modules = [ Extension('_nmsg', ['_nmsg.c'], libraries = ['nmsg']) ],
        py_modules = ['nmsg'],
    )
