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

count = 0

def cb(msg):
    global count
    count += 1
    if (count % 10000) == 0:
        sys.stderr.write(".")

def main(fname):
    io = nmsg.io()
    input = nmsg.input.open_file(fname)
    io.add_input(input)
    #io.add_output_callback(cb)
    #io.add_output_callback(cb)
    io.add_output_callback(cb)
    io.loop()

    print '\ncount: {0}'.format(count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "open an NMSG file and execute a callback function on each message")
    parser.add_argument("infile", action = "store",
                help = "file containing NMSG datagrams")
    args = parser.parse_args()
    main(args.infile)

