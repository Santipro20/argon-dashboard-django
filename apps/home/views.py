# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.tasks import num_delivery, get_data_cydi, get_data_id, eco_km, time_eco, CO2, graph_CO2, equivalence,space_eco, KPI_CO2
from django.views.decorators.csrf import csrf_protect #csrf_exempt
from django.views.generic import TemplateView



#@login_required(login_url="/login/")
@csrf_protect
def index(request,newuser=None):
    stored_selected_date = None
    selected_city = None
    context = {'segment': 'index'}

    if newuser is not None:
        num_delivery_result = num_delivery(stored_selected_date, selected_city ,newuser) 
        economi_km = eco_km(stored_selected_date, selected_city , newuser) 
        time_eco_e = time_eco(stored_selected_date,selected_city ,newuser) 
        CO2_fun = CO2(stored_selected_date, selected_city, newuser)
        graph = graph_CO2(stored_selected_date,selected_city , newuser)
        equ = equivalence(stored_selected_date,selected_city , newuser)
        sp = space_eco(stored_selected_date, selected_city ,newuser)
        KPI = KPI_CO2(stored_selected_date,selected_city,newuser)

        if newuser == 'group_id=1' or newuser == 1:
            user ='Group'
        elif newuser == 'team_id=2' or newuser == 2:
            user = 'Prestataire'
        elif newuser == 'team_id=3' or newuser == 3:
            user = 'Prestataire'
        elif newuser == 'team_id=4' or newuser == 4:
            user = 'Prestataire'
        elif newuser == 'team_id=6' or newuser == 6:
            user = 'Prestataire'
        elif newuser == 'team_id=9' or newuser == 9:
            user = 'Prestataire'
        elif newuser == 'team_id=10' or newuser == 10:
            user = 'Prestataire'
        elif newuser == 'team_id=11' or newuser == 11:
            user = 'Prestataire'
        elif newuser == 'team_id=13' or newuser == 13:
            user = 'Prestataire'
        elif newuser == 'team_id=14' or newuser == 14:
            user = 'Prestataire'
        elif newuser == 'team_id=15' or newuser == 15:
            user = 'Prestataire'
        elif newuser == 'team_id=16' or newuser == 16:
            user = 'Prestataire'
        elif newuser == 'team_id=17' or newuser == 17:
            user = 'Prestataire'
        elif newuser == 'team_id=18' or newuser == 18:
            user = 'Prestataire'
        elif newuser == 'team_id=19' or newuser == 19:
            user = 'Prestataire'
        elif newuser == 'team_id=20' or newuser == 20:
            user = 'Prestataire'
        elif newuser == 'team_id=22' or newuser == 22:
            user = 'Prestataire'
        elif newuser == 'merchant_id=606' or newuser == 606:
            user = 'Merchant'
        elif newuser == 'merchant_id=605' or newuser == 605:
            user = 'Merchant'
        elif newuser == 'merchant_id=607' or newuser == 607:
            user = 'Merchant'
        elif newuser == 'merchant_id=609' or newuser == 609:
            user = 'Merchant'
        elif newuser == 'merchant_id=610' or newuser == 610:
            user = 'Merchant'
        elif newuser == 'merchant_id=617' or newuser == 617:
            user = 'Merchant'
        elif newuser == 'merchant_id=630' or newuser == 630:
            user = 'Merchant'
        elif newuser == 'merchant_id=635' or newuser == 635:
            user = 'Merchant'
        elif newuser == 'merchant_id=640' or newuser == 640:
            user = 'Merchant'
        elif newuser == 'merchant_id=641' or newuser == 641:
            user = 'Merchant'
        elif newuser == 'merchant_id=649' or newuser == 649:
            user = 'Merchant'
        elif newuser == 'merchant_id=650' or newuser == 650:
            user = 'Merchant'
        elif newuser == 'merchant_id=651' or newuser == 651:
            user = 'Merchant'
        elif newuser == 'merchant_id=652' or newuser == 652:
            user = 'Merchant'
    else:
        num_delivery_result = num_delivery(stored_selected_date,selected_city) 
        economi_km = eco_km(stored_selected_date, selected_city ) 
        time_eco_e = time_eco(stored_selected_date, selected_city ) 
        CO2_fun = CO2(stored_selected_date,  selected_city)
        graph = graph_CO2(stored_selected_date, selected_city )
        equ = equivalence(stored_selected_date,selected_city )
        sp = space_eco(stored_selected_date,selected_city )
        KPI = KPI_CO2(stored_selected_date, selected_city)
        user =  'Admin'

    num_finised_task = num_delivery_result
    km_saved, km_saved_total = economi_km
    time_saved, time_saved_total = time_eco_e
    emi,emi_total,driving,cycling,deki_vul  = CO2_fun
    VUL_met, VUL_no2, VUL_NOx, VUL_CO, VUL_PM,deki_met, deki_no2,deki_NOx,deki_CO, deki_PM,deki_vul_met,deki_vul_no2,deki_vul_NOx,deki_vul_CO,deki_vul_PM= graph
    charger_iphone,charger_mac,trees,train, diesel, uber, print_sheet, emails, labor, water, pain, fromage  = equ
    sc_s,sc_vul,sc_deki=sp
    livra_eco_CO2,km_eco_CO2,coli_eco_CO2,weight_eco_CO2,time_eco_CO2,congestion_eco_CO2 =KPI


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
    context['newuserf'] = newuser
    context['livra_KPI'] = livra_eco_CO2
    context['km_KPI'] = km_eco_CO2
    context['coli_KPI'] = coli_eco_CO2
    context['poids_KPI'] = weight_eco_CO2
    context['m2_KPI'] = congestion_eco_CO2
    context['temps'] = time_eco_CO2
    context['selected_option'] = user

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



#@login_required(login_url="/login/")
def pages(request, new_user):
    stored_selected_date = None
    context = {}
    if new_user is not None:
        num_delivery_result = num_delivery(stored_selected_date, new_user) 
    else:
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
    




