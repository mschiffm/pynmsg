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

class NmsgClient(object):
    def __init__(self, addr, port):
        self.o = nmsg.output.open_sock(addr, int(port))
        self.o.set_buffered(False)
        self.m = nmsg.msgtype.isc.encode()

    def send(self, e_type, e_payload):
        t = time.time()
        self.m.time_sec = int(t)
        self.m.time_nsec = int((t - int(t)) * 1E9)

        self.m['type'] = e_type
        self.m['payload'] = e_payload
        self.o.write(self.m)

    def send_text(self, iterations):
        for i in range(0, iterations):
            hello = "hello world {0}".format(i)
            self.send("TEXT", hello)
        return "sent {0} TEXT-encoded payloads".format(iterations)

    def send_json(self, iterations):
        try:
            import json
            hello = { 'hello': 'world', 'foo': 'bar' }
            for i in range(0, iterations):
                hello['id'] = i
                self.send("JSON", json.dumps(hello))
            return "sent {0} JSON-encoded payloads".format(iterations)
        except ImportError:
            return "no JSON support"

    def send_yaml(self, iterations):
        try:
            import yaml
            hello = { 'hello': 'world', 'foo': 'baz' }
            for i in range(0, iterations):
                hello['id'] = i
                self.send("YAML", yaml.dump(hello))
            return "sent {0} YAML-encoded payloads".format(iterations)
        except ImportError:
            return "no YAML support"

    def send_msgpack(self, iterations):
        try:
            import msgpack
            hello = { 'hello': 'world', 'foo': 'q\x00\x00x' }
            for i in range(0, iterations):
                hello['id'] = i
                self.send("MSGPACK", msgpack.dumps(hello))
            return "sent {0} MSGPACK-encoded payloads".format(iterations)
        except ImportError:
            return "no MSGPACK support"

    def send_xml(self, iterations):
        for i in range(0, iterations):
            self.send("XML", '<xml/>')
        return "sent {0} dummy XML-encoded payloads".format(iterations)

ENCODERS = ["TEXT", "JSON", "YAML", "MSGPACK", "XML"]
ENCODERS_CHOICES = list(ENCODERS)
ENCODERS_CHOICES.append("ALL")

parser = argparse.ArgumentParser(description = "simple NMSG client")
parser.add_argument("addr_port", nargs="?", default = "127.0.0.1/9430",
                help = "address/port to listen for incoming NMSG datagrams")
parser.add_argument("-i", "--iterations", default = 3,
                help = "number of iterations to send")
parser.add_argument("-t", "--type", choices = ENCODERS_CHOICES,
                action = "store", default = "ALL",
                help = "NSMG datagram(s) to send, use 'ALL' to send all types")
args = parser.parse_args()

addr, port = args.addr_port.split("/")

client = NmsgClient(addr, port)

print "sending NMSG datagrams to {0}/{1}".format(addr, port)

if args.type == "ALL":
    for encoder in ENCODERS:
        sMeth = getattr(client, "send_" + encoder.lower())
        print sMeth(int(args.iterations))
else:
    sMeth = getattr(client, "send_" + args.type.lower())
    print sMeth(int(args.iterations))
