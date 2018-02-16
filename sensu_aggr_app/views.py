# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
import helpers

# Get global settings
dcs = getattr(settings, 'DCS', '')


def index(request):
    data = helpers.agg_dc_data(dcs)
    context = {
        'data': data
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
