"""
opaque_field.py

Copyright 2014 ETH Zurich

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
from bitstring import BitArray
import bitstring

class OpaqueFieldType(object):
    """
    Defines constants for the types of the opaque field (first byte of every
    opaque field, i.e. field).
    """
    NORMAL_OF = 0x00
    SPECIAL_OF = 0x80
    TDC_XOVR = 0x80
    NON_TDC_XOVR = 0xc0
    INPATH_XOVR = 0xe0
    INTRATD_PEER = 0xf0
    INTERTD_PEER = 0xf8
    PEER_XOVR = 0x10
    ROT_OF = 0xff

class OpaqueField(object):
    """
    Base class for the different kinds of opaque fields in SCION.
    """

    LEN = 8

    def __init__(self):
        self.info = 0 #TODO verify path.PathType in that context
        self.parsed = False
        self.raw = None

    def parse(self, raw):
        """
        Populates fields from a raw byte block.
        """
        pass

    def pack(self):
        """
        Returns opaque field as 8 byte binary string.
        """
        pass

    def __eq__(self, other):
        if type(other) is type(self):
            return self.type == other.type
        else:
            return False

    def __ne__(self, other):
        return not self == other

    def is_regular(self):
        """
        Returns true if opaque field is regular, false otherwise.
        """
        return not BitArray(bytes([self.info]))[0]

    def is_continue(self):
        """
        Returns true if continue bit is set, false otherwise.
        """
        return BitArray(bytes([self.info]))[1]

    def is_xovr(self):
        """
        Returns true if crossover point bit is set, false otherwise.
        """
        return BitArray(bytes([self.info]))[2]

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()


class HopOpaqueField(OpaqueField):
    """
    Opaque field for a hop in a path of the SCION packet header.

    Each hop opaque field has a type (8 bits), ingress/egress interfaces
    (16 bits) and a MAC (24 bits) authenticating the opaque field.
    """

    def __init__(self, raw=None):
        OpaqueField.__init__(self)
        self.ingress_if = 0
        self.egress_if = 0
        self.mac = 0
        if raw is not None:
            self.parse(raw)

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)
        if dlen < HopOpaqueField.LEN:
            logging.warning("Data too short to parse hop opaque field: "
                "data len %u", dlen)
            return
        bits = BitArray(bytes=raw)
        (self.info, self.ingress_if, self.egress_if, self.mac) = \
            bits.unpack("uintle:8, uintle:16, uintle:16, uintle:24")

        self.parsed = True

    def pack(self):
        return bitstring.pack("uintle:8, uintle:16, uintle:16, uintle:24",
                              self.info, self.ingress_if, self.egress_if,
                              self.mac).bytes

    def __eq__(self, other):
        if type(other) is type(self):
            return (self.type == other.type and
                    self.ingress_if == other.ingress_if and
                    self.egress_if == other.egress_if and
                    self.mac == other.mac)
        else:
            return False

    def __str__(self):
        s = "[Hop OF type: %u, ingress if: %u, egress if: %u, mac: %x]" % (
            self.info, self.ingress_if, self.egress_if, self.mac)
        return s


class InfoOpaqueField(OpaqueField):
    """
    Class for the info opaque field.

    The info opaque field contains type info of the path (1 byte), an expiration
    timestamp (2 bytes), the ISD ID (2 byte), # hops for this path (1 byte) and
    a reserved section (2 bytes).
    """

    def __init__(self, raw=None):
        OpaqueField.__init__(self)
        self.timestamp = 0
        self.isd_id = 0
        self.hops = 0
        self.reserved = 0
        self.raw = raw

        if raw is not None:
            self.parse(raw)

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)
        if dlen < InfoOpaqueField.LEN:
            logging.warning("Data too short to parse info opaque field: "
                "data len %u", dlen)
            return
        bits = BitArray(bytes=raw)
        (self.info, self.timestamp, self.isd_id, self.hops, self.reserved) = \
            bits.unpack("uintle:8, uintle:16, uintle:16, uintle:8, uintle:16")

        self.parsed = True

    def pack(self):
        #PSz: Should InfoOpaqueFIeld with raw==None pack to b'\x00'*8 ?
        if not self.raw:
            return b''
        return bitstring.pack("uintle:8, uintle:16, uintle:16, uintle:8,"
                              "uintle:16", self.info, self.timestamp,
                              self.isd_id, self.hops, self.reserved).bytes

    def __eq__(self, other):
        if type(other) is type(self):
            return (self.type == other.type and
                    self.info == other.info and
                    self.timestamp == other.timestamp and
                    self.isd_id == other.isd_id and
                    self.hops == other.hops and
                    self.reserved == other.reserved)
        else:
            return False

    def __str__(self):
        s = "[Info OF info: %x, TS: %u, ISD ID: %u, hops: %u]" % (
            self.info, self.timestamp, self.isd_id, self.hops)
        return s


### Lorenzo ###
class HopField(OpaqueField):
    """
    Opaque field for a hop in a path of the SCION packet header.

    Each hop opaque field has a info (8 bits), ingress/egress interfaces
    (16 bits) and a MAC (24 bits) authenticating the opaque field.
    """
    def __init__(self, raw=None):
        OpaqueField.__init__(self)
        self.ingress_if = 0
        self.egress_if = 0
        self.mac = 0
        if raw is not None:
            self.parse(raw)

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)
        if dlen < self.LEN:
            logging.warning("Data too short to parse the field, len: %u", dlen)
            return
        bits = BitArray(bytes=raw)
        (self.info, self.ingress_if, self.egress_if, self.mac) = \
            bits.unpack("uintle:8, uintle:16, uintle:16, uintle:24")
        self.parsed = True
        
    @classmethod
    def from_values(cls, ingress_if, egress_if, mac):
        hof = HopField()
        hof.ingress_if = ingress_if
        hof.egress_if = egress_if
        hof.mac = mac
        return hof

    def pack(self):
        return bitstring.pack("uintle:8, uintle:16, uintle:16, uintle:24",
               self.info, self.ingress_if, self.egress_if, self.mac).bytes

    def __str__(self):
        s = "[Hop OF info: %u, ingress if: %u, egress if: %u, mac: %x]\n" % (
            self.info, self.ingress_if, self.egress_if, self.mac)
        return s


class SpecialField(OpaqueField):
    """
    Class for the special opaque field.

    The info opaque field contains info info of the path (1 byte), an expiration
    timestamp (2 bytes), the ISD ID (2 byte), # hops for this path (2 byte) and
    a reserved section (2 bytes).
    """
    def __init__(self, raw=None):
        OpaqueField.__init__(self)
        self.info = OpaqueFieldType.SPECIAL_OF
        self.timestamp = 0
        self.isd_id = 0
        self.hops = 0
        self.reserved = 0
        if raw is not None:
            self.parse(raw)

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)
        if dlen < self.LEN:
            logging.warning("Data too short to parse the field, len: %u", dlen)
            return
        bits = BitArray(bytes=raw)
        (self.info, self.timestamp, self.isd_id, self.hops, self.reserved) = \
            bits.unpack("uintle:8, uintle:16, uintle:16, uintle:8, uintle:16")
        self.parsed = True
    
    @classmethod    
    def from_values(cls, timestamp, isd_id, hops, reserved):
        sof = SpecialField()
        sof.timestamp = timestamp
        sof.isd_id = isd_id
        sof.hops = hops
        sof.reserved = reserved
        return sof

    def pack(self):
        return bitstring.pack("uintle:8, uintle:16, uintle:16, uintle:8,"
               "uintle:16", self.info, self.timestamp, self.isd_id, self.hops,
               self.reserved).bytes

    def __str__(self):
        s = "[Special OF info: %x, TS: %u, ISD ID: %u, hops: %u]\n" % (
            self.info, self.timestamp, self.isd_id, self.hops)
        return s
        
        
class ROTField(OpaqueField):
    """
    Class for the ROT field.

    The ROT field contains type info of the path (1 byte), the ROT version
    (4 bytes), the IF ID (2 bytes), and a reserved section (1 byte).
    """
    def __init__(self, raw=None):
        OpaqueField.__init__(self)
        self.info = OpaqueFieldType.ROT_OF
        self.rot_version = 0
        self.if_id = 0
        self.reserved = 0
        if raw is not None:
            self.parse(raw)

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)
        if dlen < self.LEN:
            logging.warning("Data too short to parse the field, len: %u", dlen)
            return
        bits = BitArray(bytes=raw)
        (self.info, self.rot_version, self.if_id, self.reserved) = \
            bits.unpack("uintle:8, uintle:32, uintle:16, uintle:8")
        self.parsed = True
    
    @classmethod    
    def from_values(cls, ROTversion, if_id, reserved):
        rotf = ROTField()
        rotf.rot_version = rot_version
        rotf.if_id = if_id
        rotf.reserved = reserved
        return rotf

    def pack(self):
        return bitstring.pack("uintle:8, uintle:32, uintle:16, uintle:8",
               self.info, self.rot_version, self.if_id, self.reserved).bytes

    def __str__(self):
        s = "[ROT OF info: %x, ROTv: %u, IF ID: %u]\n" % (
            self.info, self.rot_version, self.if_id)
        return s


class SupportSignatureField(OpaqueField):
    """
    Class for the support signature field.

    The support signature field contains a certificate ID (4 bytes), the
    signature length (2 bytes), and the block size (2 bytes).
    """
    def __init__(self, raw=None):
        OpaqueField.__init__(self)
        self.cert_id = 0
        self.sig_len = 0
        self.block_size = 0
        if raw is not None:
            self.parse(raw)

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)
        if dlen < self.LEN:
            logging.warning("Data too short to parse the field, len: %u", dlen)
            return
        bits = BitArray(bytes=raw)
        (self.cert_id, self.sig_len, self.block_size) = \
            bits.unpack("uintle:32, uintle:16, uintle:16")
        self.parsed = True
    
    @classmethod    
    def from_values(cls, cert_id, sig_len, block_size):
        ssf = SupportSignatureField()
        ssf.cert_id = cert_id
        ssf.sig_len = sig_len
        ssf.block_size = block_size
        return ssf

    def pack(self):
        return bitstring.pack("uintle:32, uintle:16, uintle:16",
               self.cert_id, self.sig_len, self.block_size).bytes

    def __str__(self):
        s = "[Support Signature OF cert_id: %x, sig_len: %u, block_size: %u]\n" % (
            self.cert_id, self.sig_len, self.block_size)
        return s
        
        
class SupportPeerField(OpaqueField):
    """
    Class for the support peer field.

    The support peer field contains the trusted domain id (2 bytes),
    bandwidth allocation f (1 byte), bandwith allocation r (1 byte),
    the bandwidth class (1 bit), and a reserved section (31 bits).
    """
    def __init__(self, raw=None):
        OpaqueField.__init__(self)
        self.td_id = 0
        self.bwalloc_f = 0
        self.bwalloc_r = 0
        self.bw_class = 0
        self.reserved = 0
        if raw is not None:
            self.parse(raw)

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)
        if dlen < self.LEN:
            logging.warning("Data too short to parse the field, len: %u", dlen)
            return
        bits = BitArray(bytes=raw)
        (self.td_id, self.bwalloc_f, self.bwalloc_r, self.bw_class, _reserved) = \
            bits.unpack("uintle:16, uintle:8, uintle:8, uint:1, uint:31")
        self.parsed = True
    
    @classmethod    
    def from_values(cls, td_id, bwalloc_f, bwalloc_r, bw_class, reserved):
        spf = SupportPeerField()
        spf.td_id = td_id
        spf.bwalloc_f = bwalloc_f
        spf.bwalloc_r = bwalloc_r
        spf.bw_class = bw_class
        spf.reserved = reserved
        return spf

    def pack(self):
        return bitstring.pack("uintle:16, uintle:8, uintle:8, uint:1,"
               "uint:31", self.td_id, self.bwalloc_f, self.bwalloc_r,
               self.bw_class, self.reserved).bytes

    def __str__(self):
        s = "[Support Peer OF TD ID: %x, bwalloc_f: %u, bwalloc_r: %u, bw_class: %u]\n" % (
            self.td_id, self.bwalloc_f, self.bwalloc_r, self.bw_class)
        return s
        
        
class SupportPCBField(OpaqueField):
    """
    Class for the support PCB field.

    The support PCB field contains the trusted domain id (2 bytes),
    bandwidth allocation f (1 byte), bandwith allocation r (1 byte),
    dynamic bandwidth allocation f (1 byte), dynamic bandwidth allocation r
    (1 byte), BE bandwidth f (1 byte), and BE bandwidth r (1 byte).
    """
    def __init__(self, raw=None):
        OpaqueField.__init__(self)
        self.td_id = 0
        self.bwalloc_f = 0
        self.bwalloc_r = 0
        self.dyn_bwalloc_f = 0
        self.dyn_bwalloc_r = 0
        self.bebw_f = 0
        self.bebw_r = 0
        if raw is not None:
            self.parse(raw)

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)
        if dlen < self.LEN:
            logging.warning("Data too short to parse the field, len: %u", dlen)
            return
        bits = BitArray(bytes=raw)
        (self.td_id, self.bwalloc_f, self.bwalloc_r, self.dyn_bwalloc_f,
         self.dyn_bwalloc_r, self.bebw_f, self.bebw_r) = \
            bits.unpack("uintle:16, uintle:8, uintle:8, uintle:8, uintle:8,"
                        "uintle:8, uintle:8")
        self.parsed = True
    
    @classmethod    
    def from_values(cls, td_id, bwalloc_f, bwalloc_r, dyn_bwalloc_f,
                    dyn_bwalloc_r, bebw_f, bebw_r):
        spcbf = SupportPCBField()
        spcbf.td_id = td_id
        spcbf.bwalloc_f = bwalloc_f
        spcbf.bwalloc_r = bwalloc_r
        spcbf.dyn_bwalloc_f = dyn_bwalloc_f
        spcbf.dyn_bwalloc_r = dyn_bwalloc_r
        spcbf.bebw_f = bebw_f
        spcbf.bebw_r = bebw_r
        return spcbf

    def pack(self):
        return bitstring.pack("uintle:16, uintle:8, uintle:8, uintle:8,"
               "uintle:8, uintle:8, uintle:8", self.td_id, self.bwalloc_f,
               self.bwalloc_r, self.dyn_bwalloc_f, self.dyn_bwalloc_r,
               self.bebw_f, self.bebw_r).bytes

    def __str__(self):
        s = "[Info OF TD ID: %x, bwalloc_f: %u, bwalloc_r: %u]\n" % (
            self.td_id, self.bwalloc_f, self.bwalloc_r)
        return s
