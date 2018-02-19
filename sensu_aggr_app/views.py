# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
import helpers
import json

# Get global settings
dcs = getattr(settings, 'DCS', '')


def index(request):
    data = helpers.agg_dc_data(dcs)
    # Graph data
    y_data = json.dumps([x['dc'] for x in data['dc_stats']])
    crit_series = json.dumps([x['crit'] for x in data['dc_stats']])
    warn_series = json.dumps([x['warn'] for x in data['dc_stats']])
    ok_series = json.dumps([x['ok'] for x in data['dc_stats']])
    context = {
        'data': data,
        'y_data': y_data,
        'crit_series': crit_series,
        'warn_series': warn_series,
        'ok_series': ok_series
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
