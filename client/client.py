import asyncio
import hashlib

import aiohttp

from bittorrent.bencode.decode import Decoder

class Client(object):
'''Runs the whole show.

TODO
'''
    def __init__(self, torrent):
        self.torrent = torrent
        with open(torrent, 'rb') as f:
            text = f.read()
        decoder = Decoder(text, wanted_substring='info')
        decoder.decode()
        del text
        info_hasher = hashlib.sha1()
        info_hasher.update(decoder.substrings[b'info'])
        self.info_hash = info_hasher.digest()
        
    def run(self):
        
