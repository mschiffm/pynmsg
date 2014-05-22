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
import pprint

class UnsupportedEncodeType(Exception):
    pass

class Encode(object):
    __slots__ = ('encode', 'decode')
    def __init__(self, encode, decode):
        self.encode = encode
        self.decode = decode

class EncodeDummy(object):
    @staticmethod
    def encode(*args, **kwargs):
        raise UnsupportedEncodeType
    @staticmethod
    def decode(*args, **kwargs):
        raise UnsupportedEncodeType

try:
    import json
    #encode_json = Encode(json.dumps(sort_keys=True, indent=4), json.loads)
    encode_json = Encode(json.dumps, json.loads)
except ImportError:
    encode_json = EncodeDummy

try:
    import yaml
    encode_yaml = Encode(yaml.dump, yaml.load)
except ImportError:
    encode_yaml = EncodeDummy

try:
    import msgpack
    encode_msgpack = Encode(msgpack.dumps, msgpack.loads)
except ImportError:
    encode_msgpack = EncodeDummy

table_encode = {
    'TEXT':     Encode(str, str),
    'JSON':     encode_json,
    'YAML':     encode_yaml,
    'MSGPACK':  encode_msgpack,
    'XML':      EncodeDummy
}

# Python stores JSON objects as unicode, since we're printing them to the 
# we should convert them to 8-bit strings. We do so using the simple
# Pilfered from Stack Exchange: http://bit.ly/RUYj79
def make_utf8(input):
    if isinstance(input, dict):
        return {make_utf8(key): make_utf8(value) for key, value in 
                input.iteritems()}
    elif isinstance(input, list):
        return [make_utf8(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode("utf-8")
    else:
        return input

def process(m, prettyprint):
    nmsg.msgmod_vname_to_vid('base')
    vid = nmsg.msgmod_vname_to_vid('base')
    msgtype = nmsg.msgmod_mname_to_msgtype(vid, 'encode')
    if not (m.vid == vid and m.msgtype == msgtype):
        return
    nmsg.print_nmsg_header(m, sys.stdout)
    print "type: {0}".format(m["type"])
    if m["type"] in table_encode:
        try:
            #print "payload: {0}".format(make_utf8(table_encode[m['type']].decode(m['payload'])))
            #print "payload: {0}".format(json.dumps(table_encode[m['type']].decode(m['payload']), sort_keys=True, indent=4))
            print "payload: {0}".format(table_encode[m['type']].encode((table_encode[m['type']].decode(m['payload']))))
        except UnsupportedEncodeType:
            sys.stdout.write('payload: <UNABLE TO DECODE>')
    else:
        sys.stdout.write('payload: <UNKNOWN ENCODING>')
    sys.stdout.write('\n')

def main(addr, port, prettyprint):
    i = nmsg.input.open_sock(addr, port)
    print "listening on {0}/{1}".format(addr, port)
    while True:
        m = i.read()
        if m:
            process(m, prettyprint)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "simple NMSG encode server")
    parser.add_argument("addr_port", nargs="?", default = "127.0.0.1/9430",
            help = "address/port to listen for incoming NMSG datagrams")
    parser.add_argument("-p", "--prettyprint", dest = "prettyprint", 
            action = "store_true", default = False, 
            help = "pretty print output (JSON only)")

    args = parser.parse_args()
    address, port = args.addr_port.split("/")
    main(address, int(port), args.prettyprint)
