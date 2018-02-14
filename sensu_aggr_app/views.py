# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from helpers import get_data

# Get global settings
dcs = getattr(settings, 'DCS', '')


def index(request):
    data = get_data(dcs[0])
    context = {
        'data': data
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
