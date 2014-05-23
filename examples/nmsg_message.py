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

import time
import nmsg
import argparse


parser = argparse.ArgumentParser(description = "simple NMSG ipconn client")
parser.add_argument("addr_port", nargs="?", default = "127.0.0.1/9430",
        help = "address/port to listen for incoming NMSG datagrams")
parser.add_argument("-n", "--number", default = 100,
        help = "number of NMSG datagrams to send")
args = parser.parse_args()

addr, port = args.addr_port.split("/")

o = nmsg.output.open_sock(addr, int(port))
o.set_buffered(False)

m = nmsg.msgtype.base.ipconn()

print "sending {0} ipconn NMSG datagrams to {1}/{2}...".format(args.number, addr, port)
for i in range(0, int(args.number)):
    t = time.time()
    m.time_sec = int(t)
    m.time_nsec = int((t - int(t)) * 1E9)
    m['srcip'] = "127.0.0.{0}".format(i)
    m['dstip'] = "127.1.0.{0}".format(i)
    m['srcport'] = i
    m['dstport'] = 65535 - i
    m['proto'] = 6  #TCP
    o.write(m)
