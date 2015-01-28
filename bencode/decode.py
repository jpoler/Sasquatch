import os

import hashlib

import bittorrent.conf as conf
from collections import OrderedDict

class Decoder(object):

    def __init__(self, byte_string, wanted_substring=None):
        self.bs = byte_string
        self.mv = memoryview(byte_string)
        self.substrings = {}
        # This is ugly but necessary, otherwise nasty surprised happen with
        # always being given the same list reference, in the default keyword
        self.wanted_substring = wanted_substring

    def parse_string(self, offset, length):
        return (self.bs[offset:offset+length], offset+length)

    def parse_integer(self, offset, *args):
        e = self.bs.find(b'e', offset)
        return (int(self.bs[offset:e]), e+1)

    def parse_list(self, offset, *args):
        lst = []
        next_offset = offset
        while self.bs[next_offset] != ord(b'e'):
            func, after_header, arg = self.type_header(offset)
            obj, next_offset = func(next_offset, arg)
            lst.append(obj)
        return (lst, next_offset+1)

    def parse_dict(self, offset, *args):
        dct = OrderedDict()
        after_value = offset
        while self.bs[after_value] != ord(b'e'):
            print(self.bs[after_value])
            f, after_key_header, arg = self.type_header(after_value)
            key, after_key = f(after_key_header, arg)
            
            g, after_value_header, arg2 = self.type_header(after_key)
            value, after_value = g(after_value_header, arg2)
            print(key)
            print(self.wanted_substring)
            if key == self.wanted_substring:

                print(type(key),type(after_key), type(after_value))
                self.substrings[key] = self.bs[after_key:after_value]
            dct[key] = value
        return (dct, after_value+1)
        
    
    def type_header(self, offset):
        if self.bs[offset] == ord(b'i'):
            return (self.parse_integer, offset+1, None)
        elif self.bs[offset] == ord(b'd'):
            return (self.parse_dict, offset+1, None)
        colon = self.bs.find(b':', offset)
        datatype = self.bs[offset:colon]
        print(datatype)
        if datatype.isdigit():
            return (self.parse_string, colon + 1, int(datatype))
        elif datatype == b'l':
            return (self.parse_list, colon + 1, None)


    def decode(self):
        f, after_header, arg = self.type_header(0)
        obj, _ = f(after_header, arg)
        return obj

  
if __name__ == '__main__':
    TEST_FILE = os.path.join(conf.PROJECT_DIRECTORY, 'data', 'tom.torrent')
    with open(TEST_FILE, 'rb') as f:
        text = f.read()
    print(type(text))
    d = Decoder(text, b'info')
    print(d.decode())
    print(d.substrings)
    

