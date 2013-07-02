"""A module for listening to Tor for new consensus events. When one occurs,
initializes the checker/updater cascade in the updaters module."""

import sys, os
import logging
import socket

from config import config
from weatherapp import updaters
from stem.control import EventType, Controller

#very basic log setup
logging.basicConfig(format = '%(asctime) - 15s (%(process)d) %(message)s',
                    level = logging.DEBUG, filename = 'log/weather.log')

def newconsensus_listener(event):
    """Call C{updaters.run_all()} when a NEWCONSENSUS event is received.

    @param event: The NEWCONSENSUS event. Not used by the function.
    """
    
    logging.info('Got a new consensus. Updating router table and ' + \
                     'checking all subscriptions.')
    updaters.run_all()

def listen():
    """Sets up a connection to Tor and initializes a controller to listen for
    new consensus events.
    """
    ctrl = Controller.from_port(config.control_port)
    ctrl.authenticate(config.authenticator)
    ctrl.add_event_listener(newconsensus_listener, EventType.NEWCONSENSUS)
    print 'Listening for new consensus events.'
    logging.info('Listening for new consensus events.')
