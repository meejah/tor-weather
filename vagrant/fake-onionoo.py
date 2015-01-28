#!/usr/bin/env python

# this pretends to be OnionOO, returning some pre-canned results
# simply based on the type of document. It runs inside the Vagrant
# host. Run it thusly:
# twistd -n cyclone run fake-onionoo.py

import cyclone.web
import json

summary = dict(
    version="2.2",
    relays_published="2015-01-27 22:00:00",
    relays=[
        {"n":"cepa","f":"B69D45E2AC49A81E014425FF6E07C7435C9F89B0","a":["5.101.102.82"],"r":False},
    ],
    bridges_published="2015-01-27 21:56:40",
    bridges=[],
)

details = dict(
    version="2.2",
    relays_published="2015-01-28 07:00:00",
    relays=[
        {"nickname":"cepa",
         "fingerprint":"B69D45E2AC49A81E014425FF6E07C7435C9F89B0",
         "or_addresses":["5.101.102.82:9001"],
         "last_seen":"2015-01-28 07:00:00",
         "last_changed_address_or_port":"2014-07-02 08:00:00",
         "first_seen":"2014-07-02 08:00:00",
         "running":True,
         "flags":["Fast","Running","Valid"],
         "country":"nl",
         "country_name":"Netherlands",
         "latitude":52.5,
         "longitude":5.75,
         "as_number":"AS200130",
         "as_name":"Digital Ocean, Inc.",
         "consensus_weight":2160,
         "host_name":"5.101.102.82",
         "last_restarted":"2015-01-28 00:00:00",
         "bandwidth_rate":1048576,
         "bandwidth_burst":1073741824,
         "observed_bandwidth":4387344,
         "advertised_bandwidth":1048576,
         "exit_policy":["reject *:*"],
         "exit_policy_summary":{"reject":["1-65535"]},
         "contact":"0xC2602803128069A7 meejah <meejah@meejah.ca>",
         "platform":"Tor 0.2.4.23 on Linux",
         "consensus_weight_fraction":6.11742E-5,
         "guard_probability":0.0,
         "middle_probability":1.7412592E-4,
         "exit_probability":0.0,
         "recommended_version":True},
    ],
    bridges_published="2015-01-28 06:59:05",
    bridges=[]
)

class CannedResponseHandler(cyclone.web.RequestHandler):
    def initialize(self, ham):
        self.canned = ham

    def get(self):
        self.write(self.canned)
        self.finish()


class Application(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/summary", CannedResponseHandler, dict(ham=summary)),
            (r"/details", CannedResponseHandler, dict(ham=details)),
        ]
        settings = dict(
        )
        cyclone.web.Application.__init__(self, handlers, **settings)

application = Application()
