"""
A custom django-admin command to collect emails for hourly notifications.
This should be run as follows :
$python manage.py runhourly
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.management import setup_environ
import settings
setup_environ(settings)

from weatherapp import emails
from weatherapp.models import *

from datetime import *
from onion_py.manager import Manager


def get_relays():
    """ Returns a list of relays from Onionoo as RelayDetails objects """
    doc = Manager().query(
        'details',
        type='relay',
        fields='nickname,fingerprint,observed_bandwidth,running'
    )
    return doc.relays


def get_low_bandwidth_emails(relay, email_list):
    """ Returns email-list of LowBandwidth subscribers to be notified """
    subscriptions = BandwidthSub.objects.filter(
        subscriber__router__fingerprint=relay.fingerprint,
        subscriber__confirmed=True)
    for subcription in subscriptions:
        subscriber = subscription.subscriber
        low_bandwidth_check = checks.is_bandwidth_low(relay, subscription)
        if low_bandwidth_check is False:
            subscription.emailed = False
        elif subscription.emailed is False:
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


def get_nodedown_emails(relay, email_list):
    """ Returns email-list of NodeDown subscribers to be notified """
    subscriptions = NodeDownSub.objects.filter(
        subscriber__router__fingerprint=relay.fingerprint,
        subscriber__confirmed=True)
    for sub in subscriptions:
        if relay.running is True:
            if sub.triggered is True:
                sub.triggered = False
                sub.last_changed = relay.last_seen
        elif relay.hibernating is not True:
            if sub.triggered is not True:
                sub.triggered = True
                sub.last_changed = relay.last_seen
            if sub.is_grace_passed() and sub.emailed is not True:
                email = emails.node_down_tuple(sub.subscriber.email,
                                               relay.fingerprint,
                                               relay.nickname,
                                               sub.grace_pd,
                                               sub.subscriber.unsubs_auth,
                                               sub.subscriber.pref_auth)
                email_list.append(email)
                sub.emailed = True
    return email_list


class Command(BaseCommand):
    help = 'Clears the Router and subscription models'

    def handle(self, *args, **options):
        # Fetch all running relays
        relays = get_relays()
        email_list = []
        for relay in relays:
            if relay.running is True:
                email_list = get_low_bandwidth_emails(relay, email_list)
            email_list = get_nodedown_emails(relay, email_list)

        # Send the notification emails to selected subscribers
        #send_mass_mail(tuple(email_list), fail_silently=False)

