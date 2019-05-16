# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required( login_url = '/accounts/login/')
def index(request):
    template_name = 'manager/index.html'
    return render(request,template_name)