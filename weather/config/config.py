"""
Configuration settings.

See docs/INSTALL -- you'll want to change base_url to reflect where
this is being deployed.

@var authenticator: The authentication key
@var listener_port: The Tor control port for the listener to use. This port
    must be configured in the torrc file.
@var updater_port: The Tor control port for the updater to use. This port
    must be configured in the torrc file.
@var base_url: The root URL for the Tor Weather web application.
"""

import os
# XXX: Make bulletproof
path = os.path.split(os.path.realpath(__file__))[0]
authenticator = open(os.path.join(path, "auth_token"), "r").read().strip()

#The Tor control port to use
control_port = 9051

#The base URL for the Tor Weather web application:
base_url = 'https://weather.dev'
