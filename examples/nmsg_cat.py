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
import argparse

parser = argparse.ArgumentParser(description = "redirect NMSG datagrams")
parser.add_argument("-i", "--input", default = "127.0.0.1/8430",
        help = "address/port to receive incoming NMSG datagrams")
parser.add_argument("-o", "--output", default = "127.0.0.1/9430",
        help = "address/port to fire outgoing NMSG datagrams")
args = parser.parse_args()

iaddr, iport = args.input.split("/")
oaddr, oport = args.output.split("/")

n = nmsg.input.open_sock(iaddr, int(iport)) 
o = nmsg.output.open_sock(oaddr, int(oport))

print "redirecting NMSGS: {0}/{1}-->{2}/{3}".format(iaddr, iport, oaddr, oport)
c = 0
while True:
    c += 1
    if (c % 1000) == 0:
        sys.stderr.write('.')
    if (c % 10000) == 0:
        sys.stderr.write('%s' % c)

    m = n.read()
    o.write(m)
