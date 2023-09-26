# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.tasks import num_delivery, get_data_cydi, get_data_id, eco_km, time_eco, CO2, graph_CO2, equivalence,space_eco
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect #csrf_exempt



#@login_required(login_url="/login/")
@csrf_protect
def index(request):
    stored_selected_date = None
    context = {'segment': 'index'}

    num_delivery_result = num_delivery(stored_selected_date) 
    economi_km = eco_km(stored_selected_date) 
    time_eco_e = time_eco(stored_selected_date) 
    CO2_fun = CO2(stored_selected_date)
    graph = graph_CO2(stored_selected_date)
    equ = equivalence(stored_selected_date)
    sp = space_eco(stored_selected_date)

    num_finised_task = num_delivery_result
    km_saved, km_saved_total = economi_km
    time_saved, time_saved_total = time_eco_e
    emi,emi_total,driving,cycling,deki_vul  = CO2_fun
    VUL_met, VUL_no2, VUL_NOx, VUL_CO, VUL_PM,deki_met, deki_no2,deki_NOx,deki_CO, deki_PM,deki_vul_met,deki_vul_no2,deki_vul_NOx,deki_vul_CO,deki_vul_PM= graph
    charger_iphone,charger_mac,trees,train, diesel, uber, print_sheet, emails, labor, water, pain, fromage  = equ
    sc_s,sc_vul,sc_deki=sp

    # Share info with the context
    context['number_of_deliveries'] = num_finised_task
    context['porcentage_km'] = km_saved
    context['value_km'] = km_saved_total
    context['value_h'] = time_saved_total
    context['porcentage_h'] = time_saved
    context['value_e'] = emi_total
    context['porcentage_e'] = emi
    context['driving_data'] = driving
    context['cycling_data'] = cycling
    context['deki_vul_data'] = deki_vul
    context['VUL_met_data'] = VUL_met
    context['VUL_no2_data'] = VUL_no2
    context['VUL_NOx_data'] = VUL_NOx
    context['VUL_CO_data'] = VUL_CO
    context['VUL_PM_data'] = VUL_PM
    context['deki_met_data'] = deki_met
    context['deki_no2_data'] = deki_no2
    context['deki_NOx_data'] = deki_NOx
    context['deki_CO_data'] = deki_CO
    context['deki_PM_data'] = deki_PM
    context['deki_vul_met_data'] = deki_vul_met
    context['deki_vul_no2_data'] = deki_vul_no2
    context['deki_vul_NOx_data'] = deki_vul_NOx
    context['deki_vul_CO_data'] = deki_vul_CO
    context['deki_vul_PM_data'] = deki_vul_PM
    context['recharge_portable'] = charger_iphone
    context['recharge_ordina'] = charger_mac
    context['arbes_hec'] = trees
    context['train_voya'] = train 
    context['diesel_E10'] = diesel
    context['uber_livra'] = uber
    context['feuilles_print'] = print_sheet
    context['emails'] = emails
    context['travailleur_moyen'] = labor
    context['water_bo'] = water
    context['pain_tranches'] = pain
    context['portion_fromage'] = fromage
    context['sc_eco'] = sc_s
    context['sc_vul'] = sc_vul
    context['sc_deki'] = sc_deki
    

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



#@login_required(login_url="/login/")
def pages(request):
    stored_selected_date = None
    context = {}
    num_delivery_result = num_delivery(stored_selected_date) 
    num_finised_task = num_delivery_result
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        context['number_of_deliveries_1']= num_finised_task


        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



