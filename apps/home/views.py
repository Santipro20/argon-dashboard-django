# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#from django import template
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
#   from django.urls import reverse
from apps.home.tasks import num_delivery, get_data_cydi, get_data_id, eco_km, time_eco, CO2, graph_CO2, equivalence,space_eco, KPI_CO2
from django.views.decorators.csrf import csrf_protect #csrf_exempt
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator 
from django.shortcuts import render



#@login_required(login_url="/login/")
@method_decorator(csrf_protect, name='dispatch')
class BasePageView(TemplateView):
    template_name = 'home/index.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stored_selected_date = None
        selected_city = None 
        newuser = self.kwargs.get('newuser') 
        user = None

        if newuser is not None :
            num_delivery_result = num_delivery(stored_selected_date, selected_city ,newuser) 
            economi_km = eco_km(stored_selected_date, selected_city , newuser) 
            time_eco_e = time_eco(stored_selected_date,selected_city ,newuser) 
            CO2_fun = CO2(stored_selected_date, selected_city, newuser)
            graph = graph_CO2(stored_selected_date,selected_city , newuser)
            equ = equivalence(stored_selected_date,selected_city , newuser)
            sp = space_eco(stored_selected_date, selected_city ,newuser)
            KPI = KPI_CO2(stored_selected_date,selected_city,newuser)

            user_mapping = {
                'group_id=1': 'Group',1: 'Group','team_id=2': 'Prestataire',2: 'Prestataire','team_id=3': 'Prestataire',
                3: 'Prestataire','team_id=4': 'Prestataire',4: 'Prestataire','team_id=6': 'Prestataire',6: 'Prestataire',
                'team_id=9': 'Prestataire',9: 'Prestataire','team_id=10': 'Prestataire',10: 'Prestataire','team_id=11': 'Prestataire',
                11: 'Prestataire','team_id=13': 'Prestataire',13: 'Prestataire','team_id=14': 'Prestataire',14: 'Prestataire',
                'team_id=15': 'Prestataire',15: 'Prestataire','team_id=16': 'Prestataire',16: 'Prestataire','team_id=17': 'Prestataire',
                17: 'Prestataire','team_id=18': 'Prestataire',18: 'Prestataire','team_id=19': 'Prestataire',19: 'Prestataire',
                'team_id=20': 'Prestataire',20: 'Prestataire','team_id=22': 'Prestataire',22: 'Prestataire','merchant_id=606': 'Merchant',
                606: 'Merchant','merchant_id=605': 'Merchant',605: 'Merchant','merchant_id=607': 'Merchant',607: 'Merchant','merchant_id=609': 'Merchant',
                609: 'Merchant','merchant_id=610': 'Merchant',610: 'Merchant','merchant_id=617': 'Merchant',617: 'Merchant','merchant_id=630': 'Merchant',
                630: 'Merchant', 'merchant_id=635': 'Merchant', 635: 'Merchant','merchant_id=640': 'Merchant', 640: 'Merchant','merchant_id=641': 'Merchant',
                641: 'Merchant','merchant_id=649': 'Merchant',649: 'Merchant','merchant_id=650': 'Merchant',650: 'Merchant','merchant_id=651': 'Merchant',
                651: 'Merchant','merchant_id=652': 'Merchant',652: 'Merchant'}
            if newuser in user_mapping:
                user = user_mapping[newuser]
        else:
            user =  'Admin'
            num_delivery_result = num_delivery(stored_selected_date,selected_city) 
            economi_km = eco_km(stored_selected_date, selected_city ) 
            time_eco_e = time_eco(stored_selected_date, selected_city ) 
            CO2_fun = CO2(stored_selected_date,  selected_city)
            graph = graph_CO2(stored_selected_date, selected_city )
            equ = equivalence(stored_selected_date,selected_city )
            sp = space_eco(stored_selected_date,selected_city )
            KPI = KPI_CO2(stored_selected_date, selected_city)

        segment = 'index' 

        # Share info with the context
        context['number_of_deliveries'] = num_delivery_result
        context['porcentage_km'] =economi_km[0]
        context['value_km'] = economi_km[1]
        context['value_h'] = time_eco_e[1]
        context['porcentage_h'] = time_eco_e[0]
        context['value_e'] = CO2_fun[1]
        context['porcentage_e'] = CO2_fun[0]
        context['driving_data'] = CO2_fun[2]
        context['cycling_data'] = CO2_fun[3]
        context['deki_vul_data'] = CO2_fun[4]
        context['VUL_met_data'] = graph[0]
        context['VUL_no2_data'] = graph[1]
        context['VUL_NOx_data'] = graph[2]
        context['VUL_CO_data'] = graph[3]
        context['VUL_PM_data'] = graph[4]
        context['deki_met_data'] = graph[5]
        context['deki_no2_data'] = graph[6]
        context['deki_NOx_data'] = graph[7]
        context['deki_CO_data'] = graph[8]
        context['deki_PM_data'] = graph[9]
        context['deki_vul_met_data'] = graph[10]
        context['deki_vul_no2_data'] = graph[11]
        context['deki_vul_NOx_data'] = graph[12]
        context['deki_vul_CO_data'] = graph[13]
        context['deki_vul_PM_data'] = graph[14]
        context['recharge_portable'] = equ[0]
        context['recharge_ordina'] = equ[1]
        context['arbes_hec'] = equ[2]
        context['train_voya'] = equ[3]
        context['diesel_E10'] = equ[4]
        context['uber_livra'] = equ[5]
        context['feuilles_print'] = equ[6]
        context['emails'] = equ[7]
        context['travailleur_moyen'] = equ[8]
        context['water_bo'] = equ[9]
        context['pain_tranches'] = equ[10]
        context['portion_fromage'] = equ[11]
        context['sc_eco'] = sp[0]
        context['sc_vul'] = sp[1]
        context['sc_deki'] = sp[2]
        context['newuserf'] = newuser
        context['livra_KPI'] = KPI[0]
        context['km_KPI'] = KPI[1]
        context['coli_KPI'] = KPI[2]
        context['poids_KPI'] = KPI[3]
        context['m2_KPI'] = KPI[5]
        context['temps'] = KPI[4]
        context['selected_option'] = user
        context['segment'] = segment
        return context
    


    


