# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import requests_cache
import time
import json
import re

# Get global settings
# requests_cache.install_cache('sensu_cache', backend='sqlite', old_data_on_error=True)

# requests_cache.get_cache()
# session = requests_cache.CachedSession('sensu_cache')
# requests_cache.clear()
# requests_cache.CachedSession()


def get_data(dc, timeout=120, clear_cache=False):
    print "Retrieving data for datacenter: {0}".format(dc['name'])
    # Configure our cache, create one DB per DC.
    requests_cache.install_cache(dc["name"], backend='sqlite', old_data_on_error=True)
    if clear_cache:
        requests_cache.clear()
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
        # print "CACHE USED? {}".format(requests_cache.get_cache())
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


def get_stashes(dc, timeout=120, clear_cache=False):
    print "Retrieving stashes for datacenter: {0}".format(dc['name'])
    # Configure our cache, create one DB per DC.
    requests_cache.install_cache(dc["name"], backend='sqlite', old_data_on_error=True)
    if clear_cache:
        requests_cache.clear()
    url = 'http://{0}:{1}/silenced'.format(dc['url'], dc['port'])
    data = None
    r = None
    now = time.ctime(int(time.time()))
    try:
        if 'user' and 'password' in dc:
            r = requests.get(url, auth=(dc['user'], dc['password']), timeout=timeout)
        else:
            r = requests.get(url, timeout=timeout)
        print "Time: {0} / Stashes Used Cache: {1}".format(now, r.from_cache)
        # print "CACHE USED? {}".format(requests_cache.get_cache())
        r.raise_for_status()
    except Exception as ex:
        print "Got exception while retrieving stashes for dc: {0} ex: {1}".format(dc, str(ex))
        pass
    finally:
        if r:
            data = r.json()
            r.close()
        else:
            print "Got no data while making API call to stashes at {0} ".format(dc)

    print "Data Retrieval for datacenter stashes {0} complete".format(dc['name'])
    return data


def check_stash(stashes, hostname, checkname):
    for s in stashes:
        if re.match('^client:' + hostname + ':' + checkname + '$', s['id']):
            return True
        if re.match('^client:' + hostname + ':\*', s['id']):
            return True
    return False


def agg_dc_data(dcs, clear_cache=False):
    """
    returns: a list of dictionaries [{"dc": "dfw", {"hostname": [list,of,alert,statuses], "hostname2": [list,of,alert,statuses]}}]
    """

    _ok_total = 0
    _crit_total = 0
    _warn_total = 0
    _checks_crit = []
    _checks_warn = []
    _dc_stats = []
    for dc in dcs:
        _ok = 0
        _crit = 0
        _warn = 0
        data = get_data(dc, clear_cache=clear_cache)
        stashes = get_stashes(dc, clear_cache=clear_cache)
        print "Getting aggr data for DC: {}, number of total results: {}".format(dc["name"], len(data))
        for check in data:
            if not check['check']['name'] == "keepalive" and int(check['check']['status']) == 0:
                _ok_total += 1
                _ok += 1
            if not check['check']['name'] == "keepalive" and int(check['check']['status']) == 1:
                _crit_total += 1
                _crit += 1
            if not check['check']['name'] == "keepalive" and int(check['check']['status']) == 2:
                _warn_total += 1
                _warn += 1

            # Get only the desire list of hosts with Critial and Warning alerts.
            if check['check']['status'] and check['check']['name'] != 'keepalive':
                if not check_stash(stashes, check["client"], check['check']['name']):
                    # look only for status 1 Critical and 2 Warning.
                    if int(check['check']['status']) == 1:
                        check["dc"] = dc["name"]
                        _checks_crit.append(check)
                    if int(check['check']['status']) == 2:
                        check["dc"] = dc["name"]
                        _checks_warn.append(check)
        # Now put stats for this particular DC
        _temp_dc_stats = {
            'dc': dc['name'],
            'ok': _ok,
            'crit': _crit,
            'warn': _warn
        }
        _dc_stats.append(_temp_dc_stats)

    # Return this data into one dictionary
    output = {
        "dc_stats": _dc_stats,
        "ok": _ok_total,
        "crit": _crit_total,
        "warn": _warn_total,
        "checks_crit": _checks_crit,
        "checks_warn": _checks_warn,
        "total_dcs": len(dcs)
        }
    # print json.dumps(output, indent=True)
    return output
