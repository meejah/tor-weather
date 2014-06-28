"""
Object definitions for the Onionoo wrapper
"""

import requests


class BaseError(Exception):
    pass


class InvalidDocumentTypeError(BaseError):
    """ Raised when document type requested is not supported by Onionoo """
    def __init__(self, doc_type):
        self.doc_type = doc_type

    def __str__(self):
        return 'Invalid document type ' + repr(self.doc_type)


class InvalidParameterError(BaseError):
    """ Raised when a request parameter is not supported by Onionoo """
    def __init__(self, param):
        self.param = param

    def __str__(self):
        return 'Invalid parameter ' + repr(self.param)


class OnionooError(BaseError):
    """ Raised when Onionoo responds with an error code """
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return str(self.code) + ' - ' + self.msg


class DataError(BaseError):
    """ Raised due to insufficient/inconsistent data """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class BaseClass(object):
    pass


class _DocumentForwarder(BaseClass):
    doc = None
    keys = dict()

    def __getattr__(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        # we purposely let KeyError propagate up, if thrown
        doc_key = self.keys[k]
        if not doc_key:
            doc_key = k
        return self.doc.get(doc_key)


class RelaySummary(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(nickname='n', fingerprint='f', addresses='a',
                         running='r')

    def __str__(self):
        return "Relay summary for %s (%s) " % \
            (self.nickname or "<Not named>", self.fingerprint or
                "<No fingerprint>")


class BridgeSummary(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(nickname='n', hash='h', running='r')

    def __str__(self):
        return "Bridge summary for %s (%s) " % \
            (self.nickname or "<Not named>", self.fingerprint or
                "<No fingerprint>")


class Summary(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(relays_published=None, bridges_published=None)
        self.relays = [RelaySummary(d) for d in document.get('relays')]
        self.bridges = [BridgeSummary(d) for d in document.get('bridges')]

    def __str__(self):
        return "Summary document (%d bridges, %d relays)" % \
            (len(self.bridges or []), len(self.relays or []))


class RelayDetails(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(nickname=None, fingerprint=None, or_addresses=None,
                         exit_addresses=None, dir_address=None,
                         last_seen=None, last_changed_address_or_port=None,
                         first_seen=None, running=None, hibernating=None,
                         flags=None, as_number=None, as_name=None,
                         consensus_weight=None, host_name=None,
                         last_restarted=None, exit_policy=None,
                         exit_policy_summary=None,
                         exit_policy_v6_summary=None, contact=None,
                         platform=None, recommended_version=None, family=None,
                         advertised_bandwidth_fraction=None,
                         consensus_weight_fraction=None,
                         guard_probability=None, middle_probability=None,
                         exit_probability=None)
        self.geo = (self.doc.get('country'), self.doc.get('country_name'),
                    self.doc.get('region_name'), self.doc.get('city_name'),
                    self.doc.get('latitude'), self.doc.get('longitude'))
        self.bandwidth = (self.doc.get('bandwidth_rate'),
                          self.doc.get('bandwidth_burst'),
                          self.doc.get('bandwidth_observed'),
                          self.doc.get('bandwidth_advertised'))

    def __str__(self):
        return "Detailed relay descriptor for %s (%s)" % \
            (self.nickname or "<Not named>", self.fingerprint or
                "<No fingerprint>")


class BridgeDetails(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(nickname=None, hashed_fingerprint=None,
                         or_address=None, last_seen=None, first_seen=None,
                         running=None, flags=None, last_restarted=None,
                         advertised_bandwidth=None, platform=None,
                         pool_assignment=None)

    def __str__(self):
        return "Detailed bridge descriptor for %s (%s)" % \
            (self.nickname or "<Not named>", self.hashed_fingerprint or
                "<No fingerprint>")


class Details(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(relays_published=None, bridges_published=None)
        self.relays = [RelayDetails(d) for d in self.doc.get('relays')]
        self.bridges = [BridgeDetails(d) for d in self.doc.get('bridges')]

    def __str__(self):
        return "Details document (%d bridges, %d relays)" % \
            (len(self.bridges or []), len(self.relays or []))


class GraphHistory(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(first=None, last=None, interval=None, factor=None,
                         count=None, values=None)

    def __str__(self):
        return "Graph history object"


class BandwidthDetail(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(fingerprint=None)
        self.write_history = dict([(k, GraphHistory(v)) for k, v in
                                  self.doc.get('write_history').items()])
        self.read_history = dict([(k, GraphHistory(v)) for k, v in
                                  self.doc.get('read_history').items()])

    def __str__(self):
        return "Bandwidth object"


class Bandwidth(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(relays_published=None, bridges_published=None)
        self.relays = [BandwidthDetail(d) for d in self.doc.get('relays')]
        self.bridges = [BandwidthDetail(d) for d in self.doc.get('bridges')]

    def __str__(self):
        return "Bandwidth document(histories of %d bridges and %d relays)" % \
            (len(self.bridges or []), len(self.relays or []))


class RelayWeight(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(fingerprint=None)
        self.advertised_bandwidth_fraction = \
            dict([(k, GraphHistory(v)) for k, v in
                  self.doc.get('advertised_bandwidth_fraction').items()])
        self.consensus_weight_fraction = \
            dict([(k, GraphHistory(v)) for k, v in
                  self.doc.get('consensus_weight_fraction').items()])
        self.guard_probability = \
            dict([(k, GraphHistory(v)) for k, v in
                  self.doc.get('guard_probability').items()])
        self.middle_probability = \
            dict([(k, GraphHistory(v)) for k, v in
                  self.doc.get('middle_probability').items()])
        self.exit_probability = \
            dict([(k, GraphHistory(v)) for k, v in
                  self.doc.get('exit_probability').items()])

    def __str__(self):
        return "relay weight object for %s" % (self.fingerprint or
                                               '<no fingerprint>')


class Weights(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(relays_published=None, bridges_published=None)
        self.relays = [RelayWeight(d) for d in self.doc.get('relays')]
        self.bridges = []

    def __str__(self):
        return "Weights document containing weight history for %d relays)" % \
            (len(self.relays or []))


class BridgeClient(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(fingerprint=None)
        self.average_clients = \
            dict([(k, GraphHistory(v)) for k, v in
                  self.doc.get('average_clients').items()])

    def __str__(self):
        return "Bridge client history object for %s" % (self.fingerprint or
                                                        '<no fingerprint>')


class Clients(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(relays_published=None, bridges_published=None)
        self.relays = []
        self.bridges = [BridgeClient(d) for d in self.doc.get('bridges')]

    def __str__(self):
        return "Clients document containing client histories for %d bridges" \
            % (len(self.bridges or []))


class RelayUptime(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(fingerprint=None)
        self.uptime = {}
        if 'uptime' in self.doc.keys():
            self.uptime = dict([(k, GraphHistory(v)) for k, v in
                                self.doc.get('uptime').items()])

    def __str__(self):
        return "Relay uptime history object for %s" % (self.fingerprint or
                                                       '<no fingerprint>')


class Uptime(_DocumentForwarder):
    def __init__(self, document):
        self.doc = document
        self.keys = dict(relays_published=None, bridges_published=None)
        self.relays = [RelayUptime(d) for d in self.doc.get('relays')]
        self.bridges = [RelayUptime(d) for d in self.doc.get('bridges')]

    def __str__(self):
        return "Uptime document (Containing uptime histories for %d bridges\
            and %d relays)" % (len(self.bridges or []), len(self.relays or []))


class OnionooResponse(BaseClass):
    """ """
    def __init__(self, headers={}, status_code=None, document=None):
        self.headers = headers
        self.status_code = status_code
        self.document = document

    def __str__(self):
        return self.document


class OnionooRequest(BaseClass):
    """ A class for making sequential requests to Onionoo """

    ONIONOO_URL = 'https://onionoo.torproject.org/'
    DOC_TYPES = {
        'summary': Summary,
        'details': Details,
        'bandwidth': Bandwidth,
        'weights': Weights,
        'clients': Clients,
        'uptime': Uptime
    }
    PARAMETERS = [
        'type',
        'running',
        'search',
        'lookup',
        'country',
        'as',
        'flag',
        'first_seen_days',
        'last_seen_says',
        'contact',
        'fields',
        'order',
        'offset',
        'limit'
    ]

    def __init__(self, host=None):
        self.base_URL = host or self.ONIONOO_URL

    def get_response(self, doc_type, params={}):
        """
        Fetches requested document from Onionoo and
        returns it as an encapsulated OnionooResponse object
        """

        # Check if document requested is valid
        if doc_type.lower() not in self.DOC_TYPES.keys():
            raise InvalidDocumentTypeError(doc_type)
        doc_type = doc_type.lower()

        # Check if request parameters are valid
        for param in params.keys():
            if param not in self.PARAMETERS:
                raise InvalidParameterError(param)

        # Send the request
        req = requests.get(self.base_URL + doc_type,
                           params=params)

        # Format result based on response code
        if req.status_code != 200:
            raise OnionooError(req.status_code, req.reason)
        else:
            result = self.DOC_TYPES[doc_type](req.json())

        response = OnionooResponse(headers=req.headers,
                                   status_code=req.status_code,
                                   document=result)

        return response
