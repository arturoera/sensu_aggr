from django.core.management.base import BaseCommand
import requests
import requests_cache
import time
from django.conf import settings


class Command(BaseCommand):
    help = "Create sensu cache"

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        # Get global settings
        dcs = getattr(settings, 'DCS', '')
        dc = dcs[0]
        print dc
        timeout = 120
        requests_cache.install_cache('sensu_cache', backend='sqlite', expire_after=45)
        # cache = requests_cache.get_cache()

        # requests_cache.core.remove_expired_responses()
        # requests_cache.clear()

        print "Retrieving data for datacenter: {0}".format(dc['name'])
        url = 'http://{0}:{1}/results'.format(dc['url'], dc['port'])
        data = None
        r = None
        now = time.ctime(int(time.time()))
        try:
            if 'user' and 'password' in dc:
                r = requests.get(url, auth=(dc['user'], dc['password']), timeout=timeout)
            else:
                r = requests.get(url, timeout=timeout)
            print "Time: {0} / Used Cache: {1}".format(now, r.from_cache)
            r.raise_for_status()
        except Exception as ex:
            print "Got exception while retrieving data for dc: {0} ex: {1}".format(dc, str(ex))
            pass
        finally:
            if r:
                data = r.json()
                r.close()
            else:
                print "Got no data while making API call to {0} ".format(dc)

        print "Data Retrieval for datacenter {0} complete".format(dc['name'])
