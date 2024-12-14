import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Extract the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.roomGroupName = f'chat_{self.room_name}'
        
        # Add the channel to the room group
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        
        # Accept the WebSocket connection
        await self.accept()
        
        # Send confirmation message
        await self.send(text_data=json.dumps({
            'message': f'Connected to room: {self.room_name}'
        }))
    
    async def disconnect(self, close_code):
        # Remove the channel from the room group
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # Parse the incoming WebSocket message
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        
        # Send the message to the room group
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            }
        )
                
    async def sendMessage(self, event):
        # Extract message details from the event
        message = event["message"]
        username = event["username"]
        
        # Send the message back to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))
