from channels.generic.websocket import AsyncWebsocketConsumer
import simplejson as json
from apps.home.tasks import num_delivery, get_data_cydi, get_data_id, eco_km, time_eco, CO2, graph_CO2

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        stored_selected_date =  text_data_json['value']

        num_delivery_result = num_delivery(stored_selected_date)
        time_eco_e = time_eco(stored_selected_date)
        economi_km = eco_km(stored_selected_date)
        CO2_fun = CO2(stored_selected_date)
        graph = graph_CO2(stored_selected_date)


        num_finised_task = num_delivery_result
        km_saved, km_saved_total = economi_km
        time_saved, time_saved_total = time_eco_e
        emi, emi_total, driving, cycling = CO2_fun 
        VUL_met,VUL_no2,VUL_oz,deki_met,deki_no2,deki_oz = graph


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
            'VUL_met':VUL_met,
            'VUL_no2': VUL_no2,
            'VUL_oz': VUL_oz,
            'deki_met': deki_met,
            'deki_no2': deki_no2,
            'deki_oz': deki_oz
        }

        await self.send(text_data=json.dumps({
            'updated_data': updated_data
        }, use_decimal=True))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message'], use_decimal=True))
