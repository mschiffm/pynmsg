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

class _msgtype(object):
    """
    An instance of this object will have members for each available
    vendor, each of which has members mapping to a class for each
    msgtype. e.g.::

        m = msgtype.base.encode()

    All available message modules are automatically loaded and
    recompilation of pynmsg is not necessary to include new modules.

    This object has a dictionary member called 'types' that contains a
    mapping of all vendors to messagetypes.  This might look like::

        {'base': [ 'dns', 'dnsqr', 'email', 'encode', 'http', 'ipconn',
                'linkpair', 'logline', 'ncap', 'packet', 'pkt', 'xml']}
    """
    def __init__(self):
        cdef char *vname_str
        cdef char *mname_str

        for vid from 1 <= vid <= nmsg_msgmod_get_max_vid():
            vname_str = nmsg_msgmod_vid_to_vname(vid)

            if vname_str:
                vname = str(vname_str).lower()
                v_dict = {}

                for msgtype from 1 <= msgtype <= nmsg_msgmod_get_max_msgtype(vid):
                    mname_str = nmsg_msgmod_msgtype_to_mname(vid, msgtype)

                    if mname_str:
                        mname = str(mname_str).lower()
                        mod = msgmod(vid, msgtype)
                        m_dict = {
                            '__vid':     vid,
                            '__msgtype': msgtype,
                        }
                        v_dict[mname] = type('%s_%s' % (vname, mname), (_meta_message,), m_dict)
                v_dict['_vname'] = vname
                v_dict['_vid'] = vid

                setattr(self, vname, type(vname, (object,), v_dict))
