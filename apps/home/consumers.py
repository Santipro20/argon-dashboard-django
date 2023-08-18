
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_updated_value(self, event):
        nuevo_valor_h = event['nuevo_valor_h']

        # Envía el nuevo valor al cliente a través del WebSocket
        await self.send(text_data=json.dumps({'nuevo_valor_h': nuevo_valor_h}))