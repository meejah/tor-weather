"""
Object definitions for the onionoo wrapper
"""

import requests
import caching


class InvalidDocumentTypeError(Exception):
    def __init__(self, doc_type):
        self.doc_type = doc_type

    def __str__(self):
        return 'Invalid document type ' + repr(self.doc_type)


class OnionooError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return str(self.code) + ' - ' + self.msg


class RelaySummary:
    def __init__(self, document):
        self.nickname = document.get('n')
        self.fingerprint = document.get('f')
        self.addresses = document.get('a')
        self.running = document.get('r')

    def __str__(self):
        return "Relay summary for %s (%s) " % \
            (self.nickname or "<Not named>", self.fingerprint or
                "<No fingerprint>")


class BridgeSummary:
    def __init__(self, document):
        self.nickname = document.get('n')
        self.hash = document.get('h')
        self.running = document.get('r')

    def __str__(self):
        return "Bridge summary for %s (%s) " % \
            (self.nickname or "<Not named>", self.fingerprint or
                "<No fingerprint>")


class Summary:
    def __init__(self, document):
        self.relays_published = document.get('relays_published')
        self.bridges_published = document.get('bridges_published')
        self.relays = [RelaySummary(d) for d in document.get('relays')]
        self.bridges = [BridgeSummary(d) for d in document.get('bridges')]

    def __str__(self):
        return "Summary document (%d bridges, %d relays)" % \
            (len(self.bridges or []), len(self.relays or []))


class RelayDetails:
    def __init__(self, document):
        g = document.get
        self.nickname = g('nickname')
        self.fingerprint = g('fingerprint')
        self.or_addresses = g('or_addresses')
        self.exit_addresses = g('exit_addresses')
        self.dir_address = g('dir_address')
        self.last_seen = g('last_seen')
        self.last_changed_address_or_port = g('last_changed_address_or_port')
        self.first_seen = g('first_seen')
        self.running = g('running')
        self.hibernating = g('hibernating')
        self.flags = g('flags')
        self.geo = (g('country'), g('country_name'), g('region_name'),
                    g('city_name'), g('latitude'), g('longitude'))
        self.as_number = g('as_number')
        self.as_name = g('as_name')
        self.consensus_weight = g('consensus_weight')
        self.host_name = g('host_name')
        self.last_restarted = g('last_restarted')
        self.bandwidth = (g('bandwidth_rate'), g('bandwidth_burst'),
                          g('bandwidth_observed'), g('bandwidth_advertised'))
        self.exit_policy = g('exit_policy')
        self.exit_policy_summary = g('exit_summary_policy')
        self.exit_policy_v6_summary = g('exit_policy_v6_policy')
        self.contact = g('contact')
        self.platform = g('platform')
        self.recommended_version = g('recommended_version')
        self.family = g('family')
        self.advertised_bandwidth_fraction = \
            g('advertised_bandwidth_fraction')
        self.consensus_weight_fraction = g('consensus_weight_fraction')
        self.guard_probability = g('guard_probability')
        self.middle_probability = g('middle_probability')
        self.exit_probability = g('exit_probability')

    def __str__(self):
        return "Detailed relay descriptor for %s (%s)" % \
            (self.nickname or "<Not named>", self.fingerprint or
                "<No fingerprint>")


class BridgeDetails:
    def __init__(self, document):
        g = document.get
        self.nickname = g('nickname')
        self.hashed_fingerprint = g('hashed_fingerprint')
        self.or_address = g('or_address')
        self.last_seen = g('last_seen')
        self.first_seen = g('first_seen')
        self.running = g('running')
        self.flags = g('flags')
        self.last_restarted = g('last_restarted')
        self.advertised_bandwidth = g('advertised_bandwidth')
        self.platform = g('platform')
        self.pool_assignment = g('pool_assignment')

    def __str__(self):
        return "Detailed bridge descriptor for %s (%s)" % \
            (self.nickname or "<Not named>", self.hashed_fingerprint or
                "<No fingerprint>")


class Details:
    def __init__(self, document):
        self.relays_published = document.get('relays_published')
        self.bridges_published = document.get('bridges_published')
        self.relays = [RelayDetails(d) for d in document.get('relays')]
        self.bridges = [BridgeDetails(d) for d in document.get('bridges')]

    def __str__(self):
        return "Details document (%d bridges, %d relays)" % \
            (len(self.bridges or []), len(self.relays or []))


class GraphHistory:
    def __init__(self, document):
        g = document.get
        self.first = g('first')
        self.last = g('last')
        self.interval = g('interval')
        self.factor = g('factor')
        self.count = g('count')
        self.values = g('values')

    def __str__(self):
        return "Graph history object"


class BandwidthDetail:
    def __init__(self, document):
        g = document.get
        self.finger_print = g('fingerprint')
        self.write_history = dict([(k, GraphHistory(v)) for k, v in
                                  g('write_history').items()])
        self.read_history = dict([(k, GraphHistory(v)) for k, v in
                                  g('read_history').items()])

    def __str__(self):
        return "Bandwidth object"


class Bandwidth:
    def __init__(self, document):
        g = document.get
        self.relays_published = g('relays_published')
        self.bridges_published = g('bridges_published')
        self.relays = [BandwidthDetail(d) for d in g('relays')]
        self.bridges = [BandwidthDetail(d) for d in g('bridges')]

    def __str__(self):
        return "Bandwidth document(histories of %d bridges and %d relays)" % \
            (len(self.bridges or []), len(self.relays or []))


class RelayWeight:
    def __init__(self, document):
        g = document.get
        self.fingerprint = g('fingerprint')
        self.advertised_bandwidth_fraction = \
            dict([(k, GraphHistory(v)) for k, v in
                  g('advertised_bandwidth_fraction').items()])
        self.consensus_weight_fraction = \
            dict([(k, GraphHistory(v)) for k, v in
                  g('consensus_weight_fraction').items()])
        self.guard_probability = \
            dict([(k, GraphHistory(v)) for k, v in
                  g('guard_probability').items()])
        self.middle_probability = \
            dict([(k, GraphHistory(v)) for k, v in
                  g('middle_probability').items()])
        self.exit_probability = \
            dict([(k, GraphHistory(v)) for k, v in
                  g('exit_probability').items()])

    def __str__(self):
        return "relay weight object for %s" % (self.fingerprint or
                                               '<no fingerprint>')


class Weights:
    def __init__(self, document):
        g = document.get
        self.relays_published = g('relays_published')
        self.bridges_published = g('bridges_published')
        self.relays = [RelayWeight(d) for d in g('relays')]
        self.bridges = []

    def __str__(self):
        return "Weights document containing weight history for %d relays)" % \
            (len(self.relays or []))


class BridgeClient:
    def __init__(self, document):
        g = document.get
        self.fingerprint = g('fingerprint')
        self.average_clients = \
            dict([(k, GraphHistory(v)) for k, v in
                  g('average_clients').items()])

    def __str__(self):
        return "Bridge client history object for %s" % (self.fingerprint or
                                                        '<no fingerprint>')


class Clients:
    def __init__(self, document):
        g = document.get
        self.relays_published = g('relays_published')
        self.bridges_published = g('bridges_published')
        self.relays = []
        self.bridges = [BridgeClient(d) for d in g('bridges')]

    def __str__(self):
        return "Clients document containing client histories for %d bridges" \
            % (len(self.bridges or []))


class RelayUptime:
    def __init__(self, document):
        g = document.get
        self.fingerprint = g('fingerprint')
        self.uptime = dict([(k, GraphHistory(v)) for k, v in
                            g('uptime').items()])

    def __str__(self):
        return "Relay uptime history object for %s" % (self.fingerprint or
                                                       '<no fingerprint>')


class Uptime:
    def __init__(self, document):
        g = document.get
        self.relays_published = g('relays_published')
        self.bridges_published = g('bridges_published')
        self.relays = [RelayUptime(d) for d in g('relays')]
        self.bridges = [RelayUptime(d) for d in g('bridges')]

    def __str__(self):
        return "Uptime document (Containing uptime histories for %d bridges\
            and %d relays)" % (len(self.bridges or []), len(self.relays or []))


class OnionooResponse:
    def __init__(self, headers={}, status_code=None, document=None):
        self.headers = headers
        self.status_code = status_code
        self.document = document

    def __str__(self):
        return self.document


class OnionooRequest:
    ONIONOO_URL = 'https://onionoo.torproject.org/'
    DOC_TYPES = {
        'summary': Summary,
        'details': Details,
        'bandwidth': Bandwidth,
        'weights': Weights,
        'clients': Clients,
        'uptime': Uptime
    }

    def __init__(self, cache=None, host=None):
        self.base_URL = host or self.ONIONOO_URL
        self.cache_client = cache or caching.SimpleCache()

    def build_request(self, doc_type, params={}):
        self.doc_type = doc_type
        self.params = {}
        self.params = params

    def get_response(self):
        # Check if document is requested is valid
        if self.doc_type.lower() not in self.DOC_TYPES.keys():
            raise InvalidDocumentTypeError(self.doc_type)
        self.doc_type = self.doc_type.lower()

        # Check cache entries for similar request
        cache_entry = None
        cache_entry = self.cache_client.get(self.doc_type, self.params)

        result = None
        headers = {}
        # Add header if there is a cache hit
        if cache_entry is not None:
            last_entry_time = cache_entry['timestamp']
            headers['If-Modified-Since'] = last_entry_time

        # Send the request
        req = requests.get(self.base_URL + self.doc_type,
                           params=self.params,
                           headers=headers)

        # Format result based on response code
        if cache_entry is not None and \
           req.status_code == requests.codes.NOT_MODIFIED:
            result = cache_entry['record']
        elif req.status_code != requests.codes.OK:
            raise OnionooError(req.status_code, req.reason)
        else:
            result = self.DOC_TYPES[self.doc_type](req.json())

        response = OnionooResponse(headers=req.headers,
                                   status_code=req.status_code,
                                   document=result)

        # Update cache
        cache_entry = {'timestamp': req.headers['date'],
                       'record': result}
        self.cache_client.set(self.doc_type, self.params, cache_entry)

        return response
