from channels.generic.websocket import AsyncWebsocketConsumer
import simplejson as json
from apps.home.tasks import num_delivery, get_data_cydi, get_data_id, eco_km, time_eco, CO2, graph_CO2, equivalence,space_eco, KPI_CO2

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        stored_selected_date =  text_data_json.get('selected_date')
        newuser = text_data_json.get('newuser')
        selected_city = text_data_json.get('selected_city')
        print("Fecha seleccionada:", stored_selected_date)
        print("Nuevo usuario:", newuser)
        print("Nueva city:", selected_city)

        if newuser is not None:
            num_delivery_result = num_delivery(stored_selected_date, selected_city,newuser) 
            economi_km = eco_km(stored_selected_date, selected_city , newuser) 
            time_eco_e = time_eco(stored_selected_date, selected_city ,newuser) 
            CO2_fun = CO2(stored_selected_date,  selected_city, newuser)
            graph = graph_CO2(stored_selected_date,selected_city , newuser)
            equ = equivalence(stored_selected_date, selected_city ,newuser)
            sp = space_eco(stored_selected_date,selected_city , newuser)
            KPI = KPI_CO2(stored_selected_date,selected_city,newuser)
        else:
            num_delivery_result = num_delivery(stored_selected_date,selected_city) 
            economi_km = eco_km(stored_selected_date,selected_city ) 
            time_eco_e = time_eco(stored_selected_date,selected_city ) 
            CO2_fun = CO2(stored_selected_date, selected_city)
            graph = graph_CO2(stored_selected_date, selected_city )
            equ = equivalence(stored_selected_date, selected_city )
            sp = space_eco(stored_selected_date, selected_city)
            KPI = KPI_CO2(stored_selected_date, selected_city)

        num_finised_task = num_delivery_result
        km_saved, km_saved_total = economi_km
        time_saved, time_saved_total = time_eco_e
        emi,emi_total,driving,cycling,deki_vul  = CO2_fun
        VUL_met, VUL_no2, VUL_NOx, VUL_CO, VUL_PM,deki_met, deki_no2,deki_NOx,deki_CO, deki_PM,deki_vul_met,deki_vul_no2,deki_vul_NOx,deki_vul_CO,deki_vul_PM= graph
        charger_iphone,charger_mac,trees,train, diesel, uber, print_sheet, emails, labor, water, pain, fromage  = equ
        sc_s,sc_vul,sc_deki=sp
        livra_eco_CO2,km_eco_CO2,coli_eco_CO2,weight_eco_CO2,time_eco_CO2,congestion_eco_CO2 =KPI

        updated_data = {
            'number_of_deliveries': num_finised_task,
            'porcentage_km': km_saved,
            'value_km': km_saved_total,
            'value_h': time_saved_total,
            'porcentage_h': time_saved,
            'value_e': emi_total,
            'porcentage_e': emi,
            'driving': driving,
            'cycliung':cycling,
            'deki_vul' : deki_vul,
            'VUL_met':VUL_met,
            'VUL_no2': VUL_no2,
            'VUL_NOx': VUL_NOx,
            'VUL_CO' : VUL_CO,
            'VUL_PM' : VUL_PM,
            'deki_met': deki_met,
            'deki_no2': deki_no2,
            'deki_NOx': deki_NOx,
            'deki_CO' : deki_CO,
            'deki_PM' : deki_PM,
            'deki_vul_met' : deki_vul_met,
            'deki_vul_no2' : deki_vul_no2,
            'deki_vul_NOx' : deki_vul_NOx,
            'deki_vul_CO': deki_vul_CO,
            'deki_vul_PM' : deki_vul_PM,
            'recharge_portable': charger_iphone,
            'recharge_ordina': charger_mac,
            'arbes_hec': trees,
            'train_voya': train,
            'diesel_E10': diesel, 
            'uber_livra': uber,
            'feuilles_print': print_sheet,
            'emails': emails,
            'travailleur_moyen': labor,
            'water_bo' : water,
            'pain_tranches': pain,
            'portion_fromage': fromage,
            'sc_eco' : sc_s,
            'sc_vul': sc_vul,
            'sc_deki' : sc_deki,
            'livra_KPI' : livra_eco_CO2,
            'km_KPI': km_eco_CO2,
            'coli_KPI': coli_eco_CO2,
            'poids_KPI': weight_eco_CO2,
            'm2_KPI' : congestion_eco_CO2,
            'temps' : time_eco_CO2, 

        }

        await self.send(text_data=json.dumps({
            'updated_data': updated_data
        }, use_decimal=True))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message'], use_decimal=True))
