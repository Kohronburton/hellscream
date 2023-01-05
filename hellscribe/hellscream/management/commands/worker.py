from django.core.management.base import BaseCommand, CommandError
from hellscream.models import WorkPacket
import json
from pprint import pprint
from redis import Redis


class Command(BaseCommand):

    def handle(self, *args, **options):

        r = Redis(unix_socket_path='/var/run/redis/redis-server.sock')

        pub_sub = r.pubsub()
        pub_sub.subscribe('hellscribe')

        print('Hellscibe Ready.')
        while True:
            msg = pub_sub.get_message(timeout=5)
            if msg is None:
                continue
            else:
                # This is the initialization message
                if type(msg['data']) == int:
                    pprint(msg)
                else:
                    work = json.loads(msg['data'].decode('utf-8'))

                    pprint(msg)
                    wp = WorkPacket()
                    wp.data = work
                    wp.save()
