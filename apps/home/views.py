# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.tasks import num_delivery, get_data_cydi, get_data_id, eco_km, time_eco, CO2
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt

stored_selected_date = None

#@login_required(login_url="/login/")
@csrf_protect
def index(request):
    context = {'segment': 'index'}

    if request.method == 'POST':
        selected_date = request.POST.get('date_selectionnee')
        if selected_date:
            stored_selected_date = selected_date
        else:
            stored_selected_date = None 

    num_delivery_result = num_delivery()
    economi_km = eco_km()
    time_eco_e = time_eco()
    CO2_fun = CO2() 

    month_growth,num_finised_task = num_delivery_result
    km_saved, km_saved_total = economi_km
    time_saved, time_saved_total = time_eco_e
    emi,emi_total,c1,c2 = CO2_fun
     

    # Share info with the context
    context['number_of_deliveries'] = num_finised_task
    context['porcentage'] = month_growth
    context['porcentage_km'] = km_saved
    context['value_km'] = km_saved_total
    context['value_h'] = time_saved_total
    context['porcentage_h'] = time_saved
    context['value_e'] = emi_total
    context['porcentage_e'] = emi

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



