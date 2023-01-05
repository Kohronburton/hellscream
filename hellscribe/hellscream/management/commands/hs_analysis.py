from django.core.management.base import BaseCommand, CommandError
from hellscream.models import WorkPacket
import json
from redis import Redis
from pprint import pprint


class Command(BaseCommand):

    def handle(self, *args, **options):

        i = 0
        for wp in WorkPacket.objects.all().order_by('timestamp'):

            if 'EXECUTIONER_RESULT' in wp.data.keys() and wp.data['EXECUTIONER_RESULT'] == 1:
                pprint(wp.data)

            i += 1

        print(i)
