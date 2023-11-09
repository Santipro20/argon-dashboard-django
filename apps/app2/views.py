# from django import template
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
#   from django.urls import reverse
from apps.home.tasks import (
    num_delivery,
    get_data_cydi,
    get_data_id,
    eco_km,
    time_eco,
    CO2,
    graph_CO2,
    equivalence,
    space_eco,
    KPI_CO2,
    graph_line,
    graph_jk,
    livra_state,
    KPI_livra,
)
from django.views.decorators.csrf import csrf_protect  # csrf_exempt
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import render


# Create your views here.
class Page1View(TemplateView):
    template_name = "app2/index2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        stored_selected_date = None
        selected_city = None
        newuser = self.kwargs.get("new_user")
        user = None
        season = None

        if newuser is not None:
            num_delivery_result = num_delivery(
                stored_selected_date, selected_city, newuser
            )
            KPI = KPI_CO2(stored_selected_date, selected_city, newuser)
            economi_km = eco_km(stored_selected_date, selected_city, newuser)
            line = graph_line(stored_selected_date, selected_city, newuser, season)
            time = time_eco(stored_selected_date, selected_city, newuser)
            bar_jk = graph_jk(stored_selected_date, selected_city, newuser)
            livra_s = livra_state(stored_selected_date, selected_city, newuser)
            KPI_l = KPI_livra(stored_selected_date, selected_city, newuser)
            user_mapping = {
                "group_id=1": "Group",
                1: "Group",
                "team_id=2": "Prestataire",
                2: "Prestataire",
                "team_id=3": "Prestataire",
                3: "Prestataire",
                "team_id=4": "Prestataire",
                4: "Prestataire",
                "team_id=6": "Prestataire",
                6: "Prestataire",
                "team_id=9": "Prestataire",
                9: "Prestataire",
                "team_id=10": "Prestataire",
                10: "Prestataire",
                "team_id=11": "Prestataire",
                11: "Prestataire",
                "team_id=13": "Prestataire",
                13: "Prestataire",
                "team_id=14": "Prestataire",
                14: "Prestataire",
                "team_id=15": "Prestataire",
                15: "Prestataire",
                "team_id=16": "Prestataire",
                16: "Prestataire",
                "team_id=17": "Prestataire",
                17: "Prestataire",
                "team_id=18": "Prestataire",
                18: "Prestataire",
                "team_id=19": "Prestataire",
                19: "Prestataire",
                "team_id=20": "Prestataire",
                20: "Prestataire",
                "team_id=22": "Prestataire",
                22: "Prestataire",
                "merchant_id=606": "Merchant",
                606: "Merchant",
                "merchant_id=605": "Merchant",
                605: "Merchant",
                "merchant_id=607": "Merchant",
                607: "Merchant",
                "merchant_id=609": "Merchant",
                609: "Merchant",
                "merchant_id=610": "Merchant",
                610: "Merchant",
                "merchant_id=617": "Merchant",
                617: "Merchant",
                "merchant_id=630": "Merchant",
                630: "Merchant",
                "merchant_id=635": "Merchant",
                635: "Merchant",
                "merchant_id=640": "Merchant",
                640: "Merchant",
                "merchant_id=641": "Merchant",
                641: "Merchant",
                "merchant_id=649": "Merchant",
                649: "Merchant",
                "merchant_id=650": "Merchant",
                650: "Merchant",
                "merchant_id=651": "Merchant",
                651: "Merchant",
                "merchant_id=652": "Merchant",
                652: "Merchant",
            }
            if newuser in user_mapping:
                user = user_mapping[newuser]

        else:
            user = "Admin"
            num_delivery_result = num_delivery(stored_selected_date, selected_city)
            KPI = KPI_CO2(stored_selected_date, selected_city)
            economi_km = eco_km(stored_selected_date, selected_city)
            line = graph_line(stored_selected_date, selected_city, season)
            time = time_eco(stored_selected_date, selected_city)
            bar_jk = graph_jk(stored_selected_date, selected_city)
            livra_s = livra_state(stored_selected_date, selected_city)
            KPI_l = KPI_livra(stored_selected_date, selected_city)

        segment = "icons"

        context["selected_option"] = user
        context["segment"] = segment
        context["number_of_deliveries"] = num_delivery_result
        context["colis"] = KPI[6]
        context["kilos"] = KPI[7]
        context["distance_par"] = economi_km[2]
        context["newuserh"] = newuser
        context["valueline"] = line[0]
        context["valueline1"] = line[1]
        context["valueline2"] = line[2]
        context["temps_driving"] = time[3]
        context["temps_cycling"] = time[2]
        context["distance_cycling"] = economi_km[2]
        context["distance_driving"] = economi_km[3]
        context["days_week"] = line[3]
        context["j_0"] = bar_jk[0]
        context["j_1"] = bar_jk[1]
        context["j_2"] = bar_jk[2]
        context["k_1"] = bar_jk[3]
        context["k_2"] = bar_jk[4]
        context["k_3"] = bar_jk[5]
        context["k_4"] = bar_jk[6]
        context["k_5"] = bar_jk[7]
        context["num"] = livra_s[0]
        context["num1"] = livra_s[1]
        context["num2"] = livra_s[2]
        context["num3"] = livra_s[3]
        context["num4"] = livra_s[4]
        context["value1"] = economi_km[4]
        context["value2"] = time[4]
        context["value3"] = KPI_l[1]
        context["value4"] = KPI_l[0]
        return context
