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

# Please see the README.mkd for API and program specific details

__revision__ = "1.1"

import nmsg
import sys
import time

def main(fname, out):
    i = nmsg.input.open_file(fname)

    while True:
        m = i.read()
        if not m:
            break
        
        tm = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(m.time_sec))
        out.write('[%s.%d] ' % (tm, m.time_nsec))
        out.write('[%d:%d %s %s] ' % (m.vid, m.msgtype,
            nmsg.msgmod.vid_to_vname(m.vid), 
            nmsg.msgmod.msgtype_to_mname(m.vid, m.msgtype)))

        if m.has_source:
            out.write('[%.8x] ' % m.source)
        else:
            out.write('[] ')

        if m.has_operator:
            out.write('[%s] ' % m.operator)
        else:
            out.write('[] ')

        if m.has_group:
            out.write('[%s] ' % m.group)
        else:
            out.write('[] ')

        out.write('\n')

        for key in m.keys():
            val = m[key]
            if type(val) == list:
                for v in val:
                    out.write('%s: %s\n' % (key, repr(v)))
            else:
                out.write('%s: %s\n' % (key, repr(val)))

        out.write('\n')

if __name__ == '__main__':
    main(sys.argv[1], sys.stdout)
