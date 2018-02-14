# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
import requests
import requests_cache
import time

# Get global settings
requests_cache.install_cache('sensu_cache', backend='sqlite', old_data_on_error=True)

# requests_cache.get_cache()
# session = requests_cache.CachedSession('sensu_cache')
# requests_cache.clear()
# requests_cache.CachedSession()


def get_data(dc, timeout=120):
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
        # print requests_cache.get_cache()
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
    return data


def agg_host_data(data, stashes, client_data=None, filters=None):
    """
    returns: a dict of {"hostname": [list,of,alert,statuses], "hostname2": [list,of,alert,statuses]}
    """

    _data = data
    _stashes = stashes
    _clients = client_data
    retdata = {}

    if filters and len(filters) > 0:
        filters = filters.split(',')

    if _clients is not None:
        for c in _clients:
            if filters and len(filters) > 0:
                for f in filters:
                    if f in c['subscriptions']:
                        _host = c['name']
                        retdata[_host] = []
                        break
            else:
                _host = c['name']
                retdata[_host] = []
    else:
        for check in _data:
            _host = check['client']
            retdata[_host] = []

    for check in _data:
        _host = check['client']
        if check['check']['status'] and check['check']['name'] != 'keepalive':
            if _host in retdata:
                if not check_stash(_stashes, _host, check['check']['name']):
                    retdata[_host].append(check['check']['status'])

        if check['check']['status'] and check['check']['name'] == 'keepalive':
            if _host in retdata:
                retdata[_host].append(-1)

    assert type(retdata) == dict

    return retdata
