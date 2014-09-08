"""
Clears the subscription models before running cron jobs
"""

from django.core.management import setup_environ
import settings
setup_environ(settings)

from weatherapp.models import *


def delete_subs():
    """ Deletes entries from all subscription models """
    for sub in NodeDownSub.objects.all():
        sub.subscriber.delete()
    for sub in VersionSub.objects.all():
        sub.subscriber.delete()
    for sub in BandwidthSub.objects.all():
        sub.subscriber.delete()
    for sub in TShirtSub.objects.all():
        sub.subscriber.delete()
    NodeDownSub.objects.all().delete()
    VersionSub.objects.all().delete()
    BandwidthSub.objects.all().delete()
    TShirtSub.objects.all().delete()


def delete_router():
    """ Deletes entries from the Router model """
    for entry in Router.objects.all():
        entry.delete()

if __name__ == "__main__":
    delete_subs()
    delete_router()
