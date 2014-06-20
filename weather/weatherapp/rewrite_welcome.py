"""
Sends welcome emails to new Tor relay operators.
Check out https://trac.torproject.org/projects/tor/ticket/11081
"""

from weatherapp import emails
from weatherapp.models import Router, DeployedDatetime

from datetime import *
from onionoo_wrapper.objects import *
from onionoo_wrapper.utilities import *


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_cutoff_time():
    """ Returns the cutoff time for routers to be considered """
    return (datetime.now() - timedelta(days=6*30))


def get_deploy_time():
    """ Returns the time of deployment of current weather instance """
    deployed_query = DeployedDatetime.objects.all()
    if len(deployed_query) == 0:
        # DeployedDatetime model hasn't been populated yet
        deploy_time = datetime.now()
        DeployedDatetime(deployed=deploy_time).save()
    else:
        deploy_time = deployed_query[0].deployed
    return deploy_time


def get_stable_relays():
    """ Returns a list of RelayDetails objects with stable flag """
    req = OnionooRequest()
    params = {
        'type': 'relay',
        'running': 'true',
        'flag': 'stable'
    }
    details_doc = req.get_response('details', params=params)
    return details_doc.relays


def is_recent(relay):
    """ Returns True if relay is recent enough, False otherwise """
    cutoff_time = get_cutoff_time()
    deploy_time = get_deploy_time()
    first_seen = datetime.strptime(relay.first_seen, TIME_FORMAT)
    time_diff = (first_seen - max(deploy_time, cutoff_time)).total_seconds()
    return (time_diff > 0)


def add_entry(relay):
    """ Add entry corresponding to the relay to the Router model """
    is_exit = check_exitport(relay)
    router_entry = Router(fingerprint=relay.fingerprint,
                          name=relay.nickname,
                          welcomed=True,
                          last_seen=relay.last_seen,
                          up=True,
                          exit=is_exit)
    router_entry.save()


def delete_old_entries():
    """ Delete relay entries with old enough timestamps """
    cutoff_time = get_cutoff_time()
    deploy_time = get_deploy_time()
    for entry in Router.objects.all():
        last_seen = entry.last_seen
        if (last_seen - max(deploy_time, cutoff_time)).total_seconds() < 0:
            entry.delete()


if __name__ == "__main__":
    # Fetch new stable relays and send them welcome emails
    relays = get_stable_relays()
    email_list = []
    for relay in relays:
        email_id = scraper.deobfuscate_mail(relay.contact)
        if is_recent(relay) and email_id != '':
            if Router.objects.get(fingerprint=relay.fingerprint) == []:
                # New relay so populate Router model and add to email list
                add_entry(relay)
                email = emails.welcome_tuple(email_id, relay.fingerprint,
                                             relay.nickname, is_exit)
                email_list.append(email)

    # Send welcome emails to the selected operators
    send_mass_mail(tuple(email_list), fail_silently=False)

    # Delete old relay-entries from the database
    delete_old_entries()
