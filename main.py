import argparse

import bittorrent.client.request as request


CLIENT_NAME = 'TitBorrent'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command-line interface for {}'.format(CLIENT_NAME))
    parser.add_argument('-d', '--debug', action='store_true', help='Print debugging messages')
    parser.add_argument('-l', '--log', type=str)
    parser.add_argument("torrent_file", help="Path to the .torrent file")
    args = parser.parse_args()

    if debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    if log:
        # figure out what you want this to do
        pass


    # general scheme
    # pass pertinent args to client
    # client parses .torrent
    # client hashes info dict
    
    
