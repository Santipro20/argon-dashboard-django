from channels.generic.websocket import AsyncWebsocketConsumer
import simplejson as json
from apps.home.tasks import num_delivery, get_data_cydi, get_data_id, eco_km, time_eco, CO2, graph_CO2, equivalence,space_eco, KPI_CO2, graph_line, graph_jk, livra_state, livra_state, KPI_livra

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        stored_selected_date =  text_data_json.get('selected_date')
        selected_city = text_data_json.get('selected_city')
        newuser = text_data_json.get('newuser')
        print("Nuevo usuario:", newuser)
        new_user = text_data_json.get('new_user')
        print("Nuevo usuario:", new_user)
        season = text_data_json.get('selected_period')

        if newuser:
            newuser =newuser
        elif new_user:
            newuser =new_user
        else:
            newuser =None

        print("Fecha seleccionada:", stored_selected_date)
        print("Nuevo usuario:", newuser)
        print("Nueva city:", selected_city)
        print("Nuevo periodo:", season)

        if newuser is not None:
            num_delivery_result = num_delivery(stored_selected_date, selected_city,newuser) 
            economi_km = eco_km(stored_selected_date, selected_city , newuser) 
            time_eco_e = time_eco(stored_selected_date, selected_city ,newuser) 
            CO2_fun = CO2(stored_selected_date,  selected_city, newuser)
            graph = graph_CO2(stored_selected_date,selected_city , newuser)
            equ = equivalence(stored_selected_date, selected_city ,newuser)
            sp = space_eco(stored_selected_date,selected_city , newuser)
            KPI = KPI_CO2(stored_selected_date,selected_city,newuser)
            line = graph_line(stored_selected_date,selected_city,newuser,season=season)
            bar_jk = graph_jk(stored_selected_date,selected_city,newuser)
            livra_s = livra_state(stored_selected_date,selected_city,newuser)
            KPI_l = KPI_livra(stored_selected_date,selected_city,newuser) 
        else:
            num_delivery_result = num_delivery(stored_selected_date,selected_city) 
            economi_km = eco_km(stored_selected_date,selected_city ) 
            time_eco_e = time_eco(stored_selected_date,selected_city ) 
            CO2_fun = CO2(stored_selected_date, selected_city)
            graph = graph_CO2(stored_selected_date, selected_city )
            equ = equivalence(stored_selected_date, selected_city )
            sp = space_eco(stored_selected_date, selected_city)
            KPI = KPI_CO2(stored_selected_date, selected_city)
            line = graph_line(stored_selected_date,selected_city,season=season)
            bar_jk = graph_jk(stored_selected_date,selected_city)
            livra_s = livra_state(stored_selected_date,selected_city)
            KPI_l = KPI_livra(stored_selected_date,selected_city) 

        updated_data = {
            'number_of_deliveries': num_delivery_result,
            'porcentage_km': economi_km[0],
            'value_km': economi_km[1],
            'value_h': time_eco_e[1],
            'porcentage_h': time_eco_e[0],
            'value_e': CO2_fun[1],
            'porcentage_e': CO2_fun[0],
            'driving': CO2_fun[2],
            'cycliung': CO2_fun[3],
            'deki_vul': CO2_fun[4],
            'VUL_met': graph[0],
            'VUL_no2': graph[1],
            'VUL_NOx': graph[2],
            'VUL_CO' : graph[3],
            'VUL_PM' : graph[4],
            'deki_met': graph[5],
            'deki_no2': graph[6],
            'deki_NOx': graph[7],
            'deki_CO' : graph[8],
            'deki_PM' : graph[9],
            'deki_vul_met': graph[10],
            'deki_vul_no2': graph[11],
            'deki_vul_NOx': graph[12],
            'deki_vul_CO': graph[13],
            'deki_vul_PM': graph[14],
            'recharge_portable': equ[0],
            'recharge_ordina': equ[1],
            'arbes_hec': equ[2],
            'train_voya': equ[3],
            'diesel_E10': equ[4], 
            'uber_livra': equ[5],
            'feuilles_print': equ[6],
            'emails': equ[7],
            'travailleur_moyen': equ[8],
            'water_bo' : equ[9],
            'pain_tranches': equ[10],
            'portion_fromage': equ[11],
            'sc_eco' : sp[0],
            'sc_vul': sp[1],
            'sc_deki' : sp[2],
            'livra_KPI' : KPI[0],
            'km_KPI': KPI[1],
            'coli_KPI': KPI[2],
            'poids_KPI': KPI[3],
            'm2_KPI' : KPI[5],
            'temps' : KPI[4], 
            'colis': KPI[6],
            'kilos': KPI[7],
            'distance_par': economi_km[2],
            'value0': line[0],
            'value1': line[1],
            'value2': line[2],
            'time_d' : time_eco_e[3],
            'time_c' : time_eco_e[2],
            'distance_d' : economi_km[3],
            'distance_c' : economi_km[2],
            'days_week' : line[3],
            'j_0': bar_jk[0], 
            'j_1': bar_jk[1],
            'j_2': bar_jk[2],
            'k_1': bar_jk[3],
            'k_2': bar_jk[4],
            'k_3': bar_jk[5],
            'k_4': bar_jk[6],
            'k_5': bar_jk[7],
            'num': livra_s[0],
            'num1': livra_s[1],
            'num2':livra_s[2],
            'num3': livra_s[3],
            'num4':livra_s[4],
            'value1' : economi_km[4],
            'value2' : time_eco_e[4], 
            'value3' : KPI_l[1],
            'value4' : KPI_l[0], 
        }


        await self.send(text_data=json.dumps({
            'updated_data': updated_data
        }, use_decimal=True))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message'], use_decimal=True))
