#!/usr/bin/env python

# Copyright (c) 2009-2014 by Farsight Security, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

NAME = 'pynmsg'
VERSION = '0.2'

from distutils.core import setup
from distutils.extension import Extension
import os

try:
    from Cython.Distutils import build_ext
    setup(
        name = NAME,
        version = VERSION,
        ext_modules = [ Extension('_nmsg', ['_nmsg.pyx'], libraries = ['nmsg']) ],
        cmdclass = {'build_ext': build_ext},
        py_modules = ['nmsg'],
    )
except ImportError:
    if os.path.isfile('_nmsg.c'):
        setup(
            name = NAME,
            version = VERSION,
            ext_modules = [ Extension('_nmsg', ['_nmsg.c'], libraries = ['nmsg']) ],
            py_modules = ['nmsg'],
        )
    else:
        raise
