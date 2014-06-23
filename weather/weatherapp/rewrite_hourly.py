"""
Runs hourly and notifies subscribers if relays have been slow or down.
Check out https://trac.torproject.org/projects/tor/ticket/10697
"""

from weatherapp import emails
from weatherapp.models import *

from datetime import *
from onionoo_wrapper.objects import *
from onionoo_wrapper.utilities import *


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_running_relays():
    """ Returns a list of running relays as RelayDetails objects """
    req = OnionooRequest()
    params = {
        'type': 'relay',
        'running': 'true',
        'fields': 'nickname,fingerprint,observed_bandwidth'
    }
    details_doc = req.get_response('details', params=params)
    return details_doc.relays


def get_low_bandwidth_emails(relay):
    """ Returns email-list of LowBandwidth subscribers """
    email_list = []
    subsciptions = BandwidthSub.objects.filter
                        (subscriber__rouer__fingerprint=relay.fingerprint,
                         subscriber__confirmed=True)
    for subcription in subscriptions:
        subscriber = subscription.subscriber
        low_bandwidth_check = checks.is_bandwidth_low(relay, subscription)
        if low_bandwidth_check is False:
            subscription.emailed = False
        else if subscription.emailed is False:
            subscription.emailed = True
            email = emails.bandwidth_tuple(subscriber.email,
                                           relay.fingerprint,
                                           relay.nickname,
                                           relay.observed_bandwidth,
                                           subscription.threshold,
                                           subscriber.unsubs_auth,
                                           subscriber.pref_auth)
            email_list.append(email)
    return email_list


def get_nodedown_emails(relay, subscribers):
    """ Returns email-list of NodeDown subscribers """
    return None


if __name__ == "__main__":
    # Fetch all running relays
    relays = get_running_relays()
    email_list = []
    for relay in relays:
        email_list.append(get_low_bandwidth_emails(relay))
        email_list.append(get_nodedown_emails(relay)
    # Send welcome emails to the selected subscribers
    send_mass_mail(tuple(email_list), fail_silently=False)
