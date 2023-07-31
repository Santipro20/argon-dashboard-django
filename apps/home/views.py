# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import Courses, Tasks, Merchants, Geolocation
import pandas as pd 
from apps.home.tasks import num_delivery

#@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    
    # Convert to pandas dataframe
    df_courses = list(Courses.objects.all().values())
    df_tasks = list(Tasks.objects.all().values())
    df_merchants = list(Merchants.objects.all().values())

    result = num_delivery.apply_async(args=[df_courses, df_tasks, df_merchants])
    result_data = result.get()
    num_finised_task, month_growth, df_id_merchant = result_data

    # Share info with the context
    context['number_of_deliveries'] = num_finised_task
    context['porcentage'] = month_growth

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



