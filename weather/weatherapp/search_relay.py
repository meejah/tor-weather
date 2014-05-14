"""
This module takes a keyword as input and display's results of matching 
relays using onionoo's search functionality.
"""

import urllib2
import urllib
import json

#query_data is a global dictionary
#key is search query
#value is [last-modified timestamp, dict-formatted summary document]
query_data = {}


def print_relays(result_dict):
    """ Print the nicknames, fingerprints and IP addresses of relays """
    for relay in result_dict['relays']:
        if 'n' not in relay.keys():
            relay_nick = "Unnamed"
        else:
            relay_nick = relay['n']
        print('Nickname:%s ' % (relay_nick)),
        print('Fingerprint:%s ' % (relay['f'])),
        print('IP address(es):%s ' % (relay['a']))


def search_relays(query):
    """ Given a search query, return corresponding relay-details """

    global query_data

    # Onionoo search parameters
    base_URL = "https://onionoo.torproject.org/summary"
    params = {
        'type': 'relay',
        'search': query
    }

    # Build the appropriate request
    request_URL = base_URL + '?' + urllib.urlencode(params)
    request = urllib2.Request(url=request_URL)
    if query in query_data.keys():
        request.add_header('If-Modified-Since', query_data[query][0])

    try:
        # Send the request to Onionoo
        result = urllib2.urlopen(request)
        result_dict = json.loads(result.read())

        # Update the global dictionary
        last_modified = result.info().getheader("Last-Modified")
        query_data[query] = [last_modified, result_dict]

        print_relays(result_dict)

    except urllib2.HTTPError, error:
        if error.code == 304:
            # Not Modified
            print_relays(query_data[query][1])
        else:
            print("Error " + str(error.code) + ": " + error.reason)


if __name__ == "__main__":
    query = raw_input('Enter relay search-query: ')
    search_relays(query)
