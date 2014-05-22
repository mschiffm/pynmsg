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

import sys
import nmsg
import time
import argparse

def main(fname):
    i = nmsg.input.open_file(fname)

    while True:
        m = i.read()
        if not m:
            break
        
        tm = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(m.time_sec))
        print "[{0}.{1}]".format(tm, m.time_nsec),
        print "[{0}:{1} {2} {3}]".format(m.vid, m.msgtype,
            nmsg.msgmod.vid_to_vname(m.vid), 
            nmsg.msgmod.msgtype_to_mname(m.vid, m.msgtype)),

        if m.has_source:
            print "[{0:008x}]".format(m.source),
        else:
            print "[]",

        if m.has_operator:
            print "[{0}]".format(m.operator),
        else:
            print "[]",

        if m.has_group:
            print "[{0}]".format(m.group),
        else:
            print "[]",

        print ""

        for key in m.keys():
            val = m[key]
            if type(val) == list:
                for v in val:
                    print "{0}: {1}".format(key, repr(v))
            else:
                print "{0}: {1}".format(key, repr(val))

        print ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "dump the contents of an NMSG file")
    parser.add_argument("infile", action = "store",
                help = "file containing NMSG datagrams")
    args = parser.parse_args()
    main(args.infile)
