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

"""
Python extension module for the nmsg C library.

A Python extension module implemented in Cython for the nmsg C
library.

Read some messages::

    import nmsg

    in = nmsg.input.open_file('input.nmsg')
    while True:
        m = in.read()
        if not m:
            break
        # do something with m

Write a base.encode message::

    import json
    import time

    import nmsg

    m = nmsg.msgtype.base.encode()
    t = time.time()
    m.time_sec = int(t)
    m.time_nsec = int((t - int(t)) * 1E9)
    m.has_source = True
    m.source = 0x1a1a1a1a # replace with your source id

    m['type'] = 'JSON'
    m['payload'] = json.dumps({ 'foo' : 'bar' })

    out = nmsg.output.open_file('output.nmsg')
    out.write(m)

Print all available message types::

    for vname in nmsg.msgtype.types:
        for mname in nmsg.msgtype.types[vname]:
            print '.'.join((vname, mname))
"""

import ctypes
import sys

flags = sys.getdlopenflags()
sys.setdlopenflags(flags | ctypes.RTLD_GLOBAL)

from _nmsg import *

sys.setdlopenflags(flags)
