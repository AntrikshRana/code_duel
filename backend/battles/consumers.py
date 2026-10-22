import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BattleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'battle_{self.room_code}'

        # Join battle room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get('action')
            payload = data.get('payload', {})

            # Broadcast event to all players in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'battle_message',
                    'action': action,
                    'payload': payload
                }
            )
        except Exception as e:
            pass

    async def battle_message(self, event):
        # Send message to WebSocket client
        await self.send(text_data=json.dumps({
            'action': event['action'],
            'payload': event['payload']
        }))
