"""
This module takes a keyword as input and display's results of matching
relays using onionoo's search functionality.
"""

from onionoo_wrapper import *


def print_relays(relays):
    """ Print the nicknames, fingerprints and IP addresses of relays """

    for relay in relays:
        if relay.nickname is None:
            relay_nick = "Unnamed"
        else:
            relay_nick = relay.nickname
        print('Nickname:%s ' % (relay_nick)),
        print('Fingerprint:%s ' % (relay.fingerprint)),
        print('IP address(es):%s ' % (relay.addresses))


def search_relays(query):
    """ Given a search query, returns corresponding relay-details """

    global query_data

    # Onionoo search parameters
    params = {
        'type': 'relay',
        'search': query
    }
    req = objects.OnionooRequest()
    resp = req.get_response('summary', params)
    print_relays(resp.document.relays)


if __name__ == "__main__":
    query = raw_input('Enter relay search-query: ')
    search_relays(query)
