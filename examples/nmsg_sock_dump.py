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
import argparse

def main(addr, port):
    i = nmsg.input.open_sock(addr, port)
    print "listening for NMSG datagrams on {0}/{1}...".format(addr, port)

    while True:
        m = i.read()
        if not m:
            break

        nmsg.print_nmsg_header(m, sys.stdout)

        for key in m.keys():
            val = m[key]
            if type(val) == list:
                for v in val:
                    print "{0}: {1}".format(key, repr(v))
            else:
                print "{0}: {1}".format(key, repr(val))
        print ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "listen for NMSG datagrams and dump them to the screen")
    parser.add_argument("addr_port", nargs="?", default = "127.0.0.1/9430",
            help = "address/port to listen for incoming NMSG datagrams")
    args = parser.parse_args()
    address, port = args.addr_port.split("/")
    main(address, int(port))
