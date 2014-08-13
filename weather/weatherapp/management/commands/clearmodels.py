"""
A custom django-admin command to clear the subscription and the Router models.
This should be run as follows :
$python manage.py clearsubs
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.management import setup_environ
from weatherapp.models import *
import settings
setup_environ(settings)


class Command(BaseCommand):
    help = 'Clears the Router and subscription models'

    def handle(self, *args, **options):
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
        for entry in Router.objects.all():
            entry.delete()
        for entry in Subscriber.objects.all():
            entry.delete()
