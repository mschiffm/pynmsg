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
import select
import argparse

def main(ip, port, timeout):
    ni = nmsg.input.open_sock(ip, port)
    fd = ni.fileno()

    ni.set_blocking_io(False)

    p = select.poll()
    p.register(fd, select.POLLIN)

    while True:
        events = p.poll(timeout)
        if events:
            m = ni.read()
            while m:
                nmsg.print_nmsg_header(m, sys.stdout)
                m = ni.read()
        else:
            print 'Nope, no NMSG...'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Synchronous IO polling example")
    parser.add_argument("addr_port", nargs="?", default = "127.0.0.1/9430",
            help = "address/port to listen for incoming NMSG datagrams")
    parser.add_argument("-t", "--timeout", type = int, default = 1000,
            help = "millisecond timeout")
    args = parser.parse_args()
    address, port = args.addr_port.split("/")
    main(address, int(port), args.timeout)
